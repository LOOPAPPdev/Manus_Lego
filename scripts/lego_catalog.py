#!/usr/bin/env python3
"""Manus LEGO: reference-only inventory for Cloudflare and Vercel templates.

Python 3.11+; standard library only. Does not clone, run, or deploy external code.
"""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sys
import time
from typing import Any
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "Manus-Lego-Index/1.0 (+https://github.com/LOOPAPPdev/Manus_Lego)"
GITHUB_REPO = re.compile(r"^https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)(?:/(?:tree|blob)/([^?#]+))?/?$")
MANIFEST_VERSION = "1.0.0"
DOCS = {"README.md", "README.MD", "readme.md"}
MANIFEST_FILES = {"package.json", "pyproject.toml", "requirements.txt", "wrangler.jsonc", "wrangler.toml", "vercel.json", "Cargo.toml", "go.mod", "Dockerfile", "astro.config.mjs", "next.config.js", "next.config.mjs", "next.config.ts", "vite.config.ts", "CLAUDE.md", "AGENTS.md", "LICENSE", "LICENSE.md"}
LANGUAGE_EXTS = {".ts": "TypeScript", ".tsx": "TypeScript", ".js": "JavaScript", ".jsx": "JavaScript", ".py": "Python", ".go": "Go", ".rs": "Rust", ".astro": "Astro", ".vue": "Vue", ".svelte": "Svelte", ".css": "CSS", ".html": "HTML"}
FEATURE_LEXICON = {
    "authentication": ("auth", "next-auth", "better-auth", "clerk", "lucia"),
    "database": ("database", "postgres", "prisma", "drizzle", "supabase", "d1"),
    "ai": ("workers ai", "ai-sdk", "openai", "anthropic", "llm"),
    "blog": ("blog", "content collections", "mdx"),
    "commerce": ("stripe", "commerce", "checkout", "cart"),
    "realtime": ("websocket", "realtime", "durable object"),
    "cron": ("cron", "scheduler", "scheduled"),
    "storage": (" r2", "blob", "kv", "object storage"),
    "analytics": ("analytics", "metrics", "dashboard"),
    "multitenancy": ("multi-tenant", "multitenant", "tenant"),
}
PRODUCT_MAP = {
    "cloudflare-d1": ("d1",), "cloudflare-r2": ("r2",),
    "cloudflare-kv": ("kv_namespaces",), "durable-objects": ("durable_objects",),
    "cloudflare-ai": ("ai", "workers ai"), "vercel-blob": ("@vercel/blob",),
    "vercel-postgres": ("@vercel/postgres",), "vercel-ai-sdk": ("ai", "@ai-sdk/"),
    "supabase": ("supabase",), "stripe": ("stripe",),
}


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def put_json(path: Path, content: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(content, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:110] or "unknown"


def safe_url(url: str) -> str:
    """Restrict network access to known public hosts and HTTPS (SSRF baseline)."""
    parsed = urllib.parse.urlsplit(url)
    allow = {"api.github.com", "raw.githubusercontent.com", "vercel.com", "developers.cloudflare.com"}
    if parsed.scheme != "https" or (parsed.hostname or "").lower() not in allow or parsed.username or parsed.password or parsed.port:
        raise ValueError(f"Non-allowlisted source: {parsed.hostname or parsed.scheme}")
    if parsed.hostname == "vercel.com" and not (parsed.path.startswith("/templates") or parsed.path.endswith(".xml") or parsed.path == "/robots.txt"):
        raise ValueError("Only Vercel public gallery pages and sitemaps are permitted")
    if parsed.path.startswith("/75de") or "dash.cloudflare.com" in url:
        raise ValueError("Private dashboard paths prohibited")
    return url


class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        safe_url(newurl)
        # Avoid passing an API token to another host, even if both are allowlisted.
        if urllib.parse.urlsplit(newurl).hostname != urllib.parse.urlsplit(req.full_url).hostname and req.get_header("Authorization"):
            raise ValueError("Refusing authenticated cross-host redirect")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class HTTP:
    def __init__(self, cache_dir: Path, *, offline: bool = False, no_cache: bool = False, pause: float = 0.0):
        self.cache_dir = cache_dir
        self.offline = offline
        self.no_cache = no_cache
        self.pause = pause
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.stats = {"requests": 0, "cache_hits": 0, "errors": 0}

    def get(self, url: str) -> bytes:
        safe_url(url)
        cache_file = self.cache_dir / (hashlib.sha256(url.encode()).hexdigest() + ".bin")
        parsed = urllib.parse.urlsplit(url)
        dynamic = (parsed.hostname == "vercel.com" or bool(re.fullmatch(r"/repos/[^/]+/[^/]+", parsed.path)) or "/commits/" in parsed.path)
        if cache_file.exists() and not self.no_cache and (self.offline or not dynamic):
            self.stats["cache_hits"] += 1
            return cache_file.read_bytes()
        if self.offline:
            raise RuntimeError(f"Offline cache miss: {url}")
        headers = {"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json" if "api.github.com" in url else "text/html, application/xml, */*"}
        token = os.getenv("GITHUB_TOKEN")
        if token and urllib.parse.urlsplit(url).hostname == "api.github.com":
            headers["Authorization"] = "Bearer " + token
        last_error: Exception | None = None
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.build_opener(SafeRedirect()).open(req, timeout=20) as response:
                    if urllib.parse.urlsplit(response.geturl()).hostname not in {"api.github.com", "raw.githubusercontent.com", "vercel.com", "developers.cloudflare.com"}:
                        raise ValueError("Redirect to untrusted host")
                    data = response.read(12_000_001)
                    if len(data) > 12_000_000:
                        raise ValueError("Response exceeded 12 MB guard")
                    self.stats["requests"] += 1
                    cache_file.write_bytes(data)
                    if self.pause:
                        time.sleep(self.pause)
                    return data
            except urllib.error.HTTPError as exc:
                last_error = exc
                self.stats["errors"] += 1
                if exc.code not in {429, 500, 502, 503, 504} and not (exc.code == 403 and exc.headers.get("X-RateLimit-Remaining") == "0"):
                    break
                delay = min(int(exc.headers.get("Retry-After", 2 ** attempt)), 15)
                time.sleep(delay)
            except (urllib.error.URLError, TimeoutError) as exc:
                last_error = exc
                self.stats["errors"] += 1
                time.sleep(min(2 ** attempt, 8))
            except ValueError:
                raise
        raise RuntimeError(f"Fetch failed for {url}: {last_error}")

    def json(self, url: str) -> Any:
        return json.loads(self.get(url).decode("utf-8"))


class GalleryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._anchor_text: list[str] = []
        self.meta: dict[str, str] = {}
        self.words: list[str] = []
        self._in_title = False
        self.title = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if tag == "a":
            self._href = a.get("href")
            self._anchor_text = []
        elif tag == "meta":
            k = a.get("name") or a.get("property")
            if k and a.get("content"):
                self.meta[k] = a["content"] or ""
        elif tag == "title":
            self._in_title = True

    def handle_data(self, data: str) -> None:
        t = " ".join(data.split())
        if t:
            self.words.append(t)
            if self._href is not None:
                self._anchor_text.append(t)
            if self._in_title:
                self.title += t

    def handle_endtag(self, tag: str) -> None:
        if tag == "a":
            if self._href:
                self.links.append((self._href, " ".join(self._anchor_text).strip()))
            self._href = None
        elif tag == "title":
            self._in_title = False


def gallery_links(html: str, current: str) -> list[str]:
    p = GalleryParser()
    p.feed(html)
    links: set[str] = set()
    for href, _ in p.links:
        url = urllib.parse.urljoin(current, href)
        parsed = urllib.parse.urlsplit(url)
        if parsed.hostname == "vercel.com" and re.fullmatch(r"/templates/[a-z0-9.\-]+/[a-z0-9.\-]+/?", parsed.path):
            links.add("https://vercel.com" + parsed.path.rstrip("/"))
    return sorted(links)


def repo_info(url: str) -> dict[str, str] | None:
    match = GITHUB_REPO.match(url.split("#", 1)[0].split("?", 1)[0].rstrip("/"))
    if not match:
        return None
    owner, repo, fragment = match.groups()
    if repo.endswith(".git"):
        repo = repo[:-4]
    result = {"repo": f"{owner}/{repo}", "path": "", "ref": ""}
    if fragment:
        parts = fragment.split("/")
        result["ref"] = parts[0]
        result["path"] = "/".join(parts[1:])
    return result


def github_url(repo: str, ref: str, path: str, *, directory: bool = False) -> str:
    branch = urllib.parse.quote(ref, safe="")
    clean_path = urllib.parse.quote(path, safe="/")
    return f"https://github.com/{repo}/{'tree' if directory else 'blob'}/{branch}/{clean_path}"


def github_api(repo: str, suffix: str) -> str:
    return "https://api.github.com/repos/" + repo + suffix


def source_tree(client: HTTP, repo: str) -> tuple[dict, str, list[dict], bool]:
    meta = client.json(github_api(repo, ""))
    ref = meta["default_branch"]
    commit = client.json(github_api(repo, "/commits/" + urllib.parse.quote(ref, safe="")))
    sha = commit["sha"]
    tree = client.json(github_api(repo, "/git/trees/" + sha + "?recursive=1"))
    return meta, sha, tree.get("tree", []), bool(tree.get("truncated", False))


def discover_roots(provider: str, files: list[dict]) -> list[str]:
    paths = {x["path"] for x in files if x.get("type") == "blob"}
    roots: set[str] = set()
    if provider == "cloudflare":
        for path in paths:
            parts = path.split("/")
            if len(parts) == 2 and parts[0] not in {"node_modules", "scripts", "docs", "test", "tests"} and not parts[0].startswith(".") and parts[1] in (DOCS | MANIFEST_FILES):
                roots.add(parts[0])
    else:
        # Vercel examples repository is a monorepo of examples grouped by category.
        # A directory must contain its own README plus a recognized build manifest.
        docs = {p.rsplit("/", 1)[0] for p in paths if p.rsplit("/", 1)[-1] in DOCS and "/" in p}
        manifests = {p.rsplit("/", 1)[0] for p in paths if p.rsplit("/", 1)[-1] in {"package.json", "pyproject.toml", "requirements.txt", "Cargo.toml", "go.mod"} and "/" in p}
        roots = {p for p in (docs & manifests) if len(p.split("/")) >= 2 and not any(seg.startswith(".") or seg in {"node_modules", "__fixtures__", "test", "tests", "fixtures", "packages"} for seg in p.split("/"))}
    return sorted(roots)


def extract_jsonc(s: str) -> dict:
    # Restrict JSONC parsing to safe comment removal with quote awareness.
    chars: list[str] = []
    i, string, escape = 0, False, False
    while i < len(s):
        c = s[i]
        if string:
            chars.append(c)
            if c == '"' and not escape:
                string = False
            if c == "\\" and not escape:
                escape = True
            else:
                escape = False
            i += 1
            continue
        if c == '"':
            string = True
            chars.append(c)
            i += 1
            continue
        if s[i:i+2] == "//":
            i = s.find("\n", i)
            if i == -1: break
            continue
        if s[i:i+2] == "/*":
            j = s.find("*/", i+2)
            if j == -1: break
            i = j+2
            continue
        chars.append(c)
        i += 1
    text = re.sub(r",\s*([}\]])", r"\1", "".join(chars))
    return json.loads(text)


def fetch_file(client: HTTP, repo: str, ref: str, path: str, max_chars: int = 180_000) -> str | None:
    url = github_api(repo, "/contents/" + urllib.parse.quote(path, safe="/") + "?ref=" + urllib.parse.quote(ref, safe=""))
    try:
        resp = client.json(url)
        if resp.get("type") != "file" or resp.get("size", 0) > max_chars:
            return None
        if resp.get("encoding") != "base64":
            return None
        return base64.b64decode(resp["content"]).decode("utf-8", "replace")[:max_chars]
    except (RuntimeError, ValueError, KeyError):
        return None


def name_words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z][a-z0-9-]{1,}", s.lower()) if w not in {"with", "from", "this", "that", "template", "example", "starter"}}


