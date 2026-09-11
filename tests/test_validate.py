import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from unittest.mock import patch
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
        self.shape = validator.load_json(validator.SHAPE_EXAMPLE)
        self.build = validator.load_json(validator.BUILD_EXAMPLE)
        self.proof = validator.load_json(validator.PROOF_EXAMPLE)
        self.handoff = validator.load_json(validator.HANDOFF_EXAMPLE)
        self.loop_state = validator.load_json(validator.LOOP_STATE_EXAMPLE)

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

    def test_pack_contract_and_loop_example_pass(self):
        validator.validate_pack()
        validator.validate_loop_example()

    def test_plain_language_shape_source_is_supported_without_fake_artifact(self):
        shape = copy.deepcopy(self.shape)
        shape["source_initiative"] = {
            "source_type": "plain-language",
            "path": None,
            "sha256": None,
            "schema_version": None,
        }
        validator.validate_shape_packet(shape)

    def test_legacy_v21_initiative_packet_remains_accepted(self):
        packet = copy.deepcopy(self.packet)
        packet["schema_version"] = "2.1.0"
        del packet["initiative_id"]
        del packet["stated_ideal_process"]
        del packet["target_process_design"]
        packet["handoff"]["next_workflow"] = "discovery"
        validator.validate_packet_data(packet)

    def test_legacy_v22_initiative_packet_remains_accepted(self):
        packet = copy.deepcopy(self.packet)
        packet["schema_version"] = "2.2.0"
        del packet["stated_ideal_process"]
        del packet["target_process_design"]
        validator.validate_packet_data(packet)

    def test_legacy_v21_packet_cannot_use_new_prototype_route(self):
        packet = copy.deepcopy(self.packet)
        packet["schema_version"] = "2.1.0"
        del packet["initiative_id"]
        del packet["stated_ideal_process"]
        del packet["target_process_design"]
        with self.assertRaises(validator.ValidationError):
            validator.validate_packet_data(packet)

    def test_prototype_capable_direction_requires_proposed_target_process(self):
        packet = copy.deepcopy(self.packet)
        packet["target_process_design"]["status"] = "needs-evidence"
        with self.assertRaisesRegex(validator.ValidationError, "proposed target-process"):
            validator.validate_packet_data(packet)

    def test_target_process_declared_nodes_must_exist_in_mermaid(self):
        packet = copy.deepcopy(self.packet)
        packet["target_process_design"]["node_ids"].append("T99")
        with self.assertRaisesRegex(validator.ValidationError, "missing declared nodes"):
            validator.validate_packet_data(packet)

    def test_partial_stated_ideal_is_visibly_labelled(self):
        packet = copy.deepcopy(self.packet)
        packet["stated_ideal_process"]["status"] = "partial"
        with self.assertRaisesRegex(validator.ValidationError, "visibly label"):
            validator.validate_packet_data(packet)
        packet["stated_ideal_process"]["source"] += '\n  note["PARTIAL / UNCONFIRMED"]'
        validator.validate_packet_data(packet)

    def test_build_requires_accepted_gate(self):
        shape = copy.deepcopy(self.shape)
        shape["build_gate"].update({"status": "pending", "decided_at": None})
        with self.assertRaises(validator.ValidationError):
            validator.validate_build_packet(self.build, shape)

    def test_shape_separates_owner_from_primary_user(self):
        self.assertNotEqual(self.shape["roles"]["accountable_owner"], self.shape["roles"]["primary_user"])
        validator.validate_shape_packet(self.shape)

    def test_shape_target_user_must_match_primary_user(self):
        shape = copy.deepcopy(self.shape)
        shape["target_user"] = "Accountable owner"
        with self.assertRaisesRegex(validator.ValidationError, "primary_user"):
            validator.validate_shape_packet(shape)

    def test_shape_rejects_unknown_target_process_node(self):
        shape = copy.deepcopy(self.shape)
        shape["slice_focus"]["target_process_node_ids"].append("T99")
        with self.assertRaisesRegex(validator.ValidationError, "unknown target-process"):
            validator.validate_shape_packet(shape)

    def test_shape_that_must_split_cannot_be_build_ready(self):
        shape = copy.deepcopy(self.shape)
        shape["split_assessment"]["selected_slice_decision"] = "must-split"
        with self.assertRaisesRegex(validator.ValidationError, "must split"):
            validator.validate_shape_packet(shape)

    def test_source_split_decision_survives_selected_slice(self):
        self.assertEqual(self.shape["split_assessment"]["source_scope_decision"], "must-split")
        self.assertEqual(self.shape["split_assessment"]["selected_slice_decision"], "fits-one-slice")
        validator.validate_shape_packet(self.shape)

    def test_source_split_requires_reasons(self):
        shape = copy.deepcopy(self.shape)
        shape["split_assessment"]["source_split_reasons"] = []
        with self.assertRaisesRegex(validator.ValidationError, "source_split_reasons"):
            validator.validate_shape_packet(shape)

    def test_workflow_simulation_requires_specific_code_rationale(self):
        shape = copy.deepcopy(self.shape)
        shape["prototype"]["fidelity"] = "workflow-simulation"
        shape["prototype"]["code_required"] = True
        shape["prototype"]["code_rationale"] = "A web app would look useful."
        with self.assertRaisesRegex(validator.ValidationError, "interaction-based"):
            validator.validate_shape_packet(shape)

    def test_build_code_use_must_match_accepted_shape(self):
        build = copy.deepcopy(self.build)
        build["fidelity_delivery"]["code_used"] = False
        build["fidelity_delivery"]["delivered_format"] = "documented-simulation"
        with self.assertRaisesRegex(validator.ValidationError, "code use"):
            validator.validate_build_packet(build, self.shape)

    def test_build_rejects_incomplete_scenario_coverage(self):
        build = copy.deepcopy(self.build)
        build["scenario_coverage"] = build["scenario_coverage"][:-1]
        with self.assertRaises(validator.ValidationError):
            validator.validate_build_packet(build, self.shape)

    def test_external_effects_require_separate_authorization_status(self):
        build = copy.deepcopy(self.build)
        build["external_effects"]["live_writes"] = True
        with self.assertRaises(validator.ValidationError):
            validator.validate_build_packet(build, self.shape)

    def test_changed_predecessor_digest_is_rejected(self):
        build = copy.deepcopy(self.build)
        build["source_shape"]["sha256"] = "0" * 64
        with self.assertRaises(validator.ValidationError):
            validator.validate_build_packet(build)

    def test_synthetic_evidence_cannot_claim_validated(self):
        proof = copy.deepcopy(self.proof)
        proof["validation_status"] = "validated"
        proof["recommendation"] = "prepare-pilot-review"
        with self.assertRaises(validator.ValidationError):
            validator.validate_proof_packet(proof, self.shape, self.build)

    def test_representative_user_can_support_narrow_validation(self):
        proof = copy.deepcopy(self.proof)
        proof["validation_status"] = "validated"
        proof["evidence_types"].append("user-observation")
        proof["sessions"].append(
            {
                "id": "USR-1",
                "evidence_type": "user-observation",
                "participant_role": "Operations coordinator",
                "representative": True,
                "target_job_attempted": True,
                "target_job_completed": True,
                "observations": ["Completed the bounded target job without coaching."],
                "participant_feedback": ["The route and missing-field feedback were clear."],
                "evaluator_interpretation": ["The bounded job passed for this participant."],
            }
        )
        for result in proof["criteria_results"] + proof["scenario_results"]:
            if result["status"] == "not-assessed":
                result["status"] = "passed"
                result["evidence_type"] = "user-observation"
                result["evidence"] = "Observed in the representative-user session."
        proof["downstream_usability"] = {
            "status": "passed",
            "evidence": "A representative reviewer used the summary without reconstruction.",
        }
        proof["recommendation"] = "prepare-pilot-review"
        validator.validate_proof_packet(proof, self.shape, self.build)

    def test_validated_cannot_retain_critical_failure(self):
        proof = copy.deepcopy(self.proof)
        proof["validation_status"] = "validated"
        proof["evidence_types"].append("user-observation")
        proof["sessions"].append(
            {
                "id": "USR-1",
                "evidence_type": "user-observation",
                "participant_role": "Operations coordinator",
                "representative": True,
                "target_job_attempted": True,
                "target_job_completed": True,
                "observations": [],
                "participant_feedback": [],
                "evaluator_interpretation": [],
            }
        )
        proof["critical_failures"] = ["The prototype implied approval for an exception."]
        proof["downstream_usability"]["status"] = "passed"
        proof["recommendation"] = "prepare-pilot-review"
        with self.assertRaises(validator.ValidationError):
            validator.validate_proof_packet(proof, self.shape, self.build)

    def test_loop_current_decision_matches_history(self):
        loop_state = copy.deepcopy(self.loop_state)
        loop_state["current_decision"] = "adapt-prototype"
        with self.assertRaises(validator.ValidationError):
            validator.validate_loop_state(loop_state)

    def test_proof_cannot_downgrade_critical_criteria_or_scenarios(self):
        for field in ("criteria_results", "scenario_results"):
            with self.subTest(field=field):
                proof = copy.deepcopy(self.proof)
                proof[field][0]["critical"] = False
                with self.assertRaisesRegex(validator.ValidationError, "critical flags"):
                    validator.validate_proof_packet(proof, self.shape, self.build)

    def test_agent_evidence_cannot_recommend_pilot_review(self):
        proof = copy.deepcopy(self.proof)
        proof["recommendation"] = "prepare-pilot-review"
        with self.assertRaisesRegex(validator.ValidationError, "requires validated"):
            validator.validate_proof_packet(proof, self.shape, self.build)

    def test_stakeholder_feedback_is_not_user_observation(self):
        proof = copy.deepcopy(self.proof)
        proof["evidence_types"].append("stakeholder-feedback")
        proof["sessions"].append(
            {
                "id": "STK-1",
                "evidence_type": "stakeholder-feedback",
                "participant_role": "Requester",
                "representative": False,
                "target_job_attempted": False,
                "target_job_completed": False,
                "observations": [],
                "participant_feedback": ["This looks useful."],
                "evaluator_interpretation": ["Feedback is directional only."],
            }
        )
        validator.validate_proof_packet(proof, self.shape, self.build)
        proof["sessions"][-1]["representative"] = True
        with self.assertRaisesRegex(validator.ValidationError, "not a representative"):
            validator.validate_proof_packet(proof, self.shape, self.build)

    def test_user_observation_requires_target_job_attempt(self):
        proof = copy.deepcopy(self.proof)
        proof["evidence_types"].append("user-observation")
        proof["sessions"].append(
            {
                "id": "USR-0",
                "evidence_type": "user-observation",
                "participant_role": "Operations coordinator",
                "representative": True,
                "target_job_attempted": False,
                "target_job_completed": False,
                "observations": [],
                "participant_feedback": ["Looks fine."],
                "evaluator_interpretation": [],
            }
        )
        with self.assertRaisesRegex(validator.ValidationError, "attempted target job"):
            validator.validate_proof_packet(proof, self.shape, self.build)

    def test_retest_without_user_requires_ready_session_plan(self):
        proof = copy.deepcopy(self.proof)
        proof["session_plan"]["status"] = "blocked"
        with self.assertRaisesRegex(validator.ValidationError, "ready session plan"):
            validator.validate_proof_packet(proof, self.shape, self.build)

    def test_review_handoff_must_preserve_target_process(self):
        handoff = copy.deepcopy(self.handoff)
        handoff["process_views"]["proposed_target"]["source"] += "\n  T99[\"Invented\"]"
        with self.assertRaisesRegex(validator.ValidationError, "exactly preserve"):
            validator.validate_handoff_packet(handoff, self.packet, self.shape, self.build, self.proof)

    def test_retest_loop_cannot_be_marked_complete(self):
        state = copy.deepcopy(self.loop_state)
        state["phase"] = "complete"
        state["status"] = "completed"
        with self.assertRaisesRegex(validator.ValidationError, "wait for human evidence"):
            validator.validate_loop_state(state)

    def test_pending_shape_uses_decide_build_gate(self):
        state = copy.deepcopy(self.loop_state)
        pending_shape = copy.deepcopy(self.shape)
        pending_shape["build_gate"] = {"status": "pending", "owner": None, "decided_at": None, "notes": "Awaiting exact-slice decision."}
        state["iterations"][0]["build"] = None
        state["iterations"][0]["proof"] = None
        state["iterations"][0]["handoff"] = None
        state["phase"] = "shape"
        state["status"] = "waiting-for-human"
        state["current_decision"] = "decide-build-gate"
        state["decision_history"][-1]["decision"] = "decide-build-gate"
        original_load = validator.load_json
        def load(path):
            return pending_shape if path == validator.SHAPE_EXAMPLE else original_load(path)
        with patch.object(validator, "load_json", side_effect=load):
            validator.validate_loop_state(state)
            state["current_decision"] = "shape-slice"
            state["decision_history"][-1]["decision"] = "shape-slice"
            with self.assertRaisesRegex(validator.ValidationError, "decide-build-gate"):
                validator.validate_loop_state(state)

    def test_assessed_result_requires_evidence(self):
        proof = copy.deepcopy(self.proof)
        proof["criteria_results"][0]["evidence"] = " "
        with self.assertRaisesRegex(validator.ValidationError, "require evidence"):
            validator.validate_proof_packet(proof, self.shape, self.build)

    def test_shape_cannot_change_initiative_identity(self):
        shape = copy.deepcopy(self.shape)
        shape["initiative_id"] = "another-initiative"
        with self.assertRaisesRegex(validator.ValidationError, "initiative_id"):
            validator.validate_shape_packet(shape)

    def test_stop_and_missing_evidence_cannot_be_build_ready(self):
        for direction in ("eliminate-or-stop", "insufficient-evidence"):
            with self.subTest(direction=direction):
                source = copy.deepcopy(self.packet)
                source["recommendation"]["direction"] = direction
                original_load = validator.load_json
                def load(path):
                    return source if path == validator.EXAMPLE_PACKET else original_load(path)
                with patch.object(validator, "load_json", side_effect=load), patch.object(validator, "validate_packet_data"):
                    with self.assertRaisesRegex(validator.ValidationError, "cannot authorize"):
                        validator.validate_shape_packet(self.shape)

    def test_legacy_identity_is_accepted_by_loop(self):
        source = copy.deepcopy(self.packet)
        source["schema_version"] = "2.1.0"
        del source["initiative_id"]
        del source["stated_ideal_process"]
        del source["target_process_design"]
        source["handoff"]["next_workflow"] = "discovery"
        state = copy.deepcopy(self.loop_state)
        state["iterations"] = []
        state["phase"] = "decide"
        state["status"] = "active"
        state["decision_history"] = [
            {"at": "2026-09-08T09:00:00Z", "decision": "continue-decision-discovery", "owner": None, "basis": "Legacy identity compatibility test."}
        ]
        state["current_decision"] = "continue-decision-discovery"
        state["next_action"] = "Continue decision discovery without rewriting the legacy source."
        state["initiative_id"] = validator.initiative_id_for(source, state["source_initiative"])
        self.assertTrue(state["initiative_id"].startswith("legacy-"))
        original_load = validator.load_json
        def load(path):
            return source if path == validator.EXAMPLE_PACKET else original_load(path)
        with patch.object(validator, "load_json", side_effect=load):
            validator.validate_loop_state(state)

    def test_loop_rejects_wrong_iteration_and_missing_shape(self):
        for change in ("wrong-iteration", "missing-shape"):
            with self.subTest(change=change):
                state = copy.deepcopy(self.loop_state)
                if change == "wrong-iteration":
                    state["loop_id"] = "different-loop"
                else:
                    state["iterations"][0]["shape"] = None
                with self.assertRaises(validator.ValidationError):
                    validator.validate_loop_state(state)

    def test_artifact_root_is_independent_of_package_location(self):
        with patch.object(validator, "ARTIFACT_ROOT", validator.LOOP_EXAMPLE):
            path = validator.validate_artifact_ref({"path": "shape.json", "sha256": validator.file_sha256(validator.SHAPE_EXAMPLE)}, "external project")
            self.assertEqual(path, validator.SHAPE_EXAMPLE)

    def test_generated_artifact_cli_from_another_working_directory(self):
        for kind, path in (("shape", validator.SHAPE_EXAMPLE), ("build", validator.BUILD_EXAMPLE), ("proof", validator.PROOF_EXAMPLE), ("handoff", validator.HANDOFF_EXAMPLE), ("loop", validator.LOOP_STATE_EXAMPLE)):
            with self.subTest(kind=kind):
                result = subprocess.run(
                    [sys.executable, str(ROOT / "scripts" / "validate.py"), "--artifact", str(path), "--kind", kind, "--project-root", str(ROOT)],
                    cwd=ROOT.parent, capture_output=True, text=True, check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
