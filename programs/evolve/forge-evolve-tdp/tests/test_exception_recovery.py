"""Tests for recovery across all 6 multi-format TDP exception classes (EXC-01 through EXC-06)."""

from forge_evolve import TDPExceptionRecoveryEngine


def test_exc01_2d_vs_3d_tolerance_conflict():
    engine = TDPExceptionRecoveryEngine()
    res = engine.resolve_exc01_tolerance_conflict(tol_3d_mm=0.030, tol_2d_mm=0.015)
    assert res["exception_code"] == "EXC-01"
    assert res["detected"] is True
    assert res["resolved"] is True
    assert res["governing_tolerance_mm"] == 0.015
    assert res["hitl_review_flagged"] is True


def test_exc02_non_watertight_iges_and_flipped_normal():
    engine = TDPExceptionRecoveryEngine()
    res = engine.resolve_exc02_non_watertight_iges(
        edge_gap_mm=0.042,
        raw_normal=(0.0, 0.0, -1.0),
        outward_ray=(0.0, 0.0, 1.0),
        sewing_tol_mm=0.1,
    )
    assert res["exception_code"] == "EXC-02"
    assert res["detected"] is True
    assert res["resolved"] is True
    assert res["edge_gap_stitched"] is True
    assert res["normal_reoriented"] is True
    assert res["repaired_normal_unit"] == (0.0, 0.0, 1.0)


def test_exc03_degraded_150dpi_blueprint_ocr():
    engine = TDPExceptionRecoveryEngine()
    res = engine.resolve_exc03_degraded_blueprint_ocr(dpi=150, hatching_overlap=True)
    assert res["exception_code"] == "EXC-03"
    assert res["detected"] is True
    assert res["resolved"] is True
    assert res["gabor_hatching_stripped"] is True
    assert res["binding_accuracy_pct"] >= 97.4


def test_exc04_occluded_cavity_standoff_collision():
    engine = TDPExceptionRecoveryEngine()
    res = engine.resolve_exc04_occluded_cavity_standoff(
        nominal_normal=(0.0, 0.0, 1.0),
        overhang_obstacle_dir=(0.5, 0.0, 0.866),
        max_incidence_deg=15.0,
    )
    assert res["exception_code"] == "EXC-04"
    assert res["detected"] is True
    assert res["resolved"] is True
    assert 0.0 < res["tilt_angle_deg"] <= 15.0


def test_exc05_8level_nested_bom_unit_and_mirror_mix():
    engine = TDPExceptionRecoveryEngine()
    res = engine.resolve_exc05_nested_bom_transform(
        local_pt_raw=(10.0, -5.0, 2.0),
        nesting_depth=8,
        units="INCH",
        mirrored=True,
    )
    assert res["exception_code"] == "EXC-05"
    assert res["detected"] is True
    assert res["resolved"] is True
    assert res["normalized_pt_mm"] == (-254.0, -127.0, 50.8)
    assert res["normal_handedness_preserved"] is True


def test_exc06_underconstrained_datum_reference_frame():
    engine = TDPExceptionRecoveryEngine()
    res = engine.resolve_exc06_underconstrained_datum(["A", "B"])
    assert res["exception_code"] == "EXC-06"
    assert res["detected"] is True
    assert res["resolved"] is True
    assert res["repaired_datums"] == ["A", "B", "C"]


def test_225_case_exception_suite_aggregate():
    engine = TDPExceptionRecoveryEngine()
    suite = engine.run_225_case_exception_suite()
    assert suite["total_injected"] == 225
    assert suite["detection_rate_pct"] >= 99.5
    assert len(suite["class_breakdown"]) == 6
