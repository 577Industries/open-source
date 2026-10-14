"""Tests for continuous 200 Hz 6-link swept-capsule collision avoidance and Datum-A 3-fiducial calibration."""

from forge_evolve import (
    AerospaceTDPIngestionEngine,
    AutonomousRoboticPathPlanner,
)


def test_continuous_200hz_6link_swept_capsule_clearance():
    engine = AerospaceTDPIngestionEngine(seed=42)
    _, faces, callouts = engine.generate_acp_wing_bulkhead_tdp()
    planner = AutonomousRoboticPathPlanner()
    stations, waypoints, stats = planner.plan_inspection_trajectory(faces, callouts)

    assert len(stations) == 2
    assert len(waypoints) == 18
    assert stats["collision_free_verified"] is True

    ccd = planner.verify_6link_swept_ccd(waypoints, faces, sample_rate_hz=200, duration_sec=68.5)
    assert ccd["sample_rate_hz"] == 200
    assert ccd["collision_free_verified"] is True
    assert ccd["optimized_min_clearance_mm"] >= 55.04
    assert ccd["optimized_min_clearance_mm"] > ccd["safety_envelope_floor_mm"]  # >= 45.0 mm
    for link_name, clearance_mm in ccd["per_link_min_clearance_mm"].items():
        assert clearance_mm >= 55.04, f"{link_name} violated 55.04 mm clearance floor"


def test_datum_a_3fiducial_mobile_base_calibration():
    planner = AutonomousRoboticPathPlanner()
    calib = planner.calibrate_datum_a_fiducials(n_trials=250, seed=42)

    assert calib["trials"] == 250
    assert calib["uncalibrated_p99_error_mm"] > 5.0
    assert calib["calibrated_p99_residual_mm"] < 0.025
    assert calib["meets_sub_25um_gate"] is True
