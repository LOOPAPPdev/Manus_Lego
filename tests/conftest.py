"""Shared test bootstrap.

The repository is a polyglot monorepo: Python lives in two independent services that
are not installed into a single environment by default. `pytest.ini` declares the
``pythonpath`` entries, and this conftest repeats the setup so the suites also run
when invoked from a service directory (CI does both).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for _relative in ("services/orchestrator/src", "services/rag/src"):
    _entry = str(ROOT / _relative)
    if _entry not in sys.path:
        sys.path.insert(0, _entry)
