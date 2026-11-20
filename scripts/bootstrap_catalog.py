#!/usr/bin/env python3
"""Generate an explicit discovery-only seed from verified, public source listings.

This is NOT a live refresh and does NOT assert source commit or file-tree coverage.
"""
from __future__ import annotations
import csv
import json
from pathlib import Path
from lego_catalog import slug, put_json

BASE = Path(__file__).resolve().parents[1]
# Names verified in cloudflare/templates/templates.json via official GitHub source.
CLOUDFLARE = """agent-visibility-template
astro-blog-starter-template
chanfana-openapi-template
d1-template
durable-chat-template
llm-chat-app-template
multiplayer-globe-template
next-starter-template
openauth-template
r2-explorer-template
react-postgres-fullstack-template
react-router-hono-fullstack-template
react-router-starter-template
remix-starter-template
saas-admin-template
text-to-image-template
to-do-list-kv-template
vite-react-template
worker-publisher-template
containers-template
d1-starter-sessions-api-template
hello-world-do-template
mysql-hyperdrive-template
nlweb-template
nodejs-http-server-template
postgres-hyperdrive-template
react-router-postgres-ssr-template
x402-proxy-template
workflows-starter-template
workers-for-platforms-template
microfrontend-template
workers-builds-notifications-template
ai-brand-visibility-template
commerce-llms-txt-template
agent-commerce-analytics-template
react-starter-template
internal-sites-template
voice-agent-template
email-routing-template
email-sending-template
grpc-container-template""".splitlines()


def record(provider: str, repo: str, path: str, url: str, description: str = "") -> dict:
    return {
        "schema_version": "1.0.0", "id": f"{provider}:seed:{slug(path or url)}",
        "provider": provider, "title": (path or url.rsplit("/", 1)[-1]).replace("-", " ").title(),
        "description": description or "Directory name verified; technical attributes not yet inspected",
        "catalog_url": url if provider == "vercel" else "https://developers.cloudflare.com/workers/get-started/quickstarts/",
        "source": {"repository": repo, "path": path, "commit": None, "repository_url": f"https://github.com/{repo}", "source_url": f"https://github.com/{repo}/tree/main/{path}" if path else f"https://github.com/{repo}"},
        "readme": {"path": None, "url": None, "excerpt": None},
        "inventory": {"complete": False, "file_count": 0, "files": [], "metadata_paths": {}},
        "stack": {"languages": [], "frameworks": [], "dependencies": {}, "package_manager": "unknown", "products": [], "bindings": [], "ecosystems": [], "runtime_config": []},
        "commands": {}, "features": [], "tags": sorted(set([provider] + path.split("-"))),
        "platform_metadata": {"listed_in_templates_json": True} if provider == "cloudflare" else {},
        "license": {"status": "needs_review", "file_path": None},
        "provenance": {"origin": "cloudflare_templates_json" if provider == "cloudflare" else "vercel_public_gallery", "source_ref": "main (mutable; not pinned)" if provider == "cloudflare" else None, "inspected_files": [], "feature_basis": "not_inspected"},
        "status": "discovered_unverified", "warnings": ["Bootstrap discovery only; run live index to pin a commit and inspect files"],
    }


def main() -> None:
    items = [record("cloudflare", "cloudflare/templates", x, "") for x in CLOUDFLARE]
    items.append(record("vercel", "withastro/astro", "", "https://vercel.com/templates/astro/astro-blog", "An ultra-minimal personal site and blog built with Astro (Vercel gallery description)"))
    # Seed one directly inspected package with limited facts; runtime is unverified.
    astro = next(x for x in items if x["source"]["path"] == "astro-blog-starter-template")
    astro["description"] = "Build a personal website, blog, or portfolio with Astro."
    astro["stack"]["languages"] = ["TypeScript", "Astro"]
    astro["stack"]["frameworks"] = ["astro"]
    astro["stack"]["products"] = ["cloudflare-workers"]
    astro["stack"]["package_manager"] = "unknown"
    astro["commands"] = {"dev":"astro dev", "build":"astro build", "deploy":"wrangler deploy", "check":"astro build && tsc && wrangler deploy --dry-run"}
    astro["platform_metadata"].update({"label":"Astro Framework Starter", "products":["Workers"], "publish":True})
    astro["provenance"]["inspected_files"] = ["astro-blog-starter-template/package.json"]
    astro["provenance"]["feature_basis"] = "official_package_json_inspected"
    # Full source tree and pinned commit remain unavailable in this execution environment.
    items.sort(key=lambda x: x["id"])
    for item in items:
        dest = BASE / "catalog" / "templates" / item["provider"] / (slug(item["source"]["path"] or "vercel-astro-blog") + ".json")
        put_json(dest, item)
    summaries = [{"id": x["id"], "provider": x["provider"], "title": x["title"], "description": x["description"], "catalog_url": x["catalog_url"], "repository": x["source"]["repository"], "path": x["source"]["path"], "commit": None, "source_url": x["source"]["source_url"], "stack": {k: x["stack"][k] for k in ("languages", "frameworks", "products")}, "features": x["features"], "tags": x["tags"], "platform_metadata": x["platform_metadata"], "status": x["status"], "complete": False} for x in items]
    put_json(BASE / "catalog" / "index.json", {"schema_version": "1.0.0", "scope": "public_reference_index", "coverage": "bootstrap_discovery_only", "source_status": [
        {"provider": "cloudflare", "repo": "cloudflare/templates", "state": "official_templates_json_directory_names", "count": len(CLOUDFLARE), "commit": None},
        {"provider": "vercel", "repo": "withastro/astro", "state": "single_gallery_listing_inspected", "count": 1, "commit": None}], "template_count": len(summaries), "templates": summaries})
    with (BASE / "catalog" / "master_index.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "provider", "title", "repository", "root_path", "commit", "languages", "frameworks", "products", "features", "tags", "status", "source_url", "catalog_url"])
        for x in summaries:
            w.writerow([x["id"], x["provider"], x["title"], x["repository"], x["path"], "", ";".join(x["stack"]["languages"]), ";".join(x["stack"]["frameworks"]), ";".join(x["stack"]["products"]), "", ";".join(x["tags"]), x["status"], x["source_url"], x["catalog_url"]])
    print(json.dumps({"templates": len(items), "cloudflare": len(CLOUDFLARE), "vercel": 1, "coverage": "bootstrap_discovery_only"}, indent=2))

if __name__ == "__main__":
    main()
