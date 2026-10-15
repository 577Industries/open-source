"""Tests for CTDP-G v2.4, MIL-STD-31000B / ITAR / CMMC L2 OPA gates, SHA-256 Merkle-DAG lineage, and CRDT reconciliation."""

import dataclasses
from pathlib import Path

from forge_evolve import (
    AerospaceTDPIngestionEngine,
    CanonicalTDPPayloadSchema,
    ClosedLoopAISustainmentEngine,
    CRDTStateEntry,
    ZeroTrustMerkleLedger,
)


REPO_ROOT = Path(__file__).resolve().parent.parent


def test_six_opa_ia_compliance_gates_pass_100pct():
    engine = AerospaceTDPIngestionEngine(seed=42)
    _, faces, callouts = engine.generate_acp_wing_bulkhead_tdp()
    ledger = ZeroTrustMerkleLedger(package_id="TDP-DAF-ACP-7740-REV-C")
    policy_path = REPO_ROOT / "schemas" / "ia_compliance.rego"

    verdict = ledger.evaluate_ia_compliance(faces, callouts, rego_policy_path=policy_path)
    assert verdict["passed"] is True
    assert verdict["rules_evaluated"] == 6
    assert verdict["mil_std_31000b_score"] == 99.4
    assert verdict["bound_feature_coverage_pct"] == 100.0
    for gate_name, gate_ok in verdict["rule_results"].items():
        assert gate_ok is True, f"OPA gate {gate_name} failed"


def test_adversarial_zero_trust_blocks_unauthorized_subjects():
    engine = AerospaceTDPIngestionEngine(seed=42)
    _, faces, callouts = engine.generate_acp_wing_bulkhead_tdp()
    ledger = ZeroTrustMerkleLedger(package_id="TDP-DAF-ACP-7740-REV-C")

    # Foreign national attempt
    fn_verdict = ledger.evaluate_ia_compliance(
        faces,
        callouts,
        subject={
            "us_person_verified": False,
            "cmmc_enclave_level": 2,
            "role": "AFMC_SUSTAINMENT_ENG",
            "mtls_spiffe_verified": True,
            "spiffe_id": "spiffe://partner.org/client",
        },
    )
    assert fn_verdict["passed"] is False
    assert fn_verdict["rule_results"]["EXPORT_CONTROL_ABAC_TAGGED"] is False

    # Non-CMMC Level 1 enclave attempt
    cmmc_verdict = ledger.evaluate_ia_compliance(
        faces,
        callouts,
        subject={
            "us_person_verified": True,
            "cmmc_enclave_level": 1,
            "role": "AFMC_SUSTAINMENT_ENG",
            "mtls_spiffe_verified": True,
            "spiffe_id": "spiffe://subtier.com/cell",
        },
    )
    assert cmmc_verdict["passed"] is False
    assert cmmc_verdict["rule_results"]["EXPORT_CONTROL_ABAC_TAGGED"] is False

    # Missing SPIFFE mTLS identity
    mtls_verdict = ledger.evaluate_ia_compliance(
        faces,
        callouts,
        subject={
            "us_person_verified": True,
            "cmmc_enclave_level": 2,
            "role": "ALC_ROBOT_CELL_CONTROLLER",
            "mtls_spiffe_verified": False,
            "spiffe_id": "http://unverified.local",
        },
    )
    assert mtls_verdict["passed"] is False
    assert mtls_verdict["rule_results"]["NIST_800_207_SPIFFE_MTLS_IDENTITY"] is False


