"""Tests for multi-vendor URTS robotic post-processors (FANUC, KUKA, ABB, ROS2) and CLI entry point."""

import json
from forge_evolve import (
    AerospaceTDPIngestionEngine,
    AutonomousRoboticPathPlanner,
)
from forge_evolve.cli import main as cli_main


def test_fanuc_kuka_abb_ros2_postprocessors():
    engine = AerospaceTDPIngestionEngine(seed=42)
    _, faces, callouts = engine.generate_acp_wing_bulkhead_tdp()
    planner = AutonomousRoboticPathPlanner()
    _, waypoints, _ = planner.plan_inspection_trajectory(faces, callouts)

    fanuc_ls = planner.export_fanuc_ls(waypoints)
    assert "/PROG  FORGE_EVOLVE_ACP7740_INSP" in fanuc_ls
    assert "/POS" in fanuc_ls
    assert "P[18:\"WP-006\"]" in fanuc_ls
    assert "P[11:\"WP-018\"]" in fanuc_ls
    assert "/END" in fanuc_ls

    kuka_krl = planner.export_kuka_krl(waypoints)
    assert "DEF FORGE_EVOLVE_ACP7740_INSP ( )" in kuka_krl
    assert "TRIGGER WHEN DISTANCE=0 DELAY=0 DO TRIG_" in kuka_krl
    assert kuka_krl.strip().endswith("END")

    abb_rapid = planner.export_abb_rapid(waypoints)
    assert "MODULE ForgeEvolve_ACP7740_Insp" in abb_rapid
    assert "MoveL [[" in abb_rapid
    assert "ENDMODULE" in abb_rapid

    ros2_json_str = planner.export_ros2_moveit_json(waypoints)
    ros2_payload = json.loads(ros2_json_str)
    assert ros2_payload["header"]["dds_security_profile"] == "SROS2_ENCLAVE_MTLS_AES256GCM"
    assert len(ros2_payload["joint_names"]) == 6
    assert len(ros2_payload["points"]) == 18


def test_cli_subcommands(capsys):
    assert cli_main(["ingest", "--step", "benchmarks/AF_ACP_7740_Bulkhead.stp"]) == 0
    out_ingest = json.loads(capsys.readouterr().out)
    assert out_ingest["brep_face_count"] == 18

    assert cli_main(["verify-ia", "--policy", "schemas/ia_compliance.rego"]) == 0
    out_ia = json.loads(capsys.readouterr().out)
    assert out_ia["ia_compliance_verdict"]["passed"] is True

    assert cli_main(["plan-path", "--dialect", "FANUC"]) == 0
    out_fanuc = capsys.readouterr().out
    assert "/PROG  FORGE_EVOLVE_ACP7740_INSP" in out_fanuc

    assert cli_main(["plan-path", "--dialect", "KUKA"]) == 0
    out_kuka = capsys.readouterr().out
    assert "DEF FORGE_EVOLVE_ACP7740_INSP" in out_kuka

    assert cli_main(["plan-path", "--dialect", "ROS2"]) == 0
    out_ros2 = capsys.readouterr().out
    assert "SROS2_ENCLAVE_MTLS_AES256GCM" in out_ros2

    for suite in ("nist-mbe", "d2p2-50", "redteam-ccd"):
        assert cli_main(["benchmark", "--suite", suite]) == 0
        out_bench = json.loads(capsys.readouterr().out)
        assert out_bench["suite"] == suite
