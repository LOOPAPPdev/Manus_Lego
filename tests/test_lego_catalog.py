import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
from unittest import TestCase, main, mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import lego_catalog as lib


class CatalogUnitTests(TestCase):
    def test_private_url_rejected(self):
        for s in ["https://dash.cloudflare.com/999/workers", "http://api.github.com/repos/a/b", "https://evil.invalid/x", "https://api.github.com.evil.invalid/x"]:
            with self.assertRaises(ValueError):
                lib.safe_url(s)

    def test_github_path_ref(self):
        self.assertEqual(lib.repo_info("https://github.com/cloudflare/templates/tree/main/astro-blog-starter-template"), {"repo": "cloudflare/templates", "ref": "main", "path": "astro-blog-starter-template"})

    def test_official_cloudflare_roots(self):
        tree = [{"path": "astro-blog-starter-template/package.json", "type": "blob", "sha": "1"}, {"path": "astro-blog-starter-template/README.md", "type": "blob", "sha": "2"}, {"path": ".github/workflows/ci.yml", "type": "blob", "sha": "3"}]
        self.assertEqual(lib.discover_roots("cloudflare", tree), ["astro-blog-starter-template"])
        results = lib.repo_records("cloudflare", "cloudflare/templates", "abcd1234", tree, False)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["inventory"]["file_count"], 2)
        self.assertTrue(results[0]["readme"]["url"].endswith("astro-blog-starter-template/README.md"))
        self.assertTrue(results[0]["inventory"]["complete"])

    def test_vercel_nested_roots(self):
        paths = ["solutions/image-app/README.md", "solutions/image-app/package.json", "solutions/image-app/src/app/page.tsx", "internal/tool/README.md", ".github/test/package.json"]
        tree = [{"path": p, "type": "blob"} for p in paths]
        self.assertEqual(lib.discover_roots("vercel", tree), ["solutions/image-app"])

    def test_truncated_tree_is_not_complete(self):
        tree = [{"path": "a-template/package.json", "type": "blob", "sha": "a"}]
        r = lib.repo_records("cloudflare", "cloudflare/templates", "c" * 40, tree, True)[0]
        self.assertFalse(r["inventory"]["complete"])
        self.assertIn("truncated", " ".join(r["warnings"]))

    def test_jsonc_comments_and_url_string(self):
        v = lib.extract_jsonc('{"url":"https://demo.example/x", // comment\n "d1_databases": [1,], /* test */ }')
        self.assertEqual(v["url"], "https://demo.example/x")
        self.assertEqual(v["d1_databases"], [1])

    def test_gallery_extracts_template_urls(self):
        html = '<a href="/templates/ai/my-agent">Agent</a><a href="/templates/ai">AI</a><a href="https://evil.invalid/templates/ai/xx">X</a>'
        self.assertEqual(lib.gallery_links(html, "https://vercel.com/templates/ai"), ["https://vercel.com/templates/ai/my-agent"])

    def test_gallery_repository_url(self):
        html = '<title>Astro Blog</title><meta name="description" content="Blog starter"><a href="https://github.com/withastro/astro">astro</a>'
        x = lib.vercel_gallery_record("https://vercel.com/templates/astro/astro-blog", html)
        self.assertEqual(x["repo"], "withastro/astro")
        self.assertIn("Blog starter", x["description"])

    def test_scoring_ignores_empty_hits_and_prefers_match(self):
        source = {"templates": [{"id": "a", "provider": "cloudflare", "title": "React Database", "tags": ["database"], "features": ["database"], "path": "react-database", "stack": {"frameworks": ["react"]}}, {"id": "b", "provider": "vercel", "title": "Blog", "tags": ["blog"], "features": [], "path": "blog", "stack": {"frameworks": []}}]}
        self.assertEqual(lib.ranked(source, "react database")[0]["id"], "a")
        self.assertEqual(lib.ranked(source, "unrelated"), [])

    def test_offline_end_to_end_with_mock_api(self):
        from argparse import Namespace
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            src = d / "sources.json"
            src.write_text(json.dumps({"github_sources": [{"provider": "cloudflare", "repo": "cloudflare/templates"}]}))
            commit = "a" * 40
            responses = {
                "https://api.github.com/repos/cloudflare/templates": {"default_branch": "main"},
                "https://api.github.com/repos/cloudflare/templates/commits/main": {"sha": commit},
                f"https://api.github.com/repos/cloudflare/templates/git/trees/{commit}?recursive=1": {"truncated": False, "tree": [
                    {"path": "astro-blog-starter-template/package.json", "type": "blob", "sha": "abc", "size": 300},
                    {"path": "astro-blog-starter-template/README.md", "type": "blob", "sha": "def", "size": 100},
                ]},
            }
            content = {
                "templates.json": {"templates": {"astro-blog-starter-template": {}}},
                "astro-blog-starter-template/package.json": {"description": "Astro Blog starter", "cloudflare": {"products": ["Workers"], "publish": True}, "dependencies": {"astro": "5.0.0"}, "scripts": {"dev": "astro dev"}},
            }
            def fake_get(_http, url):
                if url in responses: return json.dumps(responses[url]).encode()
                for path, payload in content.items():
                    if url.startswith(f"https://api.github.com/repos/cloudflare/templates/contents/{path}?"):
                        import base64
                        raw = json.dumps(payload).encode()
                        return json.dumps({"type": "file", "size": len(raw), "encoding": "base64", "content": base64.b64encode(raw).decode()}).encode()
                if "README.md" in url:
                    import base64
                    raw = b"# Astro Blog\n\nA simple blog starter with MDX."
                    return json.dumps({"type": "file", "size": len(raw), "encoding": "base64", "content": base64.b64encode(raw).decode()}).encode()
                raise AssertionError("Unexpected URL: " + url)
            args = Namespace(output=str(d), sources=str(src), offline=False, refresh=False, pause=0, max_enrich=4, max_templates=None, gallery=False, max_pages=0)
            with mock.patch.object(lib.HTTP, "get", fake_get), contextlib.redirect_stdout(io.StringIO()):
                lib.index_command(args)
            index = lib.read_json(d / "catalog" / "index.json")
            self.assertEqual(index["template_count"], 1)
            record = next((d / "catalog" / "templates" / "cloudflare").glob("*.json"))
            r = lib.read_json(record)
            self.assertEqual(r["stack"]["dependencies"]["astro"], "5.0.0")
            self.assertEqual(r["commands"]["dev"], "astro dev")
            self.assertIn("cloudflare-workers", r["stack"]["products"])
            self.assertTrue(r["platform_metadata"]["listed_in_templates_json"])
            with contextlib.redirect_stdout(io.StringIO()):
                lib.validate_command(Namespace(output=str(d)))
            self.assertTrue((d / "catalog" / "master_index.csv").exists())


if __name__ == "__main__":
    main()
