"""Unit & integration tests for the 577 Industries Kinetic Core Robotics Platform."""
from forge_kinetic import (
    compute_sensor_envelope,
    solve_whole_body_ik,
    evaluate_6link_swept_ccd,
    compile_urts_program,
)

def test_sensor_occlusion_envelope():
    nom = compute_sensor_envelope(780.0, 42.0, 0.28)
    assert nom.hitl_takeover_required is False
    occ = compute_sensor_envelope(780.0, 42.0, 0.05)
    assert occ.hitl_takeover_required is True

def test_redundant_whole_body_ik():
    pos = solve_whole_body_ik([1420.0, -310.0, 880.0], "STN-PORT-01")
    assert len(pos.joint_angles_deg) == 6
    assert pos.tcp_residual_mm < 0.025

def test_swept_capsule_clearance_floor():
    ccd = evaluate_6link_swept_ccd(200, 45.0)
    assert ccd.min_clearance_kinetic_mm >= 55.04
    assert ccd.kinetic_collisions == 0
    assert ccd.naive_collisions > 0

def test_urts_multi_vendor_dialects():
    for d in ("FANUC", "KUKA", "ABB", "ROS2"):
        out = compile_urts_program(d)
        assert "55.04" in out