def test_deterministic_merkle_dag_lineage_and_pydantic_schema():
    engine_a = AerospaceTDPIngestionEngine(seed=42)
    _, faces_a, callouts_a = engine_a.generate_acp_wing_bulkhead_tdp()
    sust_a = ClosedLoopAISustainmentEngine(seed=101)
    anomalies_a, _ = sust_a.inspect_and_evaluate(faces_a, callouts_a)

    ledger_a = ZeroTrustMerkleLedger(package_id="TDP-DAF-ACP-7740-REV-C")
    verdict_a = ledger_a.evaluate_ia_compliance(faces_a, callouts_a)
    c1_a = ledger_a.commit_state("AS_DESIGNED", "FLEET_BASELINE", "spiffe://example.invalid/plm/teamcenter-exporter", faces_a, callouts_a)
    c2_a = ledger_a.commit_state("AS_BUILT", "TAIL-SYNTH-042", "spiffe://example.invalid/qa/cmm-cell-01", faces_a, callouts_a)
    c3_a = ledger_a.commit_state("AS_SUSTAINED", "TAIL-SYNTH-042", "spiffe://example.invalid/alc/mobile-manipulator-04", faces_a, callouts_a, anomalies_a)

    # Second independent run must produce identical SHA-256 Merkle roots and commit hashes
    engine_b = AerospaceTDPIngestionEngine(seed=42)
    _, faces_b, callouts_b = engine_b.generate_acp_wing_bulkhead_tdp()
    sust_b = ClosedLoopAISustainmentEngine(seed=101)
    anomalies_b, _ = sust_b.inspect_and_evaluate(faces_b, callouts_b)

    ledger_b = ZeroTrustMerkleLedger(package_id="TDP-DAF-ACP-7740-REV-C")
    c1_b = ledger_b.commit_state("AS_DESIGNED", "FLEET_BASELINE", "spiffe://example.invalid/plm/teamcenter-exporter", faces_b, callouts_b)
    c2_b = ledger_b.commit_state("AS_BUILT", "TAIL-SYNTH-042", "spiffe://example.invalid/qa/cmm-cell-01", faces_b, callouts_b)
    c3_b = ledger_b.commit_state("AS_SUSTAINED", "TAIL-SYNTH-042", "spiffe://example.invalid/alc/mobile-manipulator-04", faces_b, callouts_b, anomalies_b)

    assert c1_a["commit_hash"] == c1_b["commit_hash"]
    assert c2_a["commit_hash"] == c2_b["commit_hash"]
    assert c3_a["commit_hash"] == c3_b["commit_hash"]
    assert c2_a["parent_commit_hash"] == c1_a["commit_hash"]
    assert c3_a["parent_commit_hash"] == c2_a["commit_hash"]
    assert c3_a["merkle_root"] != c2_a["merkle_root"]

    # Validate against Pydantic v2 schema
    validated = CanonicalTDPPayloadSchema(
        package_id="TDP-DAF-ACP-7740-REV-C",
        ia_compliance_verdict=verdict_a,
        merkle_commits=ledger_a.commits,
        faces=[dataclasses.asdict(f) for f in faces_a],
        callouts=[dataclasses.asdict(c) for c in callouts_a],
    )
    assert validated.schema_version == "2.4.0"
    assert len(validated.faces) == 18


def test_crdt_multi_depot_branch_reconciliation():
    ledger = ZeroTrustMerkleLedger(package_id="TDP-DAF-ACP-7740-REV-C")

    depot_robins = [
        CRDTStateEntry("TAIL-SYNTH-042", "F-103", 10, "ROBINS_ALC", 0.028, "MRB_REVIEW", "sig-robins-10"),
        CRDTStateEntry("TAIL-SYNTH-042", "F-108", 11, "ROBINS_ALC", 0.082, "REWORK", "sig-robins-11"),
    ]
    depot_ogden = [
        CRDTStateEntry("TAIL-SYNTH-042", "F-103", 14, "OGDEN_ALC", 0.011, "ACCEPT", "sig-ogden-14"),
        CRDTStateEntry("TAIL-SYNTH-042", "F-118", 12, "OGDEN_ALC", 0.031, "REWORK", "sig-ogden-12"),
    ]

    merge_ab = ledger.reconcile_crdt_branches(depot_robins, depot_ogden)
    merge_ba = ledger.reconcile_crdt_branches(depot_ogden, depot_robins)
    merge_aa = ledger.reconcile_crdt_branches(depot_robins, depot_robins)

    # Commutativity & Idempotence
    assert merge_ab["reconciled_merkle_root"] == merge_ba["reconciled_merkle_root"]
    assert merge_ab["conflict_free"] is True
    assert merge_ab["merged_entry_count"] == 3
    assert merge_ab["merge_latency_ms"] < 4.5
    assert merge_aa["merged_entry_count"] == 2

    # F-103 must resolve to Ogden ALC's newer Lamport timestamp (14 > 10)
    f103_entry = next(e for e in merge_ab["merged_entries"] if e["face_uid"] == "F-103")
    assert f103_entry["depot_id"] == "OGDEN_ALC"
    assert f103_entry["disposition"] == "ACCEPT"
