#!/usr/bin/env python3
"""Build the integrated Manus LEGO master index from existing catalog rows and scout reports."""
from __future__ import annotations

import csv
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CATALOG = BASE / "catalog"
REPORTS = BASE / "reports" / "scouts"
OUTPUT = CATALOG / "master_index.csv"

FIELDS = [
    "id", "record_type", "provider", "title", "repository", "root_path", "commit",
    "languages", "frameworks", "products", "features", "tags", "status", "coverage",
    "source_url", "catalog_url", "report_path", "evidence_basis", "limitations",
]

# The labels and URLs are the exact scout scopes launched in this task. No fields
# not evidenced by the reports are populated as repository/runtime facts.
SCOUTS = [
    ("01-cloudflare-templates", "cloudflare", "Cloudflare templates repository", "https://github.com/cloudflare/templates", "complete", "manifest/tree correspondence in one pinned public commit"),
    ("02-vercel-examples", "vercel", "Vercel examples repository", "https://github.com/vercel/examples", "partial", "public repository metadata and selected documentation paths"),
    ("03-vercel-ai", "vercel", "Vercel AI templates category", "https://vercel.com/templates/ai", "partial", "dynamic category snapshot and selected public repository links"),
    ("04-vercel-authentication", "vercel", "Vercel authentication templates category", "https://vercel.com/templates/authentication", "partial", "dynamic category snapshot and selected public repository links"),
    ("05-vercel-backend", "vercel", "Vercel backend templates category", "https://vercel.com/templates/backend", "partial", "dynamic category snapshot and selected public repository links"),
    ("06-vercel-ecommerce", "vercel", "Vercel ecommerce templates category", "https://vercel.com/templates/ecommerce", "partial", "dynamic category snapshot and selected public repository links"),
    ("07-vercel-saas", "vercel", "Vercel SaaS templates category", "https://vercel.com/templates/saas", "partial", "dynamic category snapshot and selected public repository links"),
    ("08-vercel-security", "vercel", "Vercel security templates category", "https://vercel.com/templates/security", "partial", "dynamic category snapshot and selected public repository links"),
    ("09-vercel-starter", "vercel", "Vercel starter templates category", "https://vercel.com/templates/starter", "partial", "dynamic category snapshot and selected public repository links"),
    ("10-vercel-sitemap", "vercel", "Vercel public sitemap", "https://vercel.com/sitemap.xml", "partial", "public sitemap discovery snapshot; not proof of marketplace completeness"),
    ("11-vercel-blog", "vercel", "Vercel blog templates category", "https://vercel.com/templates/blog", "partial", "dynamic category snapshot and selected public repository links"),
    ("12-vercel-cms", "vercel", "Vercel CMS templates category", "https://vercel.com/templates/cms", "partial", "dynamic category snapshot and selected public repository links"),
    ("13-vercel-cron", "vercel", "Vercel cron templates category", "https://vercel.com/templates/cron", "partial", "public category snapshot and selected repository links"),
    ("14-vercel-marketing-sites", "vercel", "Vercel marketing sites templates category", "https://vercel.com/templates/marketing-sites", "partial", "public category snapshot and selected repository links"),
    ("15-vercel-monorepos", "vercel", "Vercel monorepos templates category", "https://vercel.com/templates/monorepos", "partial", "public category snapshot and selected repository links"),
    ("16-cloudflare-home", "cloudflare", "Cloudflare official website", "https://www.cloudflare.com/", "partial", "official public product and platform pages"),
    ("17-cloudflare-developer-docs", "cloudflare", "Cloudflare Developer Docs", "https://developers.cloudflare.com/", "partial", "official documentation index and selected product/API pages"),
    ("18-cloudflare-api", "cloudflare", "Cloudflare API documentation", "https://developers.cloudflare.com/api/", "partial", "public API reference and selected endpoint documentation"),
    ("19-cloudflare-agents", "cloudflare", "Cloudflare Agents / Agents SDK", "https://developers.cloudflare.com/agents/", "partial", "official Agents documentation and public repository metadata"),
    ("20-cloudflare-mcp", "cloudflare", "Cloudflare Remote MCP documentation", "https://developers.cloudflare.com/agents/model-context-protocol/guides/remote-mcp-server/", "partial", "official MCP/OAuth documentation and public example repository"),
    ("21-cloudflare-workflows", "cloudflare", "Cloudflare Workflows documentation", "https://developers.cloudflare.com/workflows/", "partial", "official Workflows documentation, limits, examples and API reference"),
    ("22-cloudflare-services", "cloudflare", "Cloudflare Workers platform services", "https://developers.cloudflare.com/workers/", "partial", "selected official documentation for Workers platform services"),
    ("23-cloudflare-github-org", "cloudflare", "Cloudflare GitHub organization", "https://github.com/cloudflare", "partial", "public organization listing and selected repository metadata"),
    ("24-cloudflare-templates", "cloudflare", "Cloudflare templates repository — focused scout", "https://github.com/cloudflare/templates", "partial", "templates.json and public tree evidence with incomplete item-by-item hash comparison"),
    ("25-cloudflare-vibesdk", "cloudflare", "Cloudflare VibeSDK repository", "https://github.com/cloudflare/vibesdk", "partial", "pinned public commit, tree, README, package and license metadata"),
    ("26-cloudflare-os", "cloudflare", "Cloudflare OS repository", "https://github.com/cloudflare/cloudflare-os", "partial", "pinned public commit, tree, README, workspace and license metadata"),
    ("27-system-dynamics-course", "systemdynamics.org", "System Dynamics online course catalog", "https://systemdynamics.org/learning/online-course-catalog/", "partial", "public catalog page, selected products and dynamic Airtable link"),
    ("28-system-dynamics-home", "systemdynamics.org", "System Dynamics Society", "https://systemdynamics.org/", "partial", "official institutional and resource pages"),
    ("29-machinations-learn", "machinations.io", "Machinations learning resources", "https://machinations.io/learn", "partial", "public learning paths, docs, glossary and changelog"),
    ("30-scikit-learn-guide", "scikit-learn.org", "scikit-learn User Guide", "https://scikit-learn.org/stable/user_guide.html", "partial", "official stable documentation index and related API/examples pages"),
    ("31-google-colab", "Google", "Google Colab", "https://colab.research.google.com/", "partial", "public product entry and official FAQ; no runtime execution"),
    ("32-amazon-agents-book", "Amazon/Novatec", "Construindo Aplicações com Agentes de IA", "https://www.amazon.com.br/Construindo-Aplica%C3%A7%C3%B5es-com-Agentes-Implementa%C3%A7%C3%A3o/dp/8575229907/", "partial", "public Amazon and publisher metadata"),
    ("33-amazon-ai-engineering-book", "Amazon/O'Reilly", "AI Engineering", "https://www.amazon.com.br/AI-Engineering-Building-Applications-Foundation/dp/1098166302/", "partial", "public related publisher, author and repository metadata; Amazon page unavailable"),
    ("34-coursera-ai-engineer", "Coursera/IBM", "IBM AI Engineering Professional Certificate", "https://www.coursera.org/professional-certificates/ai-engineer", "partial", "public program page and IBM contextual source"),
    ("35-claude-vertex-rag", "Claude Academy/Anthropic", "Claude Academy — Multi-index RAG pipeline", "https://academy.claude.com/courses/claude-with-google-cloud-s-vertex-ai/a-multi-index-rag-pipeline", "partial", "public lesson/course pages and official Google/Anthropic documentation"),
    ("36-langchain-ecosystem", "LangChain", "LangChain official ecosystem", "https://docs.langchain.com", "partial", "official docs and selected public GitHub repositories with observed SHAs/licenses"),
]