def enrich(record: dict, client: HTTP) -> None:
    repo, commit, root = record["source"]["repository"], record["source"]["commit"], record["source"]["path"]
    files = {f["path"].rsplit("/", 1)[-1]: f["path"] for f in record["inventory"]["files"] if f["path"].rsplit("/", 1)[0] == root}
    pkg_text = None
    for filename in ("package.json", "pyproject.toml", "requirements.txt", "wrangler.jsonc", "wrangler.toml", "vercel.json"):
        if filename not in files: continue
        content = fetch_file(client, repo, commit, files[filename])
        if not content: continue
        record["provenance"]["inspected_files"].append(files[filename])
        if filename == "package.json":
            try:
                pkg = json.loads(content)
                dependencies = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                record["stack"]["dependencies"] = dict(sorted(dependencies.items()))
                record["commands"] = pkg.get("scripts", {})
                record["stack"]["package_manager"] = pkg.get("packageManager", "unknown")
                pkg_text = content.lower()
                if record["provider"] == "cloudflare" and isinstance(pkg.get("cloudflare"), dict):
                    cfmeta = pkg["cloudflare"]
                    record["platform_metadata"].update({k: cfmeta[k] for k in ("label", "products", "categories", "publish") if k in cfmeta})
                    record["stack"]["products"] = sorted(set(record["stack"]["products"] + ["cloudflare-" + slug(str(x)) for x in cfmeta.get("products", [])]))
                if isinstance(pkg.get("description"), str) and pkg["description"].strip():
                    record["description"] = pkg["description"].strip()
            except (ValueError, TypeError):
                record["warnings"].append("package.json could not be parsed")
        elif filename == "wrangler.jsonc":
            try:
                cfg = extract_jsonc(content)
                record["stack"]["bindings"] = sorted(k for k in ("d1_databases", "r2_buckets", "kv_namespaces", "durable_objects", "ai", "queues", "vectorize", "workflows") if k in cfg)
            except (ValueError, TypeError):
                record["warnings"].append("wrangler.jsonc could not be parsed")
        elif filename == "vercel.json":
            try:
                cfg = json.loads(content)
                record["stack"]["runtime_config"] = sorted(cfg.keys())
            except ValueError:
                record["warnings"].append("vercel.json could not be parsed")
        elif filename == "pyproject.toml":
            record["stack"]["ecosystems"].append("python")
        elif filename == "requirements.txt":
            record["stack"]["ecosystems"].append("python")
    readme_path = next((files[x] for x in DOCS if x in files), None)
    if readme_path:
        readme = fetch_file(client, repo, commit, readme_path, max_chars=120_000)
        if readme:
            record["provenance"]["inspected_files"].append(readme_path)
            paragraphs = [x.strip() for x in re.split(r"\n\s*\n", readme) if x.strip() and not x.startswith("[")]
            if paragraphs:
                record["readme"]["excerpt"] = re.sub(r"[`*_#<>]", "", paragraphs[0])[:650]
            evidence = (readme[:35000] + " " + (pkg_text or "")).lower()
            record["features"] = sorted(k for k, patterns in FEATURE_LEXICON.items() if any(p in evidence for p in patterns))
            record["provenance"]["feature_basis"] = "keyword_inference_from_readme_and_package"
    deps = " ".join(record["stack"]["dependencies"].keys()).lower() + " " + " ".join(record["stack"].get("bindings", [])) + " " + (pkg_text or "")[:12000]
    record["stack"]["products"] = sorted(set(record["stack"]["products"]) | {k for k, patterns in PRODUCT_MAP.items() if any(p in deps for p in patterns)})
    frameworks = ["astro", "next", "react", "vue", "svelte", "hono", "vite", "nuxt", "fastapi", "express", "drizzle-orm", "prisma"]
    dep_names = record["stack"]["dependencies"].keys()
    record["stack"]["frameworks"] = sorted(x for x in frameworks if x in dep_names or f"@{x}/" in deps or (x == "next" and "next" in dep_names))
    record["tags"] = sorted(set(record["features"] + record["stack"]["products"] + record["stack"]["frameworks"] + [record["provider"]]))
    record["status"] = "enriched" if record["provenance"]["inspected_files"] else "reference_only"


