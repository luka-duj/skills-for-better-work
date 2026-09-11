#!/usr/bin/env python3
"""Dependency-free validation for the Skills for Better Work repository."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = ROOT
PACK_PATH = ROOT / "pack.json"
SKILLS_ROOT = ROOT / "skills"
SKILL = ROOT / "skills" / "process-before-platform"
SCHEMA_PATH = SKILL / "schemas" / "initiative-request.schema.json"
EXAMPLE_PACKET = SKILL / "examples" / "synthetic-approval-portal" / "initiative-request.json"
EXAMPLE_MARKDOWN = SKILL / "examples" / "synthetic-approval-portal" / "initiative-request.md"
EVAL_CASES = ROOT / "evals" / "cases.json"
LOOP_EVAL_CASES = ROOT / "evals" / "loop-cases.json"
LOOP_EXAMPLE = ROOT / "examples" / "better-work-loop" / "synthetic-approval-portal"
LOOP_SCHEMA_PATH = SKILLS_ROOT / "better-work-loop" / "schemas" / "loop-state.schema.json"
SHAPE_SCHEMA_PATH = SKILLS_ROOT / "shape-the-slice" / "schemas" / "prototype-brief.schema.json"
BUILD_SCHEMA_PATH = SKILLS_ROOT / "build-the-slice" / "schemas" / "prototype-build.schema.json"
PROOF_SCHEMA_PATH = SKILLS_ROOT / "prove-before-pilot" / "schemas" / "prototype-evidence.schema.json"
HANDOFF_SCHEMA_PATH = SKILLS_ROOT / "prepare-review-handoff" / "schemas" / "review-handoff.schema.json"
SHAPE_EXAMPLE = LOOP_EXAMPLE / "shape.json"
BUILD_EXAMPLE = LOOP_EXAMPLE / "build.json"
PROOF_EXAMPLE = LOOP_EXAMPLE / "proof.json"
HANDOFF_EXAMPLE = LOOP_EXAMPLE / "review-handoff.json"
LOOP_STATE_EXAMPLE = LOOP_EXAMPLE / "loop-state.json"


class ValidationError(Exception):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"{path}: {exc}") from exc


def resolve_ref(root_schema: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValidationError(f"Only local JSON Schema references are supported: {ref}")
    node: Any = root_schema
    for part in ref[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict) or part not in node:
            raise ValidationError(f"Unresolved JSON Schema reference: {ref}")
        node = node[part]
    if not isinstance(node, dict):
        raise ValidationError(f"JSON Schema reference does not resolve to an object: {ref}")
    return node


def matches_type(value: Any, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    raise ValidationError(f"Unsupported JSON Schema type: {expected}")


def validate_format(value: str, format_name: str, path: str) -> None:
    try:
        if format_name == "date-time":
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        elif format_name == "date":
            date.fromisoformat(value)
        elif format_name == "uri":
            parsed = urlparse(value)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError("URI requires a scheme and host")
    except ValueError as exc:
        raise ValidationError(f"{path}: invalid {format_name}: {value!r}") from exc


def validate_instance(value: Any, schema: dict[str, Any], root_schema: dict[str, Any], path: str = "$") -> None:
    if "anyOf" in schema:
        failures: list[str] = []
        for candidate in schema["anyOf"]:
            try:
                validate_instance(value, candidate, root_schema, path)
                return
            except ValidationError as exc:
                failures.append(str(exc))
        raise ValidationError(f"{path}: value does not match any allowed schema: {failures!r}")

    if "$ref" in schema:
        validate_instance(value, resolve_ref(root_schema, schema["$ref"]), root_schema, path)
        return

    if "const" in schema and value != schema["const"]:
        raise ValidationError(f"{path}: expected constant {schema['const']!r}, got {value!r}")
    if "enum" in schema and value not in schema["enum"]:
        raise ValidationError(f"{path}: {value!r} is not in {schema['enum']!r}")

    expected_type = schema.get("type")
    if expected_type is not None:
        candidates = expected_type if isinstance(expected_type, list) else [expected_type]
        if not any(matches_type(value, candidate) for candidate in candidates):
            raise ValidationError(f"{path}: expected type {candidates!r}, got {type(value).__name__}")

    if isinstance(value, dict):
        required = schema.get("required", [])
        missing = [key for key in required if key not in value]
        if missing:
            raise ValidationError(f"{path}: missing required properties {missing!r}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extras = sorted(set(value) - set(properties))
            if extras:
                raise ValidationError(f"{path}: unexpected properties {extras!r}")
        for key, child in value.items():
            if key in properties:
                validate_instance(child, properties[key], root_schema, f"{path}.{key}")

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise ValidationError(f"{path}: expected at least {schema['minItems']} items")
        if schema.get("uniqueItems") and len({json.dumps(item, sort_keys=True) for item in value}) != len(value):
            raise ValidationError(f"{path}: items must be unique")
        item_schema = schema.get("items")
        if item_schema:
            for index, child in enumerate(value):
                validate_instance(child, item_schema, root_schema, f"{path}[{index}]")

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            raise ValidationError(f"{path}: string is shorter than {schema['minLength']}")
        if "pattern" in schema and not re.fullmatch(schema["pattern"], value):
            raise ValidationError(f"{path}: string does not match pattern {schema['pattern']!r}")
        if "format" in schema:
            validate_format(value, schema["format"], path)

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            raise ValidationError(f"{path}: {value} is below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            raise ValidationError(f"{path}: {value} exceeds maximum {schema['maximum']}")


def validate_scorecard(packet: dict[str, Any]) -> None:
    criteria = packet["scorecard"]["criteria"]
    criterion_by_id = {item["id"]: item for item in criteria}
    if len(criterion_by_id) != len(criteria):
        raise ValidationError("scorecard criteria ids must be unique")

    effective_weights: dict[str, int | None] = {}
    for criterion in criteria:
        requester_weight = criterion["requester_weight"]
        reviewer_weight = criterion["reviewer_weight"]
        weight_status = criterion["weight_status"]
        if weight_status == "unassigned":
            if requester_weight is not None or reviewer_weight is not None:
                raise ValidationError(f"{criterion['id']}: unassigned weight status requires null weights")
        elif weight_status == "requester-draft":
            if requester_weight is None or reviewer_weight is not None:
                raise ValidationError(f"{criterion['id']}: requester-draft requires a requester weight only")
        elif requester_weight is None or reviewer_weight is None:
            raise ValidationError(f"{criterion['id']}: reviewed weight status requires requester and reviewer weights")
        effective_weights[criterion["id"]] = reviewer_weight if reviewer_weight is not None else requester_weight

    all_weights_assigned = all(weight is not None for weight in effective_weights.values())
    total_weight = sum(weight for weight in effective_weights.values() if weight is not None)
    for option in packet["scorecard"]["option_scores"]:
        seen: set[str] = set()
        numerator = 0.0
        assessed_weight = 0
        for score in option["scores"]:
            criterion_id = score["criterion_id"]
            if criterion_id not in criterion_by_id:
                raise ValidationError(f"unknown scorecard criterion id: {criterion_id}")
            if criterion_id in seen:
                raise ValidationError(f"duplicate scorecard criterion id for {option['direction']}: {criterion_id}")
            seen.add(criterion_id)
            if score["fit"] is None:
                if score["confidence"] is not None:
                    raise ValidationError(f"unassessed fit must have null confidence: {option['direction']} / {criterion_id}")
                continue
            if score["confidence"] is None or not score["rationale"].strip():
                raise ValidationError(f"assessed fit needs confidence and rationale: {option['direction']} / {criterion_id}")
            weight = effective_weights[criterion_id]
            if weight is not None:
                numerator += weight * score["fit"]
                assessed_weight += weight

        missing_criteria = set(criterion_by_id) - seen
        if missing_criteria:
            raise ValidationError(
                f"{option['direction']}: scorecard is missing criteria {sorted(missing_criteria)!r}"
            )

        expected_completeness = (
            round(assessed_weight / total_weight * 100, 1) if all_weights_assigned and total_weight else None
        )
        if expected_completeness is None and option["evidence_completeness"] is not None:
            raise ValidationError(f"{option['direction']}: evidence completeness must be null while weights are unassigned")
        if expected_completeness is not None and (
            option["evidence_completeness"] is None
            or not math.isclose(option["evidence_completeness"], expected_completeness, abs_tol=0.05)
        ):
            raise ValidationError(
                f"{option['direction']}: evidence completeness {option['evidence_completeness']} != {expected_completeness}"
            )
        expected_score = (
            round(numerator / (assessed_weight * 5) * 100, 1)
            if all_weights_assigned and assessed_weight
            else None
        )
        if option["weighted_score"] is None and expected_score is not None:
            raise ValidationError(f"{option['direction']}: weighted score is unexpectedly null")
        if option["weighted_score"] is not None and expected_score is None:
            raise ValidationError(f"{option['direction']}: weighted score must be null while weights are unassigned")
        if expected_score is not None and not math.isclose(option["weighted_score"], expected_score, abs_tol=0.05):
            raise ValidationError(f"{option['direction']}: weighted score {option['weighted_score']} != {expected_score}")

    ranking_status = packet["scorecard"]["ranking_status"]
    ranking_caveat = packet["scorecard"]["ranking_caveat"]
    all_weights_reviewed = all(
        criterion["weight_status"] in {"reviewer-confirmed", "reviewer-revised"}
        for criterion in criteria
    )
    plausible_options = [option for option in packet["options"] if option["status"] == "plausible"]
    has_blocking_condition = any(
        condition["status"] != "pass"
        for option in plausible_options
        for condition in option["critical_conditions"]
    )
    if ranking_status == "withheld" and not (isinstance(ranking_caveat, str) and ranking_caveat.strip()):
        raise ValidationError("a withheld ranking requires a plain-language ranking caveat")
    if ranking_status == "available" and not all_weights_reviewed:
        raise ValidationError("ranking cannot be available until all weights are reviewer-confirmed or reviewer-revised")
    if ranking_status == "available" and has_blocking_condition:
        raise ValidationError("ranking cannot be available while a plausible option has a failed or unresolved critical condition")


def initiative_schema_for(packet: dict[str, Any]) -> dict[str, Any]:
    schema = load_json(SCHEMA_PATH)
    version = packet.get("schema_version")
    if version == "2.3.0":
        return schema
    if version in {"2.1.0", "2.2.0"}:
        legacy = json.loads(json.dumps(schema))
        legacy["properties"]["schema_version"]["const"] = version
        for field in ("stated_ideal_process", "target_process_design"):
            legacy["required"].remove(field)
            legacy["properties"].pop(field)
        if version == "2.1.0":
            legacy["required"].remove("initiative_id")
            legacy["properties"].pop("initiative_id")
            next_workflows = legacy["$defs"]["handoff"]["properties"]["next_workflow"]["enum"]
            next_workflows.remove("prototype-shaping")
        return legacy
    raise ValidationError(f"unsupported initiative packet schema version: {version!r}")


def validate_packet(path: Path) -> None:
    packet = load_json(path)
    validate_packet_data(packet, initiative_schema_for(packet))


def validate_packet_data(packet: dict[str, Any], schema: dict[str, Any] | None = None) -> None:
    schema = schema or initiative_schema_for(packet)
    validate_instance(packet, schema, schema)
    validate_scorecard(packet)
    option_directions = [item["direction"] for item in packet["options"]]
    directions = set(option_directions)
    if len(directions) != len(option_directions):
        raise ValidationError("solution-ladder directions must be unique")
    if packet["recommendation"]["direction"] not in directions:
        raise ValidationError("recommendation direction must appear in options")
    allowed_directions = set(resolve_ref(schema, "#/$defs/direction")["enum"])
    if directions != allowed_directions:
        missing = sorted(allowed_directions - directions)
        extra = sorted(directions - allowed_directions)
        raise ValidationError(f"options must cover the complete solution ladder; missing={missing!r}, extra={extra!r}")

    systems = packet["current_state"]["systems"]
    system_names = {item["name"] for item in systems}
    if len(system_names) != len(systems):
        raise ValidationError("current_state system names must be unique")
    for step in packet["current_state"]["steps"]:
        if step["system"] is not None and step["system"] not in system_names:
            raise ValidationError(f"process step references unknown system: {step['system']!r}")
    for source in packet["current_state"]["information_sources"]:
        if source["system"] is not None and source["system"] not in system_names:
            raise ValidationError(f"information source references unknown system: {source['system']!r}")
    step_sequences = [step["sequence"] for step in packet["current_state"]["steps"]]
    if step_sequences != list(range(1, len(step_sequences) + 1)):
        raise ValidationError("current-state process steps must use contiguous sequence numbers starting at 1")

    current_state = packet["current_state"]
    diagram = packet["process_diagram"]
    gate = diagram["evidence_gate"]
    if gate["trigger_and_completion"] and not (
        current_state["trigger"] and current_state["completion_condition"]
    ):
        raise ValidationError("diagram evidence gate cannot pass trigger and completion when either is missing")
    if gate["ordered_steps_and_actors"] and len(current_state["steps"]) < 2:
        raise ValidationError("diagram evidence gate cannot pass ordered steps with fewer than two steps")
    diagram_gate_passes = all(gate.values())
    if diagram_gate_passes and diagram["status"] != "mapped":
        raise ValidationError("a successfully mapped current process requires a mapped BPMN-style diagram")
    if diagram["status"] == "mapped":
        if not diagram_gate_passes:
            raise ValidationError("a mapped process diagram requires a trigger, completion condition, and at least two steps")
        if not isinstance(diagram["source"], str) or not diagram["source"].strip():
            raise ValidationError("a mapped process diagram requires non-empty Mermaid source")
        expected_actors = {step["actor"] for step in current_state["steps"]}
        if set(diagram["actors"]) != expected_actors:
            raise ValidationError("process diagram actors must cover the actors in current-state steps")
        if diagram["mapped_step_sequences"] != step_sequences:
            raise ValidationError("process diagram mapped sequences must match all current-state steps in order")
        source = diagram["source"]
        if "flowchart LR" not in source or "start((" not in source or "finish((" not in source:
            raise ValidationError("mapped process diagram must contain a Mermaid flowchart with start and end events")
        missing_nodes = [sequence for sequence in step_sequences if not re.search(rf"\bS{sequence}\s*[\[{{]", source)]
        if missing_nodes:
            raise ValidationError(f"process diagram is missing step nodes {missing_nodes!r}")
    else:
        if diagram["source"] is not None or diagram["mapped_step_sequences"]:
            raise ValidationError("an unmapped process diagram must have null source and no mapped step sequences")
        if diagram["actors"]:
            raise ValidationError("an unmapped process diagram must not claim mapped actors")
        if not diagram["unmapped_elements"] and not diagram["caveats"]:
            raise ValidationError("an unmapped process diagram must explain the gap or non-applicability")

    if packet["schema_version"] == "2.3.0":
        for field, mapped_status, basis in (
            ("stated_ideal_process", {"mapped", "partial"}, "stakeholder-stated"),
            ("target_process_design", {"proposed", "needs-evidence"}, "agent-proposed"),
        ):
            view = packet[field]
            if view["basis"] != basis:
                raise ValidationError(f"{field} must retain its declared evidence basis")
            has_map = view["status"] in mapped_status
            if has_map:
                if not isinstance(view["source"], str) or "flowchart LR" not in view["source"]:
                    raise ValidationError(f"{field} requires non-empty Mermaid flowchart source")
                if not view["node_ids"]:
                    raise ValidationError(f"{field} requires stable node ids")
                missing = [node for node in view["node_ids"] if not re.search(rf"\b{re.escape(node)}\s*[\[{{]", view["source"])]
                if missing:
                    raise ValidationError(f"{field} Mermaid source is missing declared nodes {missing!r}")
                if field == "stated_ideal_process" and view["status"] == "partial" and "partial" not in view["source"].casefold():
                    raise ValidationError("a partial stated-ideal diagram must visibly label itself partial or unconfirmed")
            elif view["source"] is not None or view["node_ids"] or view["actors"]:
                raise ValidationError(f"{field} without a map must keep source, nodes, and actors empty")
        direction = packet["recommendation"]["direction"]
        if direction not in {"eliminate-or-stop", "insufficient-evidence"} and packet["target_process_design"]["status"] != "proposed":
            raise ValidationError("a prototype-capable recommendation requires a proposed target-process design")

    artifacts = packet["artifacts"]
    markdown_path = Path(artifacts["markdown_path"])
    json_path = Path(artifacts["json_path"])
    if markdown_path.suffix.lower() != ".md" or json_path.suffix.lower() != ".json":
        raise ValidationError("artifact paths must end in .md and .json")
    if markdown_path.stem != json_path.stem or artifacts["basename"] != markdown_path.stem:
        raise ValidationError("artifact paths and basename must share one stem")
    if Path(artifacts["directory"]).as_posix() != markdown_path.parent.as_posix():
        raise ValidationError("artifact directory must match the Markdown and JSON parent directory")

    target = packet["handoff"]["target_system"]
    if target["mapping_status"] == "not-requested":
        if any(target[key] is not None for key in ("name", "issue_type", "project_or_queue")) or target["field_mappings"]:
            raise ValidationError("not-requested target mapping must not contain invented target metadata")

    handoff = packet["handoff"]
    if handoff["submission_ready"] and handoff["missing_for_submission"]:
        raise ValidationError("submission-ready handoff must not list information missing before submission")
    if handoff["suggested_request_type"] == "do-not-submit" and handoff["submission_ready"]:
        raise ValidationError("do-not-submit handoff cannot be marked submission-ready")


def validate_example_alignment() -> None:
    packet = load_json(EXAMPLE_PACKET)
    markdown = EXAMPLE_MARKDOWN.read_text(encoding="utf-8")
    required_fragments = [
        "## Decision snapshot",
        packet["initiative_id"],
        packet["initiative"]["name"],
        packet["initiative"]["fit"],
        packet["readiness"],
        packet["recommendation"]["direction"],
        packet["recommendation"]["next_decision"],
        packet["handoff"]["next_workflow"],
        *[system["name"] for system in packet["current_state"]["systems"]],
        *[knowledge["name"] for knowledge in packet["current_state"]["knowledge_sources"]],
    ]
    normalized_markdown = markdown.casefold()
    missing = [fragment for fragment in required_fragments if fragment.casefold() not in normalized_markdown]
    if missing:
        raise ValidationError(f"example Markdown is not aligned with JSON; missing {missing!r}")
    diagram = packet["process_diagram"]
    if diagram["status"] == "mapped":
        diagram_block = f"```mermaid\n{diagram['source']}\n```"
        if diagram_block not in markdown:
            raise ValidationError("example Markdown must embed the exact Mermaid source stored in JSON")
    for field in ("stated_ideal_process", "target_process_design"):
        view = packet.get(field)
        if view and view["source"] is not None:
            diagram_block = f"```mermaid\n{view['source']}\n```"
            if diagram_block not in markdown:
                raise ValidationError(f"example Markdown must embed the exact {field} Mermaid source stored in JSON")
    markdown_path = ROOT / packet["artifacts"]["markdown_path"]
    json_path = ROOT / packet["artifacts"]["json_path"]
    if markdown_path.resolve() != EXAMPLE_MARKDOWN.resolve() or json_path.resolve() != EXAMPLE_PACKET.resolve():
        raise ValidationError("example artifact paths do not resolve to the validated files")


def validate_pack() -> dict[str, Any]:
    pack = load_json(PACK_PATH)
    if pack.get("schema_version") != "1.1.0" or pack.get("name") != "better-work-loop":
        raise ValidationError("pack.json must declare the Better Work Loop 1.1 contract")
    if pack.get("version") != "0.4.0-alpha":
        raise ValidationError("pack.json must declare version 0.4.0-alpha")
    skills = pack.get("skills")
    if not isinstance(skills, list) or [item.get("name") for item in skills] != [
        "better-work-loop",
        "process-before-platform",
        "shape-the-slice",
        "build-the-slice",
        "prove-before-pilot",
        "prepare-review-handoff",
    ]:
        raise ValidationError("pack.json must preserve the approved six-skill order")
    if pack.get("example") != "examples/better-work-loop/synthetic-approval-portal":
        raise ValidationError("pack.json must point to the approved synthetic walkthrough")
    attributes = (ROOT / ".gitattributes").read_text(encoding="utf-8")
    for pattern in ("/examples/better-work-loop/**/*.json text eol=lf", "/skills/process-before-platform/examples/**/*.json text eol=lf"):
        if pattern not in attributes:
            raise ValidationError(".gitattributes must keep hashed example JSON bytes stable across platforms")
    return pack


def validate_skills(pack: dict[str, Any] | None = None) -> None:
    pack = pack or validate_pack()
    for entry in pack["skills"]:
        skill_dir = SKILLS_ROOT / entry["name"]
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            raise ValidationError(f"missing skill entrypoint: {skill_file.relative_to(ROOT)}")
        skill_text = skill_file.read_text(encoding="utf-8")
        if not skill_text.startswith("---\n"):
            raise ValidationError(f"{entry['name']}: SKILL.md must begin with YAML frontmatter")
        frontmatter_end = skill_text.find("\n---\n", 4)
        if frontmatter_end == -1:
            raise ValidationError(f"{entry['name']}: SKILL.md frontmatter is not closed")
        frontmatter = skill_text[4:frontmatter_end]

        def require_scalar(key: str) -> str:
            match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+)$", frontmatter)
            if not match:
                raise ValidationError(f"{entry['name']}: frontmatter is missing {key!r}")
            return match.group(1).strip().strip('"\'')

        name = require_scalar("name")
        description = require_scalar("description")
        license_id = require_scalar("license")
        if name != skill_dir.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValidationError(f"{entry['name']}: name must match its folder and use lowercase hyphen-case")
        if not 1 <= len(description) <= 1024 or "<" in description or ">" in description:
            raise ValidationError(f"{entry['name']}: description must be 1-1024 characters without angle brackets")
        if license_id != "Apache-2.0":
            raise ValidationError(f"{entry['name']}: license must be Apache-2.0")
        if not re.search(r'(?m)^  author:\s*["\']Luka Dujmovic["\']$', frontmatter):
            raise ValidationError(f"{entry['name']}: metadata must identify Luka Dujmovic as author")
        if not re.search(r'(?m)^  version:\s*["\']0\.4\.0-alpha["\']$', frontmatter):
            raise ValidationError(f"{entry['name']}: metadata must declare version 0.4.0-alpha")
        compatibility_match = re.search(r'(?m)^  compatibility:\s*["\'](.+)["\']$', frontmatter)
        if not compatibility_match or len(compatibility_match.group(1)) > 500:
            raise ValidationError(f"{entry['name']}: compatibility must be present and at most 500 characters")
        if len(skill_text.splitlines()) >= 500:
            raise ValidationError(f"{entry['name']}: SKILL.md must remain below 500 lines")
        if (skill_dir / "README.md").exists():
            raise ValidationError(f"{entry['name']}: installable skill folders must not contain README.md")
        if f"${entry['name']}" not in skill_text:
            raise ValidationError(f"{entry['name']}: SKILL.md must state its explicit invocation name")

        metadata_path = skill_dir / "agents" / "openai.yaml"
        metadata = metadata_path.read_text(encoding="utf-8")
        if "allow_implicit_invocation: false" not in metadata:
            raise ValidationError(f"{entry['name']}: openai.yaml must keep invocation explicit-only")
        if f"${entry['name']}" not in metadata or "default_prompt:" not in metadata:
            raise ValidationError(f"{entry['name']}: default_prompt must mention the skill invocation")

        schema_path = ROOT / entry["schema"]
        schema = load_json(schema_path)
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            raise ValidationError(f"{entry['name']}: schema must declare Draft 2020-12")


def validate_skill() -> None:
    """Backward-compatible entrypoint retained for existing tests and callers."""
    validate_skills()


def validate_links() -> None:
    pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for markdown in ROOT.rglob("*.md"):
        relative = markdown.relative_to(ROOT)
        if relative.parts[0] in {".codex-build", "output"}:
            continue
        text = markdown.read_text(encoding="utf-8")
        for raw_target in pattern.findall(text):
            target = raw_target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            candidate = (markdown.parent / target).resolve()
            if not candidate.exists():
                raise ValidationError(f"{relative}: broken relative link {raw_target!r}")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_artifact_ref(ref: dict[str, Any], label: str) -> Path:
    path = ARTIFACT_ROOT / ref["path"]
    if not path.exists():
        raise ValidationError(f"{label}: referenced artifact does not exist: {ref['path']}")
    expected = ref.get("sha256")
    if expected is not None and file_sha256(path) != expected:
        raise ValidationError(f"{label}: SHA-256 does not match {ref['path']}")
    return path


def initiative_id_for(packet: dict[str, Any], ref: dict[str, Any]) -> str:
    if packet["schema_version"] == "2.1.0":
        digest = file_sha256(validate_artifact_ref(ref, "legacy initiative"))
        seed = f"{ref['path']}\n{digest}".encode("utf-8")
        return "legacy-" + hashlib.sha256(seed).hexdigest()[:16]
    return packet["initiative_id"]


def unique_ids(items: list[dict[str, Any]], key: str, label: str) -> set[str]:
    values = [item[key] for item in items]
    if len(values) != len(set(values)):
        raise ValidationError(f"{label}: {key} values must be unique")
    return set(values)


def validate_shape_packet(packet: dict[str, Any]) -> None:
    schema = load_json(SHAPE_SCHEMA_PATH)
    validate_instance(packet, schema, schema)
    source = packet["source_initiative"]
    if source["source_type"] == "initiative-packet":
        if source["path"] is None or source["sha256"] is None or source["schema_version"] is None:
            raise ValidationError("initiative-packet shape source requires path, digest, and schema version")
        source_packet = load_json(validate_artifact_ref(source, "shape source"))
        validate_packet_data(source_packet)
        if source["schema_version"] != source_packet["schema_version"]:
            raise ValidationError("shape source schema version must match its packet")
        if packet["initiative_id"] != initiative_id_for(source_packet, source):
            raise ValidationError("shape initiative_id must match its source")
        if source_packet["recommendation"]["direction"] in {"eliminate-or-stop", "insufficient-evidence"}:
            if packet["status"] == "ready-to-build" or packet["build_gate"]["status"] == "accepted":
                raise ValidationError("stop or insufficient-evidence direction cannot authorize a build-ready slice")
        target_nodes = set(source_packet.get("target_process_design", {}).get("node_ids", []))
        referenced_nodes = set(packet["slice_focus"]["target_process_node_ids"])
        if not referenced_nodes <= target_nodes:
            raise ValidationError(f"shape references unknown target-process nodes: {sorted(referenced_nodes - target_nodes)!r}")
        if not any(ref.startswith(("current_state.", "evidence.")) for ref in packet["source_problem_refs"]):
            raise ValidationError("initiative-backed shape requires a source-problem reference to current state or evidence")
    elif any(source[key] is not None for key in ("path", "sha256", "schema_version")):
        raise ValidationError("plain-language shape source must keep path, digest, and schema version null")
    if packet["target_user"] != packet["roles"]["primary_user"]:
        raise ValidationError("shape target_user must match roles.primary_user")
    split = packet["split_assessment"]
    if packet["status"] == "ready-to-build" and split["selected_slice_decision"] != "fits-one-slice":
        raise ValidationError("a shape that must split cannot be ready to build")
    source_split_flags = (
        "source_multiple_primary_user_jobs",
        "source_independent_uncertainties",
        "source_unrelated_failure_modes",
    )
    if split["source_scope_decision"] == "fits-one-slice" and any(split[flag] for flag in source_split_flags):
        raise ValidationError("source scope fits-one-slice conflicts with its split-risk flags")
    if split["source_scope_decision"] == "must-split" and not split["source_split_reasons"]:
        raise ValidationError("a source scope that must split requires source_split_reasons")
    if packet["prototype"]["fidelity"] == "workflow-simulation" and packet["prototype"]["code_required"]:
        if "interaction" not in packet["prototype"]["code_rationale"].casefold():
            raise ValidationError("coded workflow simulation requires an explicit interaction-based rationale")
    unique_ids(packet["scenarios"], "id", "shape scenarios")
    unique_ids(packet["acceptance_criteria"], "id", "shape criteria")
    gate = packet["build_gate"]
    if gate["status"] == "accepted" and (gate["owner"] is None or gate["decided_at"] is None):
        raise ValidationError("accepted build gate requires an owner and decision timestamp")
    if gate["status"] == "pending" and gate["decided_at"] is not None:
        raise ValidationError("pending build gate cannot have a decision timestamp")
    if gate["status"] == "rejected" and packet["status"] != "stopped":
        raise ValidationError("rejected build gate requires stopped shape status")


def validate_build_packet(packet: dict[str, Any], shape: dict[str, Any] | None = None) -> None:
    schema = load_json(BUILD_SCHEMA_PATH)
    validate_instance(packet, schema, schema)
    shape_path = validate_artifact_ref(packet["source_shape"], "build source")
    shape = shape or load_json(shape_path)
    validate_shape_packet(shape)
    for key in ("loop_id", "initiative_id", "iteration"):
        if packet[key] != shape[key]:
            raise ValidationError(f"build and shape {key} must match")
    if shape["status"] != "ready-to-build" or shape["build_gate"]["status"] != "accepted":
        raise ValidationError("build requires a ready shape with an accepted build gate")
    if packet["fidelity"] != shape["prototype"]["fidelity"]:
        raise ValidationError("build fidelity must match the accepted shape")
    delivery = packet["fidelity_delivery"]
    if delivery["shape_fidelity"] != packet["fidelity"]:
        raise ValidationError("fidelity delivery must repeat the accepted shape fidelity")
    if delivery["code_used"] != shape["prototype"]["code_required"]:
        raise ValidationError("build code use must match the accepted shape code decision")
    if not delivery["code_used"] and delivery["delivered_format"] == "runnable-code":
        raise ValidationError("runnable-code delivery must declare code_used")
    if packet["fidelity"] == "workflow-simulation" and not delivery["code_used"]:
        if delivery["delivered_format"] not in {"facilitated-rehearsal", "documented-simulation"}:
            raise ValidationError("an uncoded workflow simulation must be delivered as a rehearsal or documented simulation")
    shape_scenarios = unique_ids(shape["scenarios"], "id", "shape scenarios")
    build_scenarios = unique_ids(packet["scenario_coverage"], "scenario_id", "build scenario coverage")
    if shape_scenarios != build_scenarios:
        raise ValidationError("build scenario coverage must match every shaped scenario")
    effects = packet["external_effects"]
    if (effects["live_writes"] or effects["deployed"] or effects["services"]) and not effects["requires_separate_authorization"]:
        raise ValidationError("external build effects require separate-authorization status")
    if packet["status"] == "built-and-verified":
        if any(check["status"] == "failed" for check in packet["verification"]):
            raise ValidationError("built-and-verified cannot contain a failed verification check")
        if any(item["status"] == "failed" for item in packet["scenario_coverage"]):
            raise ValidationError("built-and-verified cannot contain a failed scenario")


def validate_proof_packet(
    packet: dict[str, Any],
    shape: dict[str, Any] | None = None,
    build: dict[str, Any] | None = None,
) -> None:
    schema = load_json(PROOF_SCHEMA_PATH)
    validate_instance(packet, schema, schema)
    shape_path = validate_artifact_ref(packet["source_shape"], "proof shape source")
    build_path = validate_artifact_ref(packet["source_build"], "proof build source")
    shape = shape or load_json(shape_path)
    build = build or load_json(build_path)
    validate_shape_packet(shape)
    validate_build_packet(build, shape)
    if any(packet["source_shape"][key] != build["source_shape"][key] for key in ("path", "sha256", "schema_version")):
        raise ValidationError("proof must use the exact shape referenced by its build")
    for key in ("loop_id", "initiative_id", "iteration"):
        if packet[key] != shape[key] or packet[key] != build[key]:
            raise ValidationError(f"proof, build, and shape {key} must match")
    shaped_criteria = unique_ids(shape["acceptance_criteria"], "id", "shape criteria")
    proof_criteria = unique_ids(packet["criteria_results"], "criterion_id", "proof criteria")
    if shaped_criteria != proof_criteria:
        raise ValidationError("proof criteria must cover every shaped acceptance criterion")
    shaped_scenarios = unique_ids(shape["scenarios"], "id", "shape scenarios")
    proof_scenarios = unique_ids(packet["scenario_results"], "scenario_id", "proof scenarios")
    if shaped_scenarios != proof_scenarios:
        raise ValidationError("proof scenarios must cover every shaped scenario")
    for source_items, results, key in (
        (shape["acceptance_criteria"], packet["criteria_results"], "criterion_id"),
        (shape["scenarios"], packet["scenario_results"], "scenario_id"),
    ):
        critical_by_id = {item["id"]: item["critical"] for item in source_items}
        for result in results:
            if result["critical"] != critical_by_id[result[key]]:
                raise ValidationError("proof critical flags must match the approved shape")
            if result["status"] != "not-assessed" and not result["evidence"].strip():
                raise ValidationError("assessed proof results require evidence")

    status = packet["validation_status"]
    unique_ids(packet["sessions"], "id", "proof sessions")
    for session in packet["sessions"]:
        if session["evidence_type"] not in packet["evidence_types"]:
            raise ValidationError("every proof session evidence type must appear in evidence_types")
        if session["evidence_type"] == "stakeholder-feedback":
            if session["representative"] or session["target_job_attempted"] or session["target_job_completed"]:
                raise ValidationError("stakeholder feedback is not a representative target-job observation")
        if session["evidence_type"] == "user-observation" and not session["target_job_attempted"]:
            raise ValidationError("user-observation requires an attempted target job")
        if session["target_job_completed"] and not session["target_job_attempted"]:
            raise ValidationError("a completed target job requires an attempted target job")
    representative_completions = [
        session
        for session in packet["sessions"]
        if session["evidence_type"] == "user-observation"
        and session["representative"]
        and session["target_job_attempted"]
        and session["target_job_completed"]
    ]
    if status in {"user-observed", "validated"} and "user-observation" not in packet["evidence_types"]:
        raise ValidationError(f"{status} requires user-observation evidence type")
    representative_attempts = [
        session for session in packet["sessions"]
        if session["evidence_type"] == "user-observation" and session["representative"] and session["target_job_attempted"]
    ]
    if status == "user-observed" and not representative_attempts:
        raise ValidationError("user-observed requires a representative target-job attempt")
    assessed_user_results = [
        result for result in packet["criteria_results"] + packet["scenario_results"]
        if result["evidence_type"] == "user-observation" and result["status"] != "not-assessed"
    ]
    if assessed_user_results and not representative_attempts:
        raise ValidationError("assessed user-observation results require a representative target-job attempt")
    if packet["recommendation"] == "prepare-pilot-review" and status != "validated":
        raise ValidationError("pilot-review recommendation requires validated evidence")
    if status == "validated":
        if not representative_completions:
            raise ValidationError("validated requires a representative user to complete the target job")
        if packet["critical_failures"]:
            raise ValidationError("validated cannot retain critical failures")
        if packet["downstream_usability"]["status"] != "passed":
            raise ValidationError("validated requires passed downstream usability")
        if any(result["critical"] and result["status"] != "passed" for result in packet["criteria_results"]):
            raise ValidationError("validated requires every critical criterion to pass")
        if any(result["critical"] and result["status"] != "passed" for result in packet["scenario_results"]):
            raise ValidationError("validated requires every critical scenario to pass")
        if packet["recommendation"] != "prepare-pilot-review":
            raise ValidationError("validated prototype must route to accountable pilot review")
    if status in {"technically-verified", "agent-verified"} and representative_completions:
        raise ValidationError(f"{status} cannot hide completed representative-user evidence")
    if packet["recommendation"] == "retest" and not representative_completions:
        plan = packet["session_plan"]
        if plan["status"] != "ready":
            raise ValidationError("retest without representative-user completion requires a ready session plan")
        for field in ("participant_roles", "tasks", "scenario_ids", "facilitator_limits", "observation_fields", "critical_stop_conditions"):
            if not plan[field]:
                raise ValidationError(f"ready session plan requires {field}")
        if not set(plan["scenario_ids"]) <= shaped_scenarios:
            raise ValidationError("session plan references unknown shaped scenarios")


def validate_handoff_packet(
    packet: dict[str, Any],
    initiative: dict[str, Any] | None = None,
    shape: dict[str, Any] | None = None,
    build: dict[str, Any] | None = None,
    proof: dict[str, Any] | None = None,
) -> None:
    schema = load_json(HANDOFF_SCHEMA_PATH)
    validate_instance(packet, schema, schema)
    sources = packet["sources"]
    source_paths = {
        name: validate_artifact_ref(sources[name], f"handoff {name} source")
        for name in ("initiative", "shape", "build", "proof")
    }
    initiative = initiative or load_json(source_paths["initiative"])
    shape = shape or load_json(source_paths["shape"])
    build = build or load_json(source_paths["build"])
    proof = proof or load_json(source_paths["proof"])
    validate_packet_data(initiative)
    validate_shape_packet(shape)
    validate_build_packet(build, shape)
    validate_proof_packet(proof, shape, build)
    for label, source, artifact in (
        ("initiative", sources["initiative"], initiative),
        ("shape", sources["shape"], shape),
        ("build", sources["build"], build),
        ("proof", sources["proof"], proof),
    ):
        if source["schema_version"] != artifact["schema_version"]:
            raise ValidationError(f"handoff {label} schema version must match its artifact")
    for key in ("loop_id", "initiative_id", "iteration"):
        if key == "loop_id" and key not in initiative:
            continue
        expected = shape[key]
        if packet[key] != expected or build[key] != expected or proof[key] != expected:
            raise ValidationError(f"handoff chain {key} must match")
    if packet["initiative_id"] != initiative_id_for(initiative, sources["initiative"]):
        raise ValidationError("handoff initiative_id must match its initiative source")
    views = packet["process_views"]
    expected_views = {
        "current_state": (initiative["process_diagram"]["status"], "observed-current", initiative["process_diagram"]["source"]),
        "stated_ideal": (initiative["stated_ideal_process"]["status"], "stakeholder-stated", initiative["stated_ideal_process"]["source"]),
        "proposed_target": (initiative["target_process_design"]["status"], "agent-proposed", initiative["target_process_design"]["source"]),
    }
    for name, (status_value, basis, source_value) in expected_views.items():
        if views[name] != {"status": status_value, "basis": basis, "source": source_value}:
            raise ValidationError(f"handoff {name} process view must exactly preserve its initiative source")
    if packet["slice_summary"]["primary_user"] != shape["roles"]["primary_user"]:
        raise ValidationError("handoff primary user must match the accepted shape")
    if packet["slice_summary"]["source_problem_refs"] != shape["source_problem_refs"]:
        raise ValidationError("handoff source-problem references must match the accepted shape")
    if packet["slice_summary"]["roles"] != shape["roles"]:
        raise ValidationError("handoff role chain must match the accepted shape")
    if packet["slice_summary"]["split_assessment"] != shape["split_assessment"]:
        raise ValidationError("handoff split assessment must match the accepted shape")
    for handoff_key, shape_value in (
        ("selected_handoff_or_decision", shape["slice_focus"]["selected_handoff_or_decision"]),
        ("target_job", shape["target_job"]),
        ("hypothesis", shape["hypothesis"]),
        ("explicitly_excluded", shape["slice_focus"]["excluded_adjacent_jobs"]),
    ):
        if packet["slice_summary"][handoff_key] != shape_value:
            raise ValidationError(f"handoff {handoff_key} must match the accepted shape")
    if packet["slice_summary"]["target_process_node_ids"] != shape["slice_focus"]["target_process_node_ids"]:
        raise ValidationError("handoff target-process nodes must match the accepted shape")
    if packet["prototype_summary"]["fidelity"] != build["fidelity"] or packet["prototype_summary"]["code_used"] != build["fidelity_delivery"]["code_used"]:
        raise ValidationError("handoff prototype fidelity and code use must match the build")
    if packet["prototype_summary"]["delivered_format"] != build["fidelity_delivery"]["delivered_format"]:
        raise ValidationError("handoff delivered format must match the build")
    if not packet["prototype_summary"]["location"].startswith(build["destination"]["path"]):
        raise ValidationError("handoff prototype location must remain within the build destination")
    if packet["recommendation"] != proof["recommendation"] or packet["evidence_summary"]["recommendation"] != proof["recommendation"]:
        raise ValidationError("handoff recommendation must match proof")
    if packet["evidence_summary"]["validation_status"] != proof["validation_status"]:
        raise ValidationError("handoff validation status must match proof")
    representative = any(s["evidence_type"] == "user-observation" and s["representative"] and s["target_job_attempted"] for s in proof["sessions"])
    if packet["evidence_summary"]["representative_user_observed"] != representative:
        raise ValidationError("handoff representative-user claim must match proof sessions")
    if packet["user_session_plan"] != proof["session_plan"]:
        raise ValidationError("handoff session plan must exactly preserve proof")
    if packet["recommendation"] == "retest" and not representative and packet["status"] != "waiting-for-human":
        raise ValidationError("retest without representative evidence requires a waiting-for-human handoff")


def validate_loop_state(packet: dict[str, Any]) -> None:
    schema = load_json(LOOP_SCHEMA_PATH)
    validate_instance(packet, schema, schema)
    initiative_path = validate_artifact_ref(packet["source_initiative"], "loop initiative source")
    initiative = load_json(initiative_path)
    validate_packet_data(initiative)
    if packet["initiative_id"] != initiative_id_for(initiative, packet["source_initiative"]):
        raise ValidationError("loop initiative_id must match its initiative source")
    iterations = [item["iteration"] for item in packet["iterations"]]
    if iterations != list(range(1, len(iterations) + 1)):
        raise ValidationError("loop iterations must be contiguous and start at 1")
    for item in packet["iterations"]:
        loaded = {}
        for phase in ("shape", "build", "proof", "handoff"):
            if item[phase] is not None:
                artifact = load_json(validate_artifact_ref(item[phase], f"loop {phase} reference"))
                for key, expected in (("loop_id", packet["loop_id"]), ("initiative_id", packet["initiative_id"]), ("iteration", item["iteration"])):
                    if artifact[key] != expected:
                        raise ValidationError(f"loop {phase} {key} must match state")
                loaded[phase] = artifact
        if "handoff" in loaded and "proof" not in loaded or "proof" in loaded and "build" not in loaded or "build" in loaded and "shape" not in loaded:
            raise ValidationError("loop cannot skip predecessor phases")
        if "shape" in loaded:
            validate_shape_packet(loaded["shape"])
        if "build" in loaded:
            if any(loaded["build"]["source_shape"][key] != item["shape"][key] for key in ("path", "sha256")):
                raise ValidationError("loop build must reference its recorded shape")
            validate_build_packet(loaded["build"], loaded["shape"])
        if "proof" in loaded:
            if any(loaded["proof"]["source_build"][key] != item["build"][key] for key in ("path", "sha256")):
                raise ValidationError("loop proof must reference its recorded build")
            validate_proof_packet(loaded["proof"], loaded["shape"], loaded["build"])
        if "handoff" in loaded:
            sources = loaded["handoff"]["sources"]
            for source_name, phase_name in (("shape", "shape"), ("build", "build"), ("proof", "proof")):
                if any(sources[source_name][key] != item[phase_name][key] for key in ("path", "sha256")):
                    raise ValidationError(f"loop handoff must reference its recorded {phase_name}")
            validate_handoff_packet(loaded["handoff"], initiative, loaded["shape"], loaded["build"], loaded["proof"])
        if "proof" in loaded and "handoff" not in loaded:
            raise ValidationError("a proved iteration requires a review handoff")
    if packet["current_decision"] is not None:
        if not packet["decision_history"] or packet["decision_history"][-1]["decision"] != packet["current_decision"]:
            raise ValidationError("current loop decision must match the latest decision-history entry")
    history_times = [entry["at"] for entry in packet["decision_history"]]
    if history_times != sorted(history_times):
        raise ValidationError("loop decision history must be chronological")
    if packet["status"] == "completed" and packet["phase"] != "complete":
        raise ValidationError("completed loop status requires complete phase")
    if packet["phase"] == "handoff" and (not packet["iterations"] or packet["iterations"][-1]["handoff"] is None):
        raise ValidationError("handoff phase requires a recorded review handoff")
    latest = packet["iterations"][-1] if packet["iterations"] else None
    if latest and latest["shape"] is not None and latest["build"] is None:
        pending_shape = load_json(ARTIFACT_ROOT / latest["shape"]["path"])
        if pending_shape["status"] == "ready-to-build" and pending_shape["build_gate"]["status"] == "pending":
            if packet["phase"] != "shape" or packet["status"] != "waiting-for-human" or packet["current_decision"] != "decide-build-gate":
                raise ValidationError("a ready shape with a pending gate must wait on decide-build-gate")
    if latest and latest["proof"] is not None:
        proof = load_json(ARTIFACT_ROOT / latest["proof"]["path"])
        representative = any(s["evidence_type"] == "user-observation" and s["representative"] and s["target_job_attempted"] and s["target_job_completed"] for s in proof["sessions"])
        if proof["recommendation"] == "retest" and not representative:
            if packet["status"] != "waiting-for-human" or packet["phase"] != "handoff" or packet["current_decision"] != "seek-user-evidence":
                raise ValidationError("retest without representative-user completion must wait for human evidence in handoff phase")


def validate_loop_example() -> None:
    shape = load_json(SHAPE_EXAMPLE)
    build = load_json(BUILD_EXAMPLE)
    proof = load_json(PROOF_EXAMPLE)
    handoff = load_json(HANDOFF_EXAMPLE)
    loop_state = load_json(LOOP_STATE_EXAMPLE)
    validate_shape_packet(shape)
    validate_build_packet(build, shape)
    validate_proof_packet(proof, shape, build)
    validate_handoff_packet(handoff, load_json(EXAMPLE_PACKET), shape, build, proof)
    validate_loop_state(loop_state)

    if proof["validation_status"] != "agent-verified" or proof["recommendation"] != "retest":
        raise ValidationError("synthetic walkthrough must not claim representative-user validation")
    if proof["downstream_usability"]["status"] != "not-assessed":
        raise ValidationError("synthetic walkthrough must leave downstream usability unassessed")

    markdown_requirements = {
        "shape.md": ["## Shape decision", shape["hypothesis"], shape["build_gate"]["status"]],
        "build.md": ["## Build result", build["status"], "External effects"],
        "proof.md": ["## Evidence decision", proof["validation_status"], proof["recommendation"]],
        "review-handoff.md": ["## Decision snapshot", handoff["recommendation"], "Ready-to-run user session"],
        "loop-state.md": ["## Current state", loop_state["current_decision"], "representative-user evidence"],
    }
    for filename, fragments in markdown_requirements.items():
        content = (LOOP_EXAMPLE / filename).read_text(encoding="utf-8")
        missing = [fragment for fragment in fragments if fragment.casefold() not in content.casefold()]
        if missing:
            raise ValidationError(f"{filename}: missing aligned fragments {missing!r}")

    prototype = (LOOP_EXAMPLE / "prototype" / "index.html").read_text(encoding="utf-8")
    for fragment in ("request-form", "aria-live", "No approval was made", "navigator.clipboard"):
        if fragment not in prototype:
            raise ValidationError(f"example prototype is missing required behavior marker: {fragment}")


def validate_eval_cases() -> None:
    payload = load_json(EVAL_CASES)
    if payload.get("schema_version") != "3.0.0":
        raise ValidationError("evals/cases.json must use collection schema version 3.0.0")
    cases = payload.get("cases")
    if not isinstance(cases, list) or len(cases) < 11:
        raise ValidationError("evals/cases.json must retain at least the eleven approved alpha cases")
    ids: set[str] = set()
    allowed_directions = set(resolve_ref(load_json(SCHEMA_PATH), "#/$defs/direction")["enum"])
    for case in cases:
        for key in ("id", "title", "input", "expected"):
            if key not in case:
                raise ValidationError(f"evaluation case is missing {key!r}")
        if case["id"] in ids:
            raise ValidationError(f"duplicate evaluation case id: {case['id']}")
        ids.add(case["id"])
        expected = case["expected"]
        for key in ("allowed_directions", "forbidden_directions", "required_behaviors"):
            if not isinstance(expected.get(key), list) or not expected[key]:
                raise ValidationError(f"{case['id']}: expected.{key} must be a non-empty list")
        invalid = (set(expected["allowed_directions"]) | set(expected["forbidden_directions"])) - allowed_directions
        if invalid:
            raise ValidationError(f"{case['id']}: unknown directions {sorted(invalid)!r}")


def validate_loop_eval_cases() -> None:
    payload = load_json(LOOP_EVAL_CASES)
    if payload.get("schema_version") != "1.1.0":
        raise ValidationError("evals/loop-cases.json must use schema version 1.1.0")
    cases = payload.get("cases")
    if not isinstance(cases, list) or len(cases) < 10:
        raise ValidationError("loop behavioral evaluation must retain at least ten cases")
    ids: set[str] = set()
    phases = {"decide", "shape", "build", "prove", "handoff", "complete"}
    for case in cases:
        for key in ("id", "title", "input", "expected"):
            if key not in case:
                raise ValidationError(f"loop evaluation case is missing {key!r}")
        if case["id"] in ids:
            raise ValidationError(f"duplicate loop evaluation case id: {case['id']}")
        ids.add(case["id"])
        expected = case["expected"]
        if expected.get("terminal_phase") not in phases:
            raise ValidationError(f"{case['id']}: invalid terminal phase")
        if not isinstance(expected.get("required_behaviors"), list) or not expected["required_behaviors"]:
            raise ValidationError(f"{case['id']}: required_behaviors must be a non-empty list")


def validate_repository(packet_path: Path | None = None) -> None:
    pack = validate_pack()
    validate_skills(pack)
    validate_links()
    validate_eval_cases()
    validate_loop_eval_cases()
    validate_packet(packet_path or EXAMPLE_PACKET)
    if packet_path is None:
        validate_example_alignment()
        validate_loop_example()


def main() -> int:
    global ARTIFACT_ROOT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, help="Validate an additional initiative packet against the active contract")
    parser.add_argument("--artifact", type=Path, help="Validate a generated shape, build, proof, or loop-state JSON")
    parser.add_argument("--kind", choices=("shape", "build", "proof", "handoff", "loop"), help="Artifact type (required with --artifact)")
    parser.add_argument("--project-root", type=Path, help="Root for recorded relative artifact paths")
    args = parser.parse_args()
    if bool(args.artifact) != bool(args.kind) or args.artifact and args.packet:
        parser.error("use --artifact and --kind together, without --packet")
    if args.project_root and not args.artifact:
        parser.error("--project-root requires --artifact")
    try:
        if args.artifact:
            ARTIFACT_ROOT = (args.project_root or Path.cwd()).resolve()
            checks = {"shape": validate_shape_packet, "build": validate_build_packet,
                      "proof": validate_proof_packet, "handoff": validate_handoff_packet, "loop": validate_loop_state}
            checks[args.kind](load_json(args.artifact))
            print(f"Validation passed: {args.kind} artifact and referenced evidence chain.")
            return 0
        validate_repository(args.packet)
    except ValidationError as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1
    print("Validation passed: Better Work Loop pack, six skills, v2.3 initiative and phase schemas, three process views, aligned artifact chain and hashes, review handoff, scorecard, and evaluation fixtures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
