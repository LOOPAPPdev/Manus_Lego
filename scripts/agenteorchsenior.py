#!/usr/bin/env python3
"""Manus LEGO deterministic pipeline entrypoint; no model/vendor dependency.

The user-facing /agenteorchsenior skill coordinates reasoning. This Python CLI
handles reproducible catalog operations and exposes machine-readable status.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'scripts' / 'lego_catalog.py'


def step(label: str, args: list[str]) -> None:
    print(json.dumps({'stage': label, 'state': 'running', 'command': args}, ensure_ascii=False), flush=True)
    result = subprocess.run([sys.executable, str(CATALOG), *args], cwd=ROOT, check=False)
    if result.returncode:
        raise SystemExit(result.returncode)
    print(json.dumps({'stage': label, 'state': 'passed'}, ensure_ascii=False), flush=True)


def index_has_unresolved_errors() -> bool:
    data = json.loads((ROOT / 'catalog' / 'index.json').read_text(encoding='utf-8'))
    return any(s.get('state') in {'error', 'invalid_json'} for s in data.get('source_status', []))


def main() -> None:
    p = argparse.ArgumentParser(description='Senior Agent Python bridge for Manus LEGO (read-only by default)')
    sub = p.add_subparsers(dest='command', required=True)
    inv = sub.add_parser('inventory', help='Refresh metadata references and validate the catalog')
    inv.add_argument('--max-enrich', type=int, default=30)
    inv.add_argument('--max-pages', type=int, default=100)
    inv.add_argument('--gallery', action='store_true', default=True)
    select = sub.add_parser('select', help='Search and create a source-only LEGO selection plan')
    select.add_argument('features', help='Natural-language requirements for a minimal template selection')
    select.add_argument('--limit', type=int, default=5)
    sub.add_parser('check', help='Run offline tests and validate the current catalog')
    all_ = sub.add_parser('pipeline', help='Check, refresh inventory, and prepare a selection plan')
    all_.add_argument('features')
    all_.add_argument('--max-enrich', type=int, default=30)
    all_.add_argument('--max-pages', type=int, default=100)
    opts = p.parse_args()
    try:
        if opts.command in {'check', 'pipeline'}:
            print(json.dumps({'stage': 'tests', 'state': 'running'}, ensure_ascii=False), flush=True)
            test = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], cwd=ROOT, check=False)
            if test.returncode: raise SystemExit(test.returncode)
            print(json.dumps({'stage': 'tests', 'state': 'passed'}, ensure_ascii=False), flush=True)
            step('validate', ['validate'])
        if opts.command in {'inventory', 'pipeline'}:
            step('inventory', ['index', '--gallery', '--max-enrich', str(opts.max_enrich), '--max-pages', str(opts.max_pages)])
            step('validate', ['validate'])
            if index_has_unresolved_errors():
                print(json.dumps({'stage': 'inventory', 'state': 'blocked', 'reason': 'One or more public sources failed. This run does not establish complete inventory coverage.'}, ensure_ascii=False), flush=True)
                raise SystemExit(2)
        if opts.command in {'select', 'pipeline'}:
            step('search', ['search', opts.features, '--limit', str(getattr(opts, 'limit', 5))])
            step('selection_plan', ['plan', opts.features, '--limit', str(getattr(opts, 'limit', 5))])
            print(json.dumps({'result': 'proposal_only', 'requires_agent': True, 'integration_permitted': False,
                'next': 'Use /agenteorchsenior and /lego to verify source, pinned SHA, licenses, compatibility and tests before integration.'}, ensure_ascii=False), flush=True)
    except FileNotFoundError as exc:
        print(json.dumps({'stage': 'prerequisite', 'state': 'blocked', 'reason': str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == '__main__':
    main()