def repo_records(provider: str, repo: str, commit: str, tree: list[dict], truncated: bool, *, limit: int | None = None) -> list[dict]:
    roots = discover_roots(provider, tree)
    if limit is not None:
        roots = roots[:limit]
    out = []
    for root in roots:
        members = [x for x in tree if x.get("path", "").startswith(root + "/") and x.get("type") == "blob"]
        prefix = root + "/"
        names = {x["path"][len(prefix):] for x in members}
        langs = sorted({LANGUAGE_EXTS[Path(x["path"]).suffix.lower()] for x in members if Path(x["path"]).suffix.lower() in LANGUAGE_EXTS})
        readme_path = next((prefix + d for d in sorted(DOCS) if d in names), None)
        title = root.rsplit("/", 1)[-1].replace("-", " ").title()
        id_ = f"{provider}:{slug(repo)}:{slug(root)}"
        metadata = {x: prefix + x for x in sorted(MANIFEST_FILES) if x in names}
        out.append({
            "schema_version": MANIFEST_VERSION, "id": id_, "provider": provider, "title": title,
            "description": "Unverified: inspect linked README and source files", "catalog_url": ("https://developers.cloudflare.com/workers/get-started/quickstarts/" if provider == "cloudflare" else "https://vercel.com/templates"),
            "source": {"repository": repo, "path": root, "commit": commit, "repository_url": "https://github.com/" + repo, "source_url": github_url(repo, commit, root, directory=True)},
            "readme": {"path": readme_path, "url": github_url(repo, commit, readme_path) if readme_path else None, "excerpt": None},
            "inventory": {"complete": not truncated, "file_count": len(members), "files": [{"path": m["path"], "sha": m.get("sha"), "size": m.get("size"), "url": github_url(repo, commit, m["path"])} for m in members], "metadata_paths": metadata},
            "stack": {"languages": langs, "frameworks": [], "dependencies": {}, "package_manager": "unknown", "products": [], "bindings": [], "ecosystems": [], "runtime_config": []},
            "commands": {}, "features": [], "tags": [provider], "platform_metadata": {},
            "license": {"status": "needs_review", "file_path": metadata.get("LICENSE") or metadata.get("LICENSE.md")},
            "provenance": {"origin": "github_official_repository", "source_ref": commit, "inspected_files": [], "feature_basis": "not_inspected"},
            "status": "reference_only", "warnings": (["GitHub tree truncated; inventory incomplete"] if truncated else []),
        })
    return out


