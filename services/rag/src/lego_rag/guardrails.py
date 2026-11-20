"""Prompt-injection guardrails for retrieved content.

Retrieved documents are data. They are wrapped in an explicit untrusted block and
scanned for instruction-like patterns. Detection never mutates the corpus and never
silently drops content: findings are surfaced with the answer so a reviewer can see
that the source tried to steer the model.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

INJECTION_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "override_instructions",
        re.compile(r"ignore\s+(all\s+)?(previous|prior|above)\s+(instructions|rules|prompts?)", re.I),
    ),
    ("disregard_system", re.compile(r"disregard\s+(the\s+)?(system|developer)\s+(prompt|message|instructions)", re.I)),
    ("role_reassignment", re.compile(r"you\s+are\s+now\s+(a|an|the)\s+\w+", re.I)),
    (
        "prompt_exfiltration",
        re.compile(r"(reveal|print|show)\s+(me\s+)?(your\s+)?(system\s+prompt|hidden\s+instructions)", re.I),
    ),
    (
        "secret_exfiltration",
        re.compile(r"(send|post|upload|exfiltrate)\s+.*(token|secret|credential|api[_\s-]?key)", re.I),
    ),
    ("tool_invocation", re.compile(r"(call|invoke|execute)\s+(the\s+)?(tool|function|command)\s*[:(]", re.I)),
    ("concealment", re.compile(r"(do\s+not|don't|never)\s+(tell|inform|reveal\s+to)\s+the\s+user", re.I)),
    ("html_comment_instruction", re.compile(r"<!--\s*(ignore|system|instruction)", re.I)),
    (
        "encoded_payload",
        re.compile(r"[A-Za-z0-9+/]{120,}={0,2}"),
    ),
)

UNTRUSTED_CLOSE = "</untrusted>"


@dataclass(frozen=True, slots=True)
class Finding:
    rule: str
    excerpt: str

    def as_dict(self) -> dict[str, str]:
        return {"rule": self.rule, "excerpt": self.excerpt}


def scan(text: str, *, max_findings: int = 5) -> list[Finding]:
    findings: list[Finding] = []
    for rule, pattern in INJECTION_RULES:
        match = pattern.search(text)
        if match:
            start = max(0, match.start() - 40)
            excerpt = text[start : match.end() + 40].replace("\n", " ")
            findings.append(Finding(rule=rule, excerpt=excerpt[:240]))
            if len(findings) >= max_findings:
                break
    return findings


def wrap_untrusted(text: str, source: str) -> str:
    """Wrap retrieved text so the model can tell data from instructions.

    Any literal closing tag inside the content is neutralised, otherwise a
    document could break out of the block and impersonate the surrounding prompt.
    """

    safe_source = re.sub(r"[^A-Za-z0-9_./#-]", "", source)[:120]
    safe_text = text.replace(UNTRUSTED_CLOSE, "&lt;/untrusted&gt;")
    return f'<untrusted source="{safe_source}">\n{safe_text}\n</untrusted>'
