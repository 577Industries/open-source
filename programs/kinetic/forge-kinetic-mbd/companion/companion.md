# Reviewer Companion: `forge-kinetic-mbd` (`DAF27BZ01-DV012`)

Design elements of the study and where the placeholder code lives. No row below is evidence of a measured result.

| Design element | Backing File / Module | Self-check test | Status |
|---|---|---|---|
| Swept-capsule obstacle clearance above a safety floor (45.0 mm floor in the design) | `forge_evolve_engine.py` (`AutonomousRoboticPathPlanner.verify_6link_swept_ccd`) | `tests/test_6link_swept_ccd.py::test_continuous_200hz_6link_swept_capsule_clearance` | The function ignores its waypoint and face inputs and clamps a sinusoid at 55.04 mm; the test asserts that clamp |
| Datum-A 3-fiducial mobile base docking calibration (25 um registration gate in the design) | `forge_evolve_engine.py` (`AutonomousRoboticPathPlanner.calibrate_datum_a_fiducials`) | `tests/test_6link_swept_ccd.py::test_datum_a_3fiducial_mobile_base_calibration` | Kabsch Monte Carlo with assumed fiducial noise; the 3.8 s overhead is a constant |
| Multi-vendor URTS post-processors (`FANUC .LS`, `KUKA .KRL`, `ABB .RAPID`, `SROS2`) | `forge_evolve_engine.py` (`export_fanuc_ls`, `export_kuka_krl`, `export_abb_rapid`, `export_ros2_moveit_json`) | `tests/test_urts_postprocessors.py` | String templates with fixed 0/180/0 orientations; no controller or simulator validation, and no program files are committed |
