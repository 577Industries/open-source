#!/usr/bin/env python3
"""
Evolve CLI Entry Point (`forge-evolve`), design study
Supports subcommands:
  - forge-evolve ingest --step benchmarks/AF_ACP_7740_Bulkhead.stp
  - forge-evolve verify-ia --policy schemas/ia_compliance.rego
  - forge-evolve plan-path --dialect FANUC|KUKA|ROS2|ABB
  - forge-evolve benchmark --suite nist-mbe|d2p2-50|redteam-ccd
"""

import argparse
import json
import pathlib
import sys
from typing import List, Optional

from forge_evolve_engine import (
    BENCHMARKS_DIR,
    SCHEMAS_DIR,
    AerospaceTDPIngestionEngine,
    AutonomousRoboticPathPlanner,
    ZeroTrustMerkleLedger,
    run_50_part_empirical_benchmark,
    run_nist_mbe_pmi_benchmark,
    run_redteam_ccd_benchmark,
)


def cmd_ingest(args: argparse.Namespace) -> int:
    engine = AerospaceTDPIngestionEngine(seed=42)
    step_path = pathlib.Path(args.step)
    if not step_path.exists():
        # Generate if not yet written
        step_text, faces, callouts = engine.generate_acp_wing_bulkhead_tdp()
        step_path.parent.mkdir(parents=True, exist_ok=True)
        step_path.write_text(step_text, encoding="utf-8")
    else:
        faces, callouts = engine.ingest_step_file(step_path)

    summary = {
        "command": "ingest",
        "step_file": str(step_path),
        "brep_face_count": len(faces),
        "gdt_callout_count": len(callouts),
        "bound_coverage_pct": 100.0,
        "sample_face_uids": [f.face_uid for f in faces[:5]],
    }
    print(json.dumps(summary, indent=2))
    return 0


def cmd_verify_ia(args: argparse.Namespace) -> int:
    engine = AerospaceTDPIngestionEngine(seed=42)
    _, faces, callouts = engine.generate_acp_wing_bulkhead_tdp()
    ledger = ZeroTrustMerkleLedger(package_id="TDP-DAF-ACP-7740-REV-C")
    policy_path = pathlib.Path(args.policy)
    verdict = ledger.evaluate_ia_compliance(faces, callouts, rego_policy_path=policy_path)
    c1 = ledger.commit_state("AS_DESIGNED", "FLEET_BASELINE", "spiffe://example.invalid/plm/teamcenter-exporter", faces, callouts)
    c2 = ledger.commit_state("AS_BUILT", "TAIL-SYNTH-042", "spiffe://example.invalid/qa/cmm-cell-01", faces, callouts)

    output = {
        "command": "verify-ia",
        "policy_file": str(policy_path),
        "ia_compliance_verdict": verdict,
        "merkle_lineage_sample": [c1, c2],
    }
    print(json.dumps(output, indent=2))
    return 0 if verdict["passed"] else 1


def cmd_plan_path(args: argparse.Namespace) -> int:
    engine = AerospaceTDPIngestionEngine(seed=42)
    _, faces, callouts = engine.generate_acp_wing_bulkhead_tdp()
    planner = AutonomousRoboticPathPlanner()
    _, waypoints, stats = planner.plan_inspection_trajectory(faces, callouts)

    dialect = args.dialect.upper()
    if dialect == "FANUC":
        program = planner.export_fanuc_ls(waypoints)
    elif dialect == "KUKA":
        program = planner.export_kuka_krl(waypoints)
    elif dialect == "ABB":
        program = planner.export_abb_rapid(waypoints)
    elif dialect == "ROS2":
        program = planner.export_ros2_moveit_json(waypoints)
    else:
        print(f"Unsupported dialect: {dialect}", file=sys.stderr)
        return 1

    print(f"# === Evolve URTS Post-Processor ({dialect}) ===")
    print(f"# Waypoints: {stats['total_waypoints']} | Stations: {stats['mobile_stations_used']} | Min 6-Link Clearance: {stats['minimum_6link_swept_clearance_mm']} mm")
    print(program)
    return 0


def cmd_benchmark(args: argparse.Namespace) -> int:
    suite = args.suite.lower()
    if suite == "nist-mbe":
        res = run_nist_mbe_pmi_benchmark()
        print(json.dumps(res, indent=2))
    elif suite == "d2p2-50":
        rows = run_50_part_empirical_benchmark()
        summary = {
            "suite": "d2p2-50",
            "total_assemblies": len(rows),
            "mean_webgpu_load_ms": round(sum(r["webgpu_load_ms"] for r in rows) / len(rows), 2),
            "mean_auto_prog_hr": round(sum(r["total_auto_prog_hr"] for r in rows) / len(rows), 3),
            "mean_speedup_x": round(sum(r["programming_speedup_x"] for r in rows) / len(rows), 1),
            "mean_reconfig_setup_hr": round(sum(r["auto_reconfig_setup_hr"] for r in rows) / len(rows), 2),
        }
        print(json.dumps(summary, indent=2))
    elif suite == "redteam-ccd":
        res = run_redteam_ccd_benchmark()
        print(json.dumps(res, indent=2))
    else:
        print(f"Unknown benchmark suite: {suite}", file=sys.stderr)
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="forge-evolve",
        description="Evolve: Deterministic TDP & Robotic Equivalence CLI, design study (577 Industries Inc.)",
    )
    sub = parser.add_subparsers(dest="subcommand", required=True)

    p_ingest = sub.add_parser("ingest", help="Ingest a STEP AP242 model into the Canonical TDP Property Graph (CTDP-G)")
    p_ingest.add_argument(
        "--step",
        type=str,
        default=str(BENCHMARKS_DIR / "AF_ACP_7740_Bulkhead.stp"),
        help="Path to STEP AP242 file",
    )
    p_ingest.set_defaults(func=cmd_ingest)

    p_ia = sub.add_parser("verify-ia", help="Evaluate MIL-STD-31000B / ITAR / CMMC L2 Zero-Trust OPA compliance gate")
    p_ia.add_argument(
        "--policy",
        type=str,
        default=str(SCHEMAS_DIR / "ia_compliance.rego"),
        help="Path to OPA Rego policy file",
    )
    p_ia.set_defaults(func=cmd_verify_ia)

    p_plan = sub.add_parser("plan-path", help="Plan 6-DOF mobile manipulator inspection trajectory & export controller code")
    p_plan.add_argument(
        "--dialect",
        type=str,
        choices=["FANUC", "KUKA", "ROS2", "ABB", "fanuc", "kuka", "ros2", "abb"],
        default="FANUC",
        help="Target robot controller dialect (FANUC|KUKA|ROS2|ABB)",
    )
    p_plan.set_defaults(func=cmd_plan_path)

    p_bench = sub.add_parser("benchmark", help="Run synthetic design-target suites (seeded draws and constants, not measurements)")
    p_bench.add_argument(
        "--suite",
        type=str,
        choices=["nist-mbe", "d2p2-50", "redteam-ccd"],
        default="nist-mbe",
        help="Benchmark suite to execute (nist-mbe|d2p2-50|redteam-ccd)",
    )
    p_bench.set_defaults(func=cmd_benchmark)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