def vercel_gallery_record(page_url: str, html: str) -> dict | None:
    p = GalleryParser()
    p.feed(html)
    # Prefer a repository link from the template page, not a generic GitHub landing page.
    linked = [(repo_info(url), anchor) for url, anchor in p.links if url.startswith("https://github.com/")]
    linked = [(r, a) for r, a in linked if r and r["repo"] not in {"vercel/vercel"}]
    if not linked:
        return None
    label = None
    for i, word in enumerate(p.words):
        if word.lower() == "repository" and i + 1 < len(p.words):
            label = p.words[i + 1].strip().lower()
            break
    src = next((r for r, a in linked if label and a.lower() == label), None)
    if src is None:
        src = next((r for r, a in linked if not r["repo"].startswith("vercel/") and a.lower() not in {"github", "source", "open source"}), None)
    if src is None:
        src = next((r for r, a in linked if "repository" in a.lower()), linked[0][0])
    clean_path = urllib.parse.urlsplit(page_url).path
    name = clean_path.rsplit("/", 1)[-1].replace("-", " ").title()
    return {"page": page_url, "title": name, "description": p.meta.get("description", ""), "repo": src["repo"], "path": src["path"], "ref": src["ref"], "status": "gallery_discovered"}


def sitemap_urls(client: HTTP, url: str, *, max_sitemaps: int = 20, max_urls: int = 50_000) -> list[str]:
    pending = [url]
    seen: set[str] = set()
    results: set[str] = set()
    while pending and len(seen) < max_sitemaps and len(results) < max_urls:
        current = pending.pop(0)
        if current in seen: continue
        seen.add(current)
        try:
            xml = ET.fromstring(client.get(current))
        except (ET.ParseError, RuntimeError, ValueError):
            continue
        for loc in xml.iter():
            if not loc.tag.endswith("loc") or not loc.text:
                continue
            sub = loc.text.strip()
            if sub.endswith(".xml") and sub.startswith("https://vercel.com/"):
                pending.append(sub)
            elif sub.startswith("https://vercel.com/templates/") and re.fullmatch(r"/templates/[a-z0-9.\-]+/[a-z0-9.\-]+/?", urllib.parse.urlsplit(sub).path):
                results.add(sub.rstrip("/"))
                if len(results) >= max_urls: break
    return sorted(results)


