"""The read-only catalog API, exercised over HTTP against the built server.

The test starts the compiled artifact (`apps/api/dist/index.js`), not the TypeScript
source, so it also proves the build output runs on the target runtime.
"""

from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "apps/api/dist/index.js"

pytestmark = pytest.mark.integration


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


@pytest.fixture(scope="module")
def base_url(tmp_path_factory: pytest.TempPathFactory):
    if shutil.which("node") is None:
        pytest.skip("node is not installed")
    if not DIST.is_file():
        pytest.skip("apps/api/dist is not built; run `pnpm exec turbo run build`")

    port = _free_port()
    log = tmp_path_factory.mktemp("api") / "server.log"
    env = {
        **os.environ,
        "LEGO_API_PORT": str(port),
        "LEGO_API_HOST": "127.0.0.1",
        "LEGO_LOG_LEVEL": "error",
        "NODE_ENV": "test",
    }
    with log.open("wb") as handle:
        process = subprocess.Popen(
            ["node", str(DIST)],
            cwd=ROOT,
            env=env,
            stdout=handle,
            stderr=subprocess.STDOUT,
        )
    url = f"http://127.0.0.1:{port}"
    deadline = time.time() + 20
    try:
        while time.time() < deadline:
            if process.poll() is not None:
                break
            try:
                with urllib.request.urlopen(f"{url}/health", timeout=1) as response:
                    if response.status == 200:
                        break
            except (urllib.error.URLError, TimeoutError):
                time.sleep(0.15)
        else:
            process.kill()
            pytest.fail("the API did not become healthy in time")
        if process.poll() is not None:
            pytest.fail(f"the API exited during start-up: {log.read_text(errors='replace')[-2000:]}")
        yield url
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()


def _call(url: str, path: str, method: str = "GET") -> tuple[int, dict[str, str], bytes]:
    request = urllib.request.Request(f"{url}{path}", method=method)
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, dict(response.headers), response.read()
    except urllib.error.HTTPError as error:
        return error.code, dict(error.headers), error.read()


def test_health_reports_catalog_state(base_url: str) -> None:
    """REQ-PW-001 — the service exposes a typed health envelope for orchestrators."""
    status, _, body = _call(base_url, "/health")
    payload = json.loads(body)

    assert status == 200
    assert payload["data"]["status"] == "ok"
    assert payload["data"]["catalog_loaded"] is True
    assert payload["meta"]["request_id"]


def test_catalog_listing_is_paginated(base_url: str) -> None:
    """REQ-PW-001 — responses follow the shared envelope contract."""
    status, _, body = _call(base_url, "/api/v1/templates?limit=5&offset=0")
    payload = json.loads(body)

    assert status == 200
    data = payload["data"]
    assert len(data["items"]) == 5
    assert data["total"] >= 40
    assert data["limit"] == 5
    assert payload["meta"]["source"] == "catalog/index.json"


def test_invalid_pagination_is_rejected(base_url: str) -> None:
    """REQ-PW-003 — an out-of-range parameter is a client error, not a silent clamp."""
    status, _, body = _call(base_url, "/api/v1/templates?limit=101")
    payload = json.loads(body)

    assert status == 400
    assert payload["error"]["code"]
    assert payload["error"]["request_id"]


def test_unknown_template_returns_404_envelope(base_url: str) -> None:
    """REQ-PW-003 — missing resources are reported without leaking internals."""
    status, _, body = _call(base_url, "/api/v1/templates/cloudflare:does-not-exist")
    payload = json.loads(body)

    assert status == 404
    assert "does-not-exist" in payload["error"]["message"]
    assert "stack" not in json.dumps(payload)


def test_write_methods_are_refused(base_url: str) -> None:
    """REQ-PW-006 — the service is read-only by construction."""
    status, _, body = _call(base_url, "/api/v1/templates", method="POST")
    payload = json.loads(body)

    assert status == 400
    assert payload["error"]["details"]["allowed"] == ["GET", "HEAD", "OPTIONS"]


def test_hardening_headers_are_present(base_url: str) -> None:
    """REQ-PW-006 — every response carries the browser-side hardening headers."""
    _, headers, _ = _call(base_url, "/health")
    lowered = {key.lower(): value for key, value in headers.items()}

    assert lowered["x-content-type-options"] == "nosniff"
    assert lowered["x-frame-options"] == "DENY"
    assert lowered["referrer-policy"] == "no-referrer"
    assert "default-src 'none'" in lowered["content-security-policy"]
    assert "x-ratelimit-limit" in lowered


def test_governance_endpoints_expose_gate_state(base_url: str) -> None:
    """REQ-PW-005 — gates are served from evidence, with an explicit status per gate."""
    status, _, body = _call(base_url, "/api/v1/gates")
    payload = json.loads(body)

    assert status == 200
    data = payload["data"]
    if not data["available"]:
        # No gate report yet: the API must say so instead of inventing a status.
        assert data["report"] is None
        assert "lego verify" in data["hint"]
        return

    gates = data["report"]["gates"]
    assert len(gates) == 7
    assert {gate["id"] for gate in gates} == {f"G{index}" for index in range(7)}
    for gate in gates:
        assert gate["status"] in {"pass", "fail", "blocked", "not_evaluated"}
