"""Typed configuration contracts and cross-file validation.

Every YAML file under ``config/`` and ``agents/registry.yaml`` is parsed with
``extra="forbid"`` so a typo fails closed instead of being silently ignored.
Cross-file rules (tool allowlists, approval coverage, gate references, agent
identity) are checked in :func:`validate_configuration`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from .paths import RepoPaths

STRICT = ConfigDict(extra="forbid", frozen=True)


class ConfigError(RuntimeError):
    """Raised when configuration is structurally or semantically invalid."""

    def __init__(self, problems: list[str]) -> None:
        self.problems = problems
        super().__init__("Invalid configuration:\n" + "\n".join(f"- {problem}" for problem in problems))


# --------------------------------------------------------------------------- #
# config/manus.yaml
# --------------------------------------------------------------------------- #
class ProjectConfig(BaseModel):
    model_config = STRICT
    id: str
    name: str
    owner: str
    repository: str
    default_branch: str


class RuntimeConfig(BaseModel):
    model_config = STRICT
    node: str
    python: str
    package_manager: str


class CatalogConfig(BaseModel):
    model_config = STRICT
    root: str
    index: str
    manifests: str
    coverage_label: str


class ApiConfig(BaseModel):
    model_config = STRICT
    port: int = Field(gt=0, le=65535)
    cors_origins: list[str]
    read_only: bool
    rate_limit_per_minute: int = Field(gt=0)


class WebConfig(BaseModel):
    model_config = STRICT
    port: int = Field(gt=0, le=65535)


class PathsConfig(BaseModel):
    model_config = STRICT
    requirements: str
    traceability: str
    evidence_dir: str
    agents: str
    team_schema: str
    security_policy: str


class GateConfig(BaseModel):
    model_config = STRICT
    id: Literal["G0", "G1", "G2", "G3", "G4", "G5", "G6"]
    name: str
    owner: str
    blocking: bool


class ManusConfig(BaseModel):
    model_config = STRICT
    schema_version: str
    project: ProjectConfig
    runtime: RuntimeConfig
    catalog: CatalogConfig
    api: ApiConfig
    web: WebConfig
    paths: PathsConfig
    commands: dict[str, str]
    gates: list[GateConfig]


# --------------------------------------------------------------------------- #
# config/security.yaml
# --------------------------------------------------------------------------- #
class Reference(BaseModel):
    model_config = STRICT
    id: str
    title: str
    url: str


class PolicyMeta(BaseModel):
    model_config = STRICT
    name: str
    owner: str
    approver: str
    review_cycle_days: int = Field(gt=0)
    references: list[Reference]


class Classification(BaseModel):
    model_config = STRICT
    levels: list[str]
    default: str


class SecretPattern(BaseModel):
    model_config = STRICT
    name: str
    regex: str


class SecretScan(BaseModel):
    model_config = STRICT
    enabled: bool
    patterns: list[SecretPattern]
    allowlist_paths: list[str]


class SecretsConfig(BaseModel):
    model_config = STRICT
    storage: str
    commit_forbidden: bool
    log_redaction: bool
    scan: SecretScan


class NetworkConfig(BaseModel):
    model_config = STRICT
    require_https: bool
    allowed_hosts: list[str]
    deny_private_ranges: bool
    max_response_bytes: int = Field(gt=0)
    request_timeout_seconds: int = Field(gt=0)


class ApprovalsConfig(BaseModel):
    model_config = STRICT
    approver: str
    required_for: list[str]
    evidence_dir: str


class AutonomyConfig(BaseModel):
    model_config = STRICT
    default_scope: str
    max_autonomous_scope: list[str]
    stop_conditions: list[str]


class PromptInjectionPolicy(BaseModel):
    model_config = STRICT
    treat_retrieved_content_as_untrusted: bool
    wrap_untrusted_context: bool
    require_citation: bool
    refuse_when_no_source: bool


class ToolUsePolicy(BaseModel):
    model_config = STRICT
    allowlist_enforced: bool
    least_privilege: bool
    max_tool_calls_per_task: int = Field(gt=0)


class AiDataPolicy(BaseModel):
    model_config = STRICT
    pii_in_logs: str
    embeddings_are_sensitive: bool
    private_corpora_in_git: str


class AiPolicy(BaseModel):
    model_config = STRICT
    prompt_injection: PromptInjectionPolicy
    tool_use: ToolUsePolicy
    data: AiDataPolicy


class ContainerPolicy(BaseModel):
    model_config = STRICT
    non_root_user: bool
    read_only_rootfs: bool
    no_new_privileges: bool
    pinned_base_images: bool
    forbid_latest_tag: bool
    healthcheck_required: bool


class SupplyChainPolicy(BaseModel):
    model_config = STRICT
    lockfiles_required: list[str]
    action_pinning: str
    sbom_format: str
    provenance: str
    dependency_review: bool


class SecurityPolicy(BaseModel):
    model_config = STRICT
    schema_version: str
    policy: PolicyMeta
    classification: Classification
    secrets: SecretsConfig
    network: NetworkConfig
    approvals: ApprovalsConfig
    autonomy: AutonomyConfig
    ai: AiPolicy
    containers: ContainerPolicy
    supply_chain: SupplyChainPolicy


# --------------------------------------------------------------------------- #
# config/TEAMSCHEMA.yaml
# --------------------------------------------------------------------------- #
class TeamIdentity(BaseModel):
    model_config = STRICT
    id: str
    name: str
    owner: str
    accountable: str
    approval_authority: str
    separation_of_duties: bool


class OrchestratorAutonomy(BaseModel):
    model_config = STRICT
    default: str
    max_autonomous_scope: list[str]


class Escalation(BaseModel):
    model_config = STRICT
    on_policy_violation: str
    on_missing_evidence: str
    on_ambiguous_requirement: str


class Orchestrator(BaseModel):
    model_config = STRICT
    command: str
    policy: str
    autonomy: OrchestratorAutonomy
    approval_required: list[str]
    escalation: Escalation


class Agent(BaseModel):
    model_config = STRICT
    id: str
    role: str
    description: str
    tools: list[str] = Field(min_length=1)
    writes: list[str] = Field(min_length=1)
    constraints: list[str]


class Execution(BaseModel):
    model_config = STRICT
    workflow: str
    traceability: bool
    evidence_required: bool
    max_parallel_agents: int = Field(gt=0, le=32)
    gates: list[str]
    require_independent_auditor: bool


class ToolSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)
    klass: str = Field(alias="class")
    risk: Literal["low", "medium", "high"]
    scope: str


class ToolPolicy(BaseModel):
    model_config = STRICT
    catalog: dict[str, ToolSpec]


class TeamSchema(BaseModel):
    model_config = STRICT
    schema_version: str
    team: TeamIdentity
    orchestrator: Orchestrator
    agents: list[Agent]
    execution: Execution
    tool_policy: ToolPolicy


# --------------------------------------------------------------------------- #
# config/sources.yaml
# --------------------------------------------------------------------------- #
class SourceLimitations(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class SourcePolicy(BaseModel):
    model_config = STRICT
    default_trust: str
    require_https: bool
    require_pinned_commit_for_reuse: bool
    execute_candidate_code: bool
    max_sources: int = Field(gt=0, le=100)


class ReviewedSource(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)
    id: str
    provider: str
    repository: str
    url: str
    trust: str
    license_posture: str
    reviewed_by: str
    reviewed_at: str
    role: str
    limitations: list[str] = Field(default_factory=list)


class RejectedSource(BaseModel):
    model_config = STRICT
    id: str
    reason: str


class SourcesConfig(BaseModel):
    model_config = STRICT
    schema_version: str
    policy: SourcePolicy
    sources: list[ReviewedSource]
    rejected_sources: list[RejectedSource]


# --------------------------------------------------------------------------- #
# agents/registry.yaml
# --------------------------------------------------------------------------- #
class AgentRuntime(BaseModel):
    model_config = STRICT
    id: str
    team_agent: str
    purpose: str
    prompt: str
    tools: list[str]
    outputs: list[str]
    approval_required: list[str]


class AgentsRegistry(BaseModel):
    model_config = STRICT
    schema_version: str
    orchestrator: str
    agents: list[AgentRuntime]


# --------------------------------------------------------------------------- #
# Loading and validation
# --------------------------------------------------------------------------- #
@dataclass(slots=True)
class ConfigBundle:
    manus: ManusConfig
    security: SecurityPolicy
    team: TeamSchema
    sources: SourcesConfig
    agents: AgentsRegistry
    problems: list[str] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not self.problems

    def require_valid(self) -> None:
        if self.problems:
            raise ConfigError(self.problems)


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ConfigError([f"Missing configuration file: {path}"])
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:  # pragma: no cover - malformed YAML is an operator error
        raise ConfigError([f"Invalid YAML in {path}: {exc}"]) from exc
    if not isinstance(loaded, dict):
        raise ConfigError([f"{path} must contain a YAML mapping"])
    return loaded


def _parse[T: BaseModel](model: type[T], path: Path) -> tuple[T | None, list[str]]:
    raw = _read_yaml(path)
    try:
        return model.model_validate(raw), []
    except ValidationError as exc:
        problems = [
            f"{path.name}: {'.'.join(str(part) for part in error['loc'])}: {error['msg']}" for error in exc.errors()
        ]
        return None, problems


def load_configuration(paths: RepoPaths) -> ConfigBundle:
    """Load every configuration file and return a bundle with accumulated problems."""

    problems: list[str] = []
    parsed: dict[str, Any] = {}

    for key, model, path in (
        ("manus", ManusConfig, paths.manus_config),
        ("security", SecurityPolicy, paths.security_policy),
        ("team", TeamSchema, paths.team_schema),
        ("sources", SourcesConfig, paths.sources_config),
        ("agents", AgentsRegistry, paths.agents_registry),
    ):
        try:
            value, file_problems = _parse(model, path)
        except ConfigError as exc:
            problems.extend(exc.problems)
            continue
        problems.extend(file_problems)
        if value is not None:
            parsed[key] = value

    if len(parsed) < 5:
        return ConfigBundle(
            manus=parsed.get("manus"),  # type: ignore[arg-type]
            security=parsed.get("security"),  # type: ignore[arg-type]
            team=parsed.get("team"),  # type: ignore[arg-type]
            sources=parsed.get("sources"),  # type: ignore[arg-type]
            agents=parsed.get("agents"),  # type: ignore[arg-type]
            problems=problems,
        )

    bundle = ConfigBundle(
        manus=parsed["manus"],
        security=parsed["security"],
        team=parsed["team"],
        sources=parsed["sources"],
        agents=parsed["agents"],
    )
    bundle.problems.extend(problems)
    bundle.problems.extend(validate_configuration(bundle, paths))
    return bundle


def validate_configuration(bundle: ConfigBundle, paths: RepoPaths) -> list[str]:
    """Cross-file rules. Returns a list of human-readable problems."""

    problems: list[str] = []
    team, security, manus, sources, agents = (
        bundle.team,
        bundle.security,
        bundle.manus,
        bundle.sources,
        bundle.agents,
    )

    # --- Identity and authority ---
    if team.team.owner != team.team.accountable:
        problems.append("TEAMSCHEMA: team.owner must equal team.accountable (single accountable orchestrator)")
    if team.team.owner not in {agent.id for agent in team.agents}:
        problems.append(f"TEAMSCHEMA: team.owner '{team.team.owner}' is not a declared agent")
    if team.team.approval_authority != security.approvals.approver:
        problems.append("TEAMSCHEMA: team.approval_authority must match security.approvals.approver")

    ids = [agent.id for agent in team.agents]
    if len(ids) != len(set(ids)):
        problems.append("TEAMSCHEMA: duplicate agent ids")

    # --- Policy path and approval coverage ---
    policy_path = paths.root / team.orchestrator.policy
    if not policy_path.is_file():
        problems.append(f"TEAMSCHEMA: orchestrator.policy does not exist: {team.orchestrator.policy}")

    missing_approvals = sorted(set(security.approvals.required_for) - set(team.orchestrator.approval_required))
    if missing_approvals:
        problems.append(
            "TEAMSCHEMA: orchestrator.approval_required is missing security-mandated approvals: "
            + ", ".join(missing_approvals)
        )

    # --- Autonomy cannot exceed the security ceiling ---
    exceeding = sorted(
        set(team.orchestrator.autonomy.max_autonomous_scope) - set(security.autonomy.max_autonomous_scope)
    )
    if exceeding:
        problems.append("TEAMSCHEMA: autonomy exceeds security policy ceiling: " + ", ".join(exceeding))

    # --- Tool allowlist ---
    allowlist = set(team.tool_policy.catalog)
    for agent in team.agents:
        unknown = sorted(set(agent.tools) - allowlist)
        if unknown:
            problems.append(
                f"TEAMSCHEMA: agent '{agent.id}' uses tools absent from tool_policy.catalog: {', '.join(unknown)}"
            )
        if agent.id == team.team.owner and "repo_write" in agent.tools:
            # The orchestrator coordinates; implementation belongs to the engineering agent.
            problems.append("TEAMSCHEMA: orchestrator must not hold repo_write (separation of duties)")

    # --- Gates referenced by execution must be declared ---
    declared_gates = {gate.id for gate in manus.gates}
    if set(team.execution.gates) != declared_gates:
        problems.append(
            "TEAMSCHEMA: execution.gates must match the gates declared in config/manus.yaml "
            f"(missing: {sorted(declared_gates - set(team.execution.gates))}, extra: {sorted(set(team.execution.gates) - declared_gates)})"
        )

    # --- Independent auditor ---
    if team.execution.require_independent_auditor:
        auditor = next((agent for agent in team.agents if agent.role == "independent_verification"), None)
        if auditor is None:
            problems.append(
                "TEAMSCHEMA: execution requires an independent auditor but no agent has role independent_verification"
            )
        elif "repo_write" in auditor.tools:
            problems.append("TEAMSCHEMA: the independent auditor must not hold repo_write")

    workflow_path = paths.root / team.execution.workflow
    if not workflow_path.is_file():
        problems.append(f"TEAMSCHEMA: execution.workflow does not exist: {team.execution.workflow}")

    # --- Agent registry consistency ---
    if agents.orchestrator != team.orchestrator.command:
        problems.append(
            f"agents/registry.yaml: orchestrator '{agents.orchestrator}' must match TEAMSCHEMA command '{team.orchestrator.command}'"
        )
    registry_ids = {agent.id for agent in agents.agents}
    if registry_ids != set(ids):
        problems.append(
            "agents/registry.yaml: agent ids must match TEAMSCHEMA exactly "
            f"(missing: {sorted(set(ids) - registry_ids)}, extra: {sorted(registry_ids - set(ids))})"
        )
    team_by_id = {agent.id: agent for agent in team.agents}
    for runtime_agent in agents.agents:
        spec = team_by_id.get(runtime_agent.id)
        if spec is None:
            continue
        if runtime_agent.team_agent != spec.id:
            problems.append(f"agents/registry.yaml: '{runtime_agent.id}' team_agent must reference its TEAMSCHEMA id")
        if set(runtime_agent.tools) != set(spec.tools):
            problems.append(f"agents/registry.yaml: '{runtime_agent.id}' tools must equal the TEAMSCHEMA tool set")
        prompt_path = paths.root / runtime_agent.prompt
        if not prompt_path.is_file():
            problems.append(
                f"agents/registry.yaml: prompt file missing for '{runtime_agent.id}': {runtime_agent.prompt}"
            )
        unapproved = sorted(set(runtime_agent.approval_required) - set(team.orchestrator.approval_required))
        if unapproved:
            problems.append(
                f"agents/registry.yaml: '{runtime_agent.id}' requires approvals not declared by the orchestrator: "
                + ", ".join(unapproved)
            )

    # --- Sources ---
    if len(sources.sources) > sources.policy.max_sources:
        problems.append("config/sources.yaml: more sources than policy.max_sources allows")
    for source in sources.sources:
        if sources.policy.require_https and not source.url.startswith("https://"):
            problems.append(f"config/sources.yaml: '{source.id}' must use https")
        if source.provider not in {"cloudflare", "vercel"}:
            problems.append(f"config/sources.yaml: '{source.id}' has unsupported provider '{source.provider}'")
    if sources.policy.execute_candidate_code:
        problems.append("config/sources.yaml: execute_candidate_code must remain false (AGENTS.md constraint)")

    # --- Security policy sanity ---
    if not security.secrets.commit_forbidden:
        problems.append("config/security.yaml: secrets.commit_forbidden must be true")
    if not security.network.require_https:
        problems.append("config/security.yaml: network.require_https must be true")
    if security.ai.tool_use.allowlist_enforced is False:
        problems.append("config/security.yaml: ai.tool_use.allowlist_enforced must be true")
    for pattern in security.secrets.scan.patterns:
        try:
            re.compile(pattern.regex)
        except re.error as exc:
            problems.append(f"config/security.yaml: invalid regex for '{pattern.name}': {exc}")

    return problems