def index_command(args: argparse.Namespace) -> None:
    root = Path(args.output).resolve()
    source = read_json(Path(args.sources), {})
    client = HTTP(root / ".cache" / "http", offline=args.offline, no_cache=args.refresh, pause=args.pause)
    previous = read_json(root / "catalog" / "index.json", {})
    prev_by_id = {entry["id"]: entry for entry in previous.get("templates", [])}
    records: list[dict] = []
    outcomes = []
    for src in source.get("github_sources", []):
        provider, repo = src["provider"], src["repo"]
        try:
            _meta, commit, files, truncated = source_tree(client, repo)
            all_ = repo_records(provider, repo, commit, files, truncated, limit=args.max_templates)
            # The Cloudflare repository's own templates.json gives the curated
            # template set; not every directory in the monorepo is a template.
            if repo == "cloudflare/templates":
                curated = fetch_file(client, repo, commit, "templates.json")
                if curated:
                    try:
                        listed = set(json.loads(curated).get("templates", {}))
                        for r in all_:
                            r["platform_metadata"]["listed_in_templates_json"] = r["source"]["path"] in listed
                            if r["source"]["path"] not in listed:
                                r["warnings"].append("Directory is not in official templates.json")
                    except (ValueError, TypeError):
                        outcomes.append({"provider": provider, "source": "templates.json", "state": "invalid_json"})
            for i, record in enumerate(all_):
                path = root / "catalog" / "templates" / provider / (slug(record["source"]["path"]) + ".json")
                old = read_json(path)
                if old and old.get("source", {}).get("commit") == commit and not args.refresh:
                    record = old
                    if old.get("status") != "enriched" and args.max_enrich != 0 and i < args.max_enrich:
                        enrich(record, client)
                elif args.max_enrich != 0 and i < args.max_enrich:
                    enrich(record, client)
                put_json(path, record)
                records.append(record)
            outcomes.append({"provider": provider, "repo": repo, "state": "partial" if truncated or args.max_templates is not None else "tree_complete", "found": len(all_), "commit": commit})
        except (ValueError, RuntimeError, KeyError) as exc:
            outcomes.append({"provider": provider, "repo": repo, "state": "error", "reason": str(exc)})
    # Secondary source: public Vercel gallery. It is not equivalent to the whole gallery
    # unless the site offers an exhaustive and current public sitemap.
    if args.gallery:
        gallery_urls: set[str] = set()
        for category in source.get("vercel_categories", []):
            try:
                gallery_urls.update(gallery_links(client.get(category).decode("utf-8", "replace"), category))
            except (RuntimeError, ValueError) as exc:
                outcomes.append({"provider": "vercel-gallery", "source": category, "state": "error", "reason": str(exc)})
        for sm in source.get("vercel_sitemaps", []):
            gallery_urls.update(sitemap_urls(client, sm))
        seen_gallery = []
        for url in sorted(gallery_urls)[: args.max_pages]:
            try:
                item = vercel_gallery_record(url, client.get(url).decode("utf-8", "replace"))
                if item: seen_gallery.append(item)
            except (RuntimeError, ValueError) as exc:
                outcomes.append({"provider": "vercel-gallery", "source": url, "state": "error", "reason": str(exc)})
        put_json(root / "catalog" / "vercel_gallery_links.json", {"discovered": len(gallery_urls), "inspected": len(seen_gallery), "gallery_coverage": "partial_or_unverified", "items": seen_gallery})
        # Gallery refs outside vercel/examples are preserved even when the source repo
        # has not yet been independently inspected.
        for item in seen_gallery:
            matching = next((r for r in records if r["source"]["repository"] == item["repo"] and r["source"]["path"] == item["path"]), None)
            if matching:
                matching["catalog_url"] = item["page"]
                put_json(root / "catalog" / "templates" / matching["provider"] / (slug(matching["source"]["path"]) + ".json"), matching)
                continue
            uid = "vercel:gallery:" + slug(item["page"].split("/templates/")[-1])
            path = root / "catalog" / "gallery" / (slug(urllib.parse.urlsplit(item["page"]).path) + ".json")
            rec = {"schema_version": MANIFEST_VERSION, "id": uid, "provider": "vercel", "title": item["title"], "description": item["description"], "catalog_url": item["page"], "source": {"repository": item["repo"], "path": item["path"], "commit": None, "repository_url": "https://github.com/" + item["repo"], "source_url": "https://github.com/" + item["repo"]}, "readme": {"path": None, "url": None, "excerpt": None}, "inventory": {"complete": False, "file_count": 0, "files": [], "metadata_paths": {}}, "stack": {"languages": [], "frameworks": [], "dependencies": {}, "package_manager": "unknown", "products": [], "bindings": [], "ecosystems": [], "runtime_config": []}, "commands": {}, "features": [], "tags": ["vercel"], "license": {"status": "needs_review", "file_path": None}, "provenance": {"origin": "vercel_public_gallery", "source_ref": None, "inspected_files": [], "feature_basis": "not_inspected"}, "status": "discovered_unverified", "platform_metadata": {}, "warnings": ["Full GitHub tree not inspected; do not import until resolved"]}
            put_json(path, rec)
            records.append(rec)
        outcomes.append({"provider": "vercel-gallery", "state": "discovery_non_exhaustive", "discovered_pages": len(gallery_urls), "resolved_pages": len(seen_gallery)})
    # Preserve prior snapshot if network temporarily fails, but mark its provenance as stale.
    if not records and prev_by_id:
        raise RuntimeError("No sources could be indexed; preserving previous index without claiming a fresh run")
    summaries = []
    for r in records:
        summaries.append({"id": r["id"], "provider": r["provider"], "title": r["title"], "description": r["description"], "catalog_url": r["catalog_url"], "repository": r["source"]["repository"], "path": r["source"]["path"], "commit": r["source"]["commit"], "source_url": r["source"]["source_url"], "stack": {"languages": r["stack"]["languages"], "frameworks": r["stack"]["frameworks"], "products": r["stack"]["products"]}, "features": r["features"], "tags": r["tags"], "platform_metadata": r.get("platform_metadata", {}), "status": r["status"], "complete": r["inventory"]["complete"]})
    summaries.sort(key=lambda x: x["id"])
    put_json(root / "catalog" / "index.json", {"schema_version": MANIFEST_VERSION, "scope": "public_reference_index", "coverage": "partial_or_unverified", "source_status": outcomes, "template_count": len(summaries), "templates": summaries})
    csv_path = root / "catalog" / "master_index.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "provider", "title", "repository", "root_path", "commit", "languages", "frameworks", "products", "features", "tags", "status", "source_url", "catalog_url"])
        for x in summaries:
            w.writerow([x["id"], x["provider"], x["title"], x["repository"], x["path"], x["commit"], ";".join(x["stack"]["languages"]), ";".join(x["stack"]["frameworks"]), ";".join(x["stack"]["products"]), ";".join(x["features"]), ";".join(x["tags"]), x["status"], x["source_url"], x["catalog_url"]])
    print(json.dumps({"indexed": len(summaries), "sources": outcomes, "http": client.stats}, ensure_ascii=False, indent=2))


