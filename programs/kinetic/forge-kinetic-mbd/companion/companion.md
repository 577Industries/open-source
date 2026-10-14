# Reviewer Companion — `forge-kinetic-mbd` (`DAF27BZ01-DV012`)

| Proposal Claim (DAF27BZ01-DV012) | Backing File / Module | Verification Test |
|---|---|---|
| 200 Hz 6-Link Swept-Capsule Obstacle Clearance (`>= 55.04 mm` vs `45.0 mm` floor) | `forge_evolve_engine.py`, `run_adversarial_benchmarks.py` | `tests/test_6link_swept_ccd.py::test_swept_capsule_clearance_above_safety_floor` |
| Datum-A 3-Fiducial Mobile Base Docking Calibration (`0.015 mm < 0.025 mm` gate) | `run_adversarial_benchmarks.py` | `tests/test_6link_swept_ccd.py::test_3fiducial_mobile_base_docking_residual` |
| Multi-Vendor URTS Post-Processors (`FANUC .LS`, `KUKA .KRL`, `ABB .RAPID`, `SROS2`) | `forge_evolve_engine.py`, `benchmarks/AF_ACP_7740_FANUC.ls`, `benchmarks/AF_ACP_7740_KUKA.src` | `tests/test_urts_postprocessors.py` |
