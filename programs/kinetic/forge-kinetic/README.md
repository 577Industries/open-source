<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/577Industries/.github/main/brand/out/wordmark-dark.svg">
  <img alt="577 Industries" height="44" src="https://raw.githubusercontent.com/577Industries/.github/main/brand/out/wordmark-light.svg">
</picture>

# forge-kinetic

`KINETIC` · [Product page on 577industries.com](https://www.577industries.com/kinetic) · [Interactive 3D WebGL Studio](https://www.577industries.com/kinetic/studio) · [Work reference](https://www.577industries.com/work/forge-kinetic)

**Physical AI, multi-sensor operating envelopes, redundant whole-body kinematics, 200 Hz 6-link swept-capsule collision avoidance, and hardware-agnostic Unified Robotic Task Specification (URTS) compilation.**

[![ci](https://img.shields.io/github/actions/workflow/status/577Industries/forge-kinetic/ci.yml?style=flat-square&label=ci)](https://github.com/577Industries/forge-kinetic/actions/workflows/ci.yml)
[![license](https://img.shields.io/badge/license-Apache_2.0-blue?style=flat-square)](LICENSE)

## Core Architecture & Domain Extensions

`forge-kinetic` is the foundational physical AI and robotics platform developed by **577 Industries Inc.** It connects sensor operating-envelope analysis with real-time GPU/CPU Signed Distance Field (SDF) collision avoidance and multi-vendor industrial robot controller generation:

```text
Sensor Envelope & Occlusion Analysis -> 3D Signed Distance Field (SDF)
  -> Redundant 6-DOF + AGV Whole-Body IK -> 200 Hz 6-Link Swept-Capsule CCD
  -> URTS Intermediate Representation -> Native FANUC / KUKA / ABB / SROS2 + HITL Handover
```

### Official Domain Extensions & Research Labs

| Extension / Lab | Program / Domain Scope | Capabilities Added |
|---|---|---|
| [`577Industries/forge-kinetic-mbd`](https://github.com/577Industries/forge-kinetic-mbd) | U.S. Air Force / Space Force `DAF27BZ01-DV012` (Autonomous TDP-to-Robot Compilation) | Multimodal 2D/3D ASME Y14.5 GD&T topological binding (99.1% precision on NIST MBE PMI `FTC-01..11`), 6D reachability-inversion mobile base clustering, Datum-A 3-fiducial calibration (<0.025 mm residual), and No-Code depot workbench |
| [IRIS Perception Lab](https://www.577industries.com/government/labs/iris) | Sparse-Data Sensor Fusion Research | Held-out environmental condition evaluation under limited labeling budgets |

## Quickstart (Offline, Deterministic)

```bash
pip install -e ".[dev]"
pytest -v
forge-kinetic envelope --standoff-mm 780 --occluder-offset 0.18
forge-kinetic swept-ccd --freq-hz 200
forge-kinetic urts-compile --dialect FANUC
forge-kinetic urts-compile --dialect KUKA
```

## Reading Order

1. [`companion/companion.md`](companion/companion.md) — Maps core robotics platform contracts to files and tests.
2. [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) — Instructions to reproduce every verification output offline.
3. [`EXCLUSIONS.md`](EXCLUSIONS.md) — Publication boundary (synthetic geometry and simulation artifacts).