def ranked(index: dict, query: str, provider: str = "all", limit: int = 10) -> list[dict]:
    wanted = name_words(query)
    hits = []
    for item in index.get("templates", []):
        if provider != "all" and item["provider"] != provider:
            continue
        title = name_words(item["title"])
        tags = name_words(" ".join(item.get("tags", [])))
        features = name_words(" ".join(item.get("features", [])))
        paths = name_words(item.get("path", ""))
        frameworks = name_words(" ".join(item.get("stack", {}).get("frameworks", [])))
        score = 5*len(wanted & title) + 4*len(wanted & tags) + 3*len(wanted & features) + 2*len(wanted & paths) + len(wanted & frameworks)
        if score > 0:
            hits.append({"score": score, **item})
    return sorted(hits, key=lambda x: (-x["score"], x["id"]))[:limit]


def search_command(args: argparse.Namespace) -> None:
    index = read_json(Path(args.output) / "catalog" / "index.json", {})
    hits = ranked(index, args.query, args.provider, args.limit)
    print(json.dumps({"query": args.query, "count": len(hits), "results": hits}, ensure_ascii=False, indent=2))


def plan_command(args: argparse.Namespace) -> None:
    index = read_json(Path(args.output) / "catalog" / "index.json", {})
    hits = ranked(index, args.query, args.provider, args.limit)
    plan = {"schema_version": MANIFEST_VERSION, "status": "proposal_only", "request": args.query, "strategy": "reference_first_selective_reuse", "candidates": [{"id": r["id"], "score": r["score"], "source_url": r["source_url"], "commit": r["commit"], "reason": "deterministic lexical match; manual fit check required", "validation": {"license": "pending", "security": "pending", "dependency_compatibility": "pending", "integration_tests": "pending"}} for r in hits], "gates": ["G0 specification and boundaries approved", "G1 repository, commit, license and provenance verified", "G2 dependency, runtime and platform compatibility checked", "G3 select smallest useful files or template; no bulk import", "G4 tests fail red on required behavior before integration", "G5 isolated integration and security checks pass", "G6 owner approves deployment and secrets"]}
    path = Path(args.output) / "catalog" / "selection_plan.json"
    put_json(path, plan)
    print(json.dumps({"path": str(path), "candidates": len(hits), "status": plan["status"]}, indent=2))


