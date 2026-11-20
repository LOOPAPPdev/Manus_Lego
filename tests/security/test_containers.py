"""Container and runtime hardening.

SP 800-190 controls that are cheap to verify statically: pinned base images, non-root
users, health checks, a read-only root filesystem and dropped capabilities. These are
the controls a reviewer can re-check without running the image.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
DOCKER_DIR = ROOT / "infrastructure/docker"

DOCKERFILES = ["Dockerfile.api", "Dockerfile.orchestrator", "Dockerfile.rag", "Dockerfile.web"]


@pytest.fixture(scope="module", params=DOCKERFILES)
def dockerfile(request: pytest.FixtureRequest) -> tuple[str, str]:
    path = DOCKER_DIR / request.param
    assert path.is_file(), f"{path.relative_to(ROOT)} is required"
    return request.param, path.read_text(encoding="utf-8")


def _resolve_args(text: str) -> dict[str, str]:
    """Collect ARG defaults so `FROM ${BASE}` can be checked like a literal."""
    args: dict[str, str] = {}
    for match in re.finditer(r"^ARG\s+([A-Za-z_][A-Za-z0-9_]*)=(\S+)", text, re.MULTILINE):
        args[match.group(1)] = match.group(2)
    return args


def test_base_images_are_pinned_by_digest(dockerfile: tuple[str, str]) -> None:
    """REQ-PO-004 — a mutable tag makes the build non-reproducible and unverifiable."""
    name, text = dockerfile
    args = _resolve_args(text)
    froms = [
        re.sub(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}", lambda m: args.get(m.group(1), m.group(0)), image)
        for image in re.findall(r"^FROM\s+(\S+)", text, re.MULTILINE)
    ]
    assert froms, f"{name} has no FROM line"
    for image in froms:
        if image == "scratch":
            continue
        assert "@sha256:" in image, f"{name}: base image '{image}' is not pinned by digest"
        assert ":latest" not in image, f"{name}: ':latest' is forbidden"


def test_runs_as_non_root(dockerfile: tuple[str, str]) -> None:
    """REQ-PW-006 — a compromised process must not be able to write to the image."""
    name, text = dockerfile
    users = re.findall(r"^USER\s+(\S+)", text, re.MULTILINE)
    assert users, f"{name} never switches user"
    final = users[-1]
    assert final not in {"root", "0", "0:0"}, f"{name} runs as root"
    assert re.fullmatch(r"(?:[a-z_][a-z0-9_-]*|[1-9][0-9]{2,5})(?::\S+)?", final), f"{name}: unexpected USER '{final}'"


def test_declares_healthcheck_and_signal_handling(dockerfile: tuple[str, str]) -> None:
    """REQ-PO-004 — orchestrators need a health signal and graceful shutdown."""
    name, text = dockerfile
    assert "HEALTHCHECK" in text, f"{name} has no HEALTHCHECK"
    assert "STOPSIGNAL" in text or "SIGTERM" in text, f"{name} does not handle termination"


def test_builds_in_multiple_stages(dockerfile: tuple[str, str]) -> None:
    """REQ-PO-004 — build tooling must not ship in the runtime image."""
    name, text = dockerfile
    stages = re.findall(r"^FROM\s+\S+\s+AS\s+(\S+)", text, re.MULTILINE | re.IGNORECASE)
    assert len(stages) >= 1, f"{name} is a single-stage build"
    assert re.search(r"^COPY\s+--from=", text, re.MULTILINE), f"{name} does not copy from a build stage"


def test_compose_applies_runtime_hardening() -> None:
    """REQ-PW-006 — the local stack mirrors the production security posture."""
    path = DOCKER_DIR / "compose.yaml"
    assert path.is_file()
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    services = document["services"]
    assert {"api", "web", "rag-indexer"} <= set(services), set(services)

    long_running = {"api", "web"}
    assert long_running <= set(services), set(services)

    for name, service in services.items():
        assert service.get("read_only") is True, f"{name}: root filesystem must be read-only"
        assert "no-new-privileges:true" in (service.get("security_opt") or []), f"{name}: no-new-privileges"
        assert "ALL" in (service.get("cap_drop") or []), f"{name}: drop all capabilities"
        assert service.get("user"), f"{name}: explicit non-root user required"

    for name in long_running:
        service = services[name]
        assert service.get("healthcheck"), f"{name}: healthcheck required"
        assert service.get("restart") in {"unless-stopped", "on-failure"}, f"{name}: restart policy required"

    # A batch job must be opt-in and must not be restarted forever.
    for name in set(services) - long_running:
        service = services[name]
        assert service.get("profiles"), f"{name}: batch services must be profile-gated"
        assert service.get("restart") == "no", f"{name}: a batch job must not restart"


def test_no_privileged_or_host_network_escape_hatches() -> None:
    """REQ-PW-006 — privileged containers and host networking defeat the isolation."""
    text = (DOCKER_DIR / "compose.yaml").read_text(encoding="utf-8")
    assert "privileged: true" not in text
    assert "network_mode: host" not in text
    assert "/var/run/docker.sock" not in text