def first_paragraph(report: Path) -> str:
    text = report.read_text(encoding="utf-8")
    # Prefer the first prose paragraph after a common conclusion/identification heading.
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line.startswith("## ")]
    for start in starts:
        block = []
        for line in lines[start + 1 :]:
            if line.startswith("## "):
                break
            if line.strip() and not line.startswith("-") and not line.startswith("["):
                block.append(line.strip())
            elif block and not line.strip():
                break
        if block:
            return " ".join(block)[:700]
    return ""


def main() -> None:
    legacy_path = CATALOG / "master_index.csv"
    with legacy_path.open(newline="", encoding="utf-8") as f:
        legacy = list(csv.DictReader(f))

    rows = []
    for old in legacy:
        row = {field: "" for field in FIELDS}
        row.update(old)
        row["record_type"] = "template_seed"
        row["coverage"] = "unverified"
        row["evidence_basis"] = "pre-existing catalog seed; not replaced by scout-level source evidence"
        row["limitations"] = "Existing seed record retained unchanged; per-template runtime and current source verification remain pending."
        rows.append(row)

    for source_id, provider, title, url, coverage, basis in SCOUTS:
        report = REPORTS / f"{source_id}.md"
        if not report.exists():
            raise SystemExit(f"Missing scout report: {report}")
        row = {field: "" for field in FIELDS}
        row.update({
            "id": f"scout:{source_id}",
            "record_type": "source_scout",
            "provider": provider,
            "title": title,
            "status": coverage,
            "coverage": coverage,
            "source_url": url,
            "report_path": str(report),
            "evidence_basis": basis,
            "limitations": "See linked scout report; source-level evidence is not runtime/build/deploy proof.",
            "tags": "scout;source-evidence;" + provider.lower().replace("/", ";"),
            "features": "source exploration;provenance;coverage classification",
        })
        rows.append(row)

    tmp = OUTPUT.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(OUTPUT)
    print(f"wrote {OUTPUT} rows={len(rows)} legacy={len(legacy)} scouts={len(SCOUTS)}")


if __name__ == "__main__":
    main()