def validate_command(args: argparse.Namespace) -> None:
    base = Path(args.output)
    index = read_json(base / "catalog" / "index.json", {})
    issues = []
    ids = set()
    for item in index.get("templates", []):
        if item.get("id") in ids: issues.append("Duplicate id: " + str(item.get("id")))
        ids.add(item.get("id"))
        if item.get("complete") and not item.get("commit"): issues.append("False completeness: " + item.get("id", "?"))
        if item.get("status") in {"enriched", "reference_only"} and not item.get("commit"): issues.append("Missing commit: " + item.get("id", "?"))
        if item.get("source_url", "").startswith("https://dash.cloudflare.com/"): issues.append("Leaked dashboard URL in " + item.get("id", "?"))
    if len(index.get("templates", [])) != index.get("template_count", 0): issues.append("template_count mismatch")
    # File-level path + provenance checks across all saved template manifests.
    for path in list((base / "catalog" / "templates").glob("**/*.json")) + list((base / "catalog" / "gallery").glob("*.json")):
        doc = read_json(path, {})
        src = doc.get("source", {})
        if doc.get("inventory", {}).get("complete") and not src.get("commit"): issues.append(f"{path}: complete without commit")
        for item in doc.get("inventory", {}).get("files", []):
            if not item.get("path", "").startswith(src.get("path", "") + "/"):
                issues.append(f"{path}: file outside template root")
    result = {"valid": not issues, "templates": len(ids), "issues": issues}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if issues: sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Manus LEGO reference-only template indexing and selection")
    parser.add_argument("--output", default=str(ROOT), help="Repository root")
    sub = parser.add_subparsers(dest="cmd", required=True)
    ix = sub.add_parser("index", help="Discover public template refs, inspect GitHub tree, and build manifests")
    ix.add_argument("--sources", default=str(ROOT / "catalog" / "sources.json"))
    ix.add_argument("--offline", action="store_true")
    ix.add_argument("--refresh", action="store_true")
    ix.add_argument("--pause", type=float, default=0.1)
    ix.add_argument("--max-enrich", type=int, default=25, help="Max metadata/README enrichments per source; 0 = tree-only")
    ix.add_argument("--max-templates", type=int, default=None)
    ix.add_argument("--gallery", action="store_true", help="Discover public Vercel gallery; always report partial coverage")
    ix.add_argument("--max-pages", type=int, default=100, help="Limit public template detail-page fetches")
    ix.set_defaults(func=index_command)
    search = sub.add_parser("search", help="Search indexed templates without reading source code")
    search.add_argument("query")
    search.add_argument("--provider", choices=["all", "cloudflare", "vercel"], default="all")
    search.add_argument("--limit", type=int, default=10)
    search.set_defaults(func=search_command)
    plan = sub.add_parser("plan", help="Create read-only LEGO composition plan")
    plan.add_argument("query")
    plan.add_argument("--provider", choices=["all", "cloudflare", "vercel"], default="all")
    plan.add_argument("--limit", type=int, default=5)
    plan.set_defaults(func=plan_command)
    valid = sub.add_parser("validate", help="Check manifest consistency and provenance")
    valid.set_defaults(func=validate_command)
    args = parser.parse_args()
    if args.cmd == "index":
        if args.max_enrich < 0 or args.max_pages < 0 or (args.max_templates is not None and args.max_templates < 0):
            parser.error("Limits must be non-negative")
    args.func(args)


if __name__ == "__main__":
    main()
