import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("repository_validate", ROOT / "scripts" / "validate.py")
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class RepositoryValidationTests(unittest.TestCase):
    def setUp(self):
        self.schema = validator.load_json(validator.SCHEMA_PATH)
        self.packet = validator.load_json(validator.EXAMPLE_PACKET)

    def test_repository_contract_passes(self):
        validator.validate_repository()

    def test_missing_required_field_fails(self):
        packet = copy.deepcopy(self.packet)
        del packet["recommendation"]
        with self.assertRaises(validator.ValidationError):
            validator.validate_instance(packet, self.schema, self.schema)

    def test_unknown_direction_fails(self):
        packet = copy.deepcopy(self.packet)
        packet["recommendation"]["direction"] = "build-the-demo"
        with self.assertRaises(validator.ValidationError):
            validator.validate_instance(packet, self.schema, self.schema)

    def test_score_mismatch_fails(self):
        packet = copy.deepcopy(self.packet)
        packet["scorecard"]["option_scores"][0]["weighted_score"] = 99.9
        with self.assertRaises(validator.ValidationError):
            validator.validate_scorecard(packet)

    def test_null_fit_requires_null_confidence(self):
        packet = copy.deepcopy(self.packet)
        target = packet["scorecard"]["option_scores"][1]["scores"][-1]
        target["confidence"] = "low"
        with self.assertRaises(validator.ValidationError):
            validator.validate_scorecard(packet)

    def test_scorecard_option_must_cover_every_criterion(self):
        packet = copy.deepcopy(self.packet)
        packet["scorecard"]["option_scores"][0]["scores"] = packet["scorecard"]["option_scores"][0]["scores"][:-1]
        with self.assertRaises(validator.ValidationError):
            validator.validate_scorecard(packet)

    def test_withheld_ranking_requires_caveat(self):
        packet = copy.deepcopy(self.packet)
        packet["scorecard"]["ranking_caveat"] = None
        with self.assertRaises(validator.ValidationError):
            validator.validate_scorecard(packet)

    def test_requester_weights_cannot_produce_available_ranking(self):
        packet = copy.deepcopy(self.packet)
        for criterion in packet["scorecard"]["criteria"]:
            criterion["requester_weight"] = 3
            criterion["reviewer_weight"] = None
            criterion["weight_status"] = "requester-draft"
        packet["scorecard"]["ranking_status"] = "available"
        packet["scorecard"]["ranking_caveat"] = None
        with self.assertRaises(validator.ValidationError):
            validator.validate_scorecard(packet)

    def test_available_ranking_requires_resolved_critical_conditions(self):
        packet = copy.deepcopy(self.packet)
        for criterion in packet["scorecard"]["criteria"]:
            criterion["requester_weight"] = 3
            criterion["reviewer_weight"] = 3
            criterion["weight_status"] = "reviewer-confirmed"
        for option in packet["scorecard"]["option_scores"]:
            assessed = [score for score in option["scores"] if score["fit"] is not None]
            option["evidence_completeness"] = round(len(assessed) / len(packet["scorecard"]["criteria"]) * 100, 1)
            option["weighted_score"] = round(sum(score["fit"] for score in assessed) / (len(assessed) * 5) * 100, 1)
        packet["options"][1]["critical_conditions"].append(
            {
                "criterion_id": "ownership",
                "status": "unresolved",
                "evidence": "Support ownership has not been confirmed.",
                "owner": None,
                "consequence": "The option cannot be selected responsibly.",
            }
        )
        packet["scorecard"]["ranking_status"] = "available"
        packet["scorecard"]["ranking_caveat"] = None
        with self.assertRaises(validator.ValidationError):
            validator.validate_scorecard(packet)

    def test_unassigned_weights_keep_aggregates_null(self):
        packet = copy.deepcopy(self.packet)
        for criterion in packet["scorecard"]["criteria"]:
            criterion["requester_weight"] = None
            criterion["reviewer_weight"] = None
            criterion["weight_status"] = "unassigned"
        for option in packet["scorecard"]["option_scores"]:
            option["weighted_score"] = None
            option["evidence_completeness"] = None

        validator.validate_instance(packet, self.schema, self.schema)
        validator.validate_scorecard(packet)

    def test_solution_ladder_must_be_complete(self):
        packet = copy.deepcopy(self.packet)
        packet["options"] = packet["options"][:-1]
        with self.assertRaises(validator.ValidationError):
            validator.validate_packet_data(packet)

    def test_process_step_cannot_reference_unknown_system(self):
        packet = copy.deepcopy(self.packet)
        packet["current_state"]["steps"][0]["system"] = "Unlisted tool"
        with self.assertRaises(validator.ValidationError):
            validator.validate_packet_data(packet)

    def test_solution_ladder_directions_must_be_unique(self):
        packet = copy.deepcopy(self.packet)
        packet["options"][-1] = copy.deepcopy(packet["options"][0])
        with self.assertRaises(validator.ValidationError):
            validator.validate_packet_data(packet)

    def test_submission_ready_requires_no_missing_fields(self):
        packet = copy.deepcopy(self.packet)
        packet["handoff"]["submission_ready"] = True
        packet["handoff"]["missing_for_submission"] = ["Owner needed before routing"]
        with self.assertRaises(validator.ValidationError):
            validator.validate_packet_data(packet)

    def test_do_not_submit_cannot_be_submission_ready(self):
        packet = copy.deepcopy(self.packet)
        packet["handoff"]["suggested_request_type"] = "do-not-submit"
        packet["handoff"]["submission_ready"] = True
        packet["handoff"]["missing_for_submission"] = []
        with self.assertRaises(validator.ValidationError):
            validator.validate_packet_data(packet)

    def test_successful_process_map_requires_mapped_diagram(self):
        packet = copy.deepcopy(self.packet)
        packet["process_diagram"].update(
            {
                "status": "insufficient-evidence",
                "source": None,
                "actors": [],
                "mapped_step_sequences": [],
                "unmapped_elements": ["Diagram omitted despite a complete map."],
            }
        )
        with self.assertRaises(validator.ValidationError):
            validator.validate_packet_data(packet)

    def test_mapped_diagram_must_cover_every_process_step(self):
        packet = copy.deepcopy(self.packet)
        packet["process_diagram"]["mapped_step_sequences"] = [1, 2, 3]
        with self.assertRaises(validator.ValidationError):
            validator.validate_packet_data(packet)

    def test_unmapped_diagram_cannot_contain_source(self):
        packet = copy.deepcopy(self.packet)
        packet["current_state"]["trigger"] = None
        packet["process_diagram"]["evidence_gate"]["trigger_and_completion"] = False
        packet["process_diagram"]["status"] = "insufficient-evidence"
        packet["process_diagram"]["mapped_step_sequences"] = []
        packet["process_diagram"]["actors"] = []
        with self.assertRaises(validator.ValidationError):
            validator.validate_packet_data(packet)

    def test_incomplete_map_can_record_no_diagram_without_guessing(self):
        packet = copy.deepcopy(self.packet)
        packet["current_state"]["trigger"] = None
        packet["process_diagram"].update(
            {
                "status": "insufficient-evidence",
                "source": None,
                "actors": [],
                "mapped_step_sequences": [],
                "unmapped_elements": ["The process trigger is unknown."],
            }
        )
        packet["process_diagram"]["evidence_gate"]["trigger_and_completion"] = False
        validator.validate_packet_data(packet)

    def test_example_markdown_and_json_align(self):
        validator.validate_example_alignment()


if __name__ == "__main__":
    unittest.main()
