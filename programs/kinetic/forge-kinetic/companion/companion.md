# Reviewer Companion — `forge-kinetic` Core Robotics Platform

| Platform Subsystem | Module | Verification Test | Output Artifact |
|---|---|---|---|
| 1. Sensor Operating Envelope & Occlusion | `src/forge_kinetic/perception.py` | `tests/test_forge_kinetic_core.py::test_sensor_occlusion_envelope` | `results/sensor-envelope.json` |
| 2. Redundant 6-DOF + AGV Inverse Kinematics | `src/forge_kinetic/kinematics.py` | `tests/test_forge_kinetic_core.py::test_redundant_whole_body_ik` | `results/ik-posture.json` |
| 3. 200 Hz 6-Link Swept-Capsule CCD (`>= 55.04 mm`) | `src/forge_kinetic/ccd.py` | `tests/test_forge_kinetic_core.py::test_swept_capsule_clearance_floor` | `results/swept-ccd-profile.json` |
| 4. URTS Multi-Vendor Post-Processors (`FANUC`, `KUKA`, `ABB`, `SROS2`) | `src/forge_kinetic/urts.py` | `tests/test_forge_kinetic_core.py::test_urts_multi_vendor_dialects` | `results/urts-fanuc.txt` |
