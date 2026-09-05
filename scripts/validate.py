#!/usr/bin/env python3
"""Dependency-free validation for the Skills for Better Work repository."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "process-before-platform"
SCHEMA_PATH = SKILL / "schemas" / "initiative-request.schema.json"
EXAMPLE_PACKET = SKILL / "examples" / "synthetic-approval-portal" / "initiative-request.json"
EXAMPLE_MARKDOWN = SKILL / "examples" / "synthetic-approval-portal" / "initiative-request.md"
EVAL_CASES = ROOT / "evals" / "cases.json"


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
        item_schema = schema.get("items")
        if item_schema:
            for index, child in enumerate(value):
                validate_instance(child, item_schema, root_schema, f"{path}[{index}]")

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            raise ValidationError(f"{path}: string is shorter than {schema['minLength']}")
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


def validate_packet(path: Path) -> None:
    schema = load_json(SCHEMA_PATH)
    packet = load_json(path)
    validate_packet_data(packet, schema)


def validate_packet_data(packet: dict[str, Any], schema: dict[str, Any] | None = None) -> None:
    schema = schema or load_json(SCHEMA_PATH)
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


def validate_example_alignment() -> None:
    packet = load_json(EXAMPLE_PACKET)
    markdown = EXAMPLE_MARKDOWN.read_text(encoding="utf-8")
    required_fragments = [
        packet["initiative"]["name"],
        packet["initiative"]["fit"],
        packet["readiness"],
        packet["recommendation"]["direction"],
        packet["recommendation"]["next_decision"],
        *[system["name"] for system in packet["current_state"]["systems"]],
        *[knowledge["name"] for knowledge in packet["current_state"]["knowledge_sources"]],
    ]
    normalized_markdown = markdown.casefold()
    missing = [fragment for fragment in required_fragments if fragment.casefold() not in normalized_markdown]
    if missing:
        raise ValidationError(f"example Markdown is not aligned with JSON; missing {missing!r}")
    markdown_path = ROOT / packet["artifacts"]["markdown_path"]
    json_path = ROOT / packet["artifacts"]["json_path"]
    if markdown_path.resolve() != EXAMPLE_MARKDOWN.resolve() or json_path.resolve() != EXAMPLE_PACKET.resolve():
        raise ValidationError("example artifact paths do not resolve to the validated files")


def validate_skill() -> None:
    skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    if not skill_text.startswith("---\n") or "\nname: process-before-platform\n" not in skill_text:
        raise ValidationError("SKILL.md frontmatter is missing or has the wrong name")
    if "$process-before-platform" not in skill_text:
        raise ValidationError("SKILL.md must state the explicit invocation name")
    metadata = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
    if "allow_implicit_invocation: false" not in metadata:
        raise ValidationError("agents/openai.yaml must keep invocation explicit-only")
    if 'default_prompt: "Use $process-before-platform' not in metadata:
        raise ValidationError("default_prompt must mention $process-before-platform")


def validate_links() -> None:
    pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for markdown in ROOT.rglob("*.md"):
        text = markdown.read_text(encoding="utf-8")
        for raw_target in pattern.findall(text):
            target = raw_target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            candidate = (markdown.parent / target).resolve()
            if not candidate.exists():
                raise ValidationError(f"{markdown.relative_to(ROOT)}: broken relative link {raw_target!r}")


def validate_eval_cases() -> None:
    payload = load_json(EVAL_CASES)
    if payload.get("schema_version") != "2.0.0":
        raise ValidationError("evals/cases.json must use schema version 2.0.0")
    cases = payload.get("cases")
    if not isinstance(cases, list) or len(cases) != 11:
        raise ValidationError("evals/cases.json must contain the eleven approved alpha cases")
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


def validate_repository(packet_path: Path | None = None) -> None:
    validate_skill()
    validate_links()
    validate_eval_cases()
    validate_packet(packet_path or EXAMPLE_PACKET)
    if packet_path is None:
        validate_example_alignment()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, help="Validate an additional initiative packet against the active contract")
    args = parser.parse_args()
    try:
        validate_repository(args.packet)
    except ValidationError as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1
    print("Validation passed: skill, links, v2 initiative schema, aligned example artifacts, scorecard, and evaluation fixtures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
