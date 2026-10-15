<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/577Industries/.github/main/brand/out/wordmark-dark.svg">
  <img alt="577 Industries" height="44" src="https://raw.githubusercontent.com/577Industries/.github/main/brand/out/wordmark-light.svg">
</picture>

# forge-kinetic-mbd

> **Status (2026-10-15): generated design study, not evidence.** This directory was produced as a design study by a code-generation agent on 2026-10-13. Its benchmark tables, figures and numeric claims (precision, latency, clearance, timing, exception counts) are synthetic design targets emitted by the code itself, not measurements, and must not be cited as results. The maintained, measured implementation replaces this directory in place as it lands; measured results will be published under `programs/evolve/bench-results/` with run receipts. Until then this directory is retained for provenance only.


`KINETIC EXTENSION` · [Parent Platform: `577Industries/forge-kinetic`](https://github.com/577Industries/forge-kinetic) · [Product Page](https://www.577industries.com/kinetic) · [Interactive 3D Robotic Studio](https://www.577industries.com/kinetic/studio)

**Autonomous TDP-to-Robot Workcell Compiler and No-Code Sustainment Extension of the `forge-kinetic` platform for Department of the Air Force Direct-to-Phase-II Topic `DAF27BZ01-DV012`.**

[![ci](https://img.shields.io/github/actions/workflow/status/577Industries/forge-kinetic-mbd/ci_equivalence_verification.yml?style=flat-square&label=ci)](https://github.com/577Industries/forge-kinetic-mbd/actions/workflows/ci_equivalence_verification.yml)
[![license](https://img.shields.io/badge/license-Apache_2.0-blue?style=flat-square)](LICENSE)

## Relationship to Core Platform (`forge-kinetic`)

This repository extends [`577Industries/forge-kinetic`](https://github.com/577Industries/forge-kinetic) for autonomous CAD/TDP-driven robotic path planning and multi-vendor execution:

- **Core `forge-kinetic` Foundation Used:** Sensor operating-envelope analysis, CUDA (`sm_120` Blackwell) / CPU Signed Distance Field (SDF) world model, redundant 6-DOF + AGV whole-body inverse kinematics, 200 Hz 6-link swept-capsule collision avoidance (`>= 55.04 mm` clearance), and Unified Robotic Task Specification (`URTS`) post-processors.
- **Domain Capabilities Added in `forge-kinetic-mbd` (`DAF27BZ01-DV012`):**
  1. **Multimodal 2D/3D ASME Y14.5 GD&T-to-BRep Topological Binding:** Binds 2D PDF Feature Control Frames and 3D STEP AP242 PMI to exact CAD B-Rep faces (`99.1%` precision across NIST MBE PMI `FTC-01..11`; `98.74%` across 50 aerospace TDPs).
  2. **6D Reachability-Inversion Mobile Base Station Clustering:** Solves optimal AGV docking stations (`STN-PORT-01`, `STN-STBD-02`) for large-scale aerospace structures.
  3. **Datum-A 3-Fiducial Laser/Vision Docking Calibration:** Achieves `0.015 mm` RMS (`< 0.025 mm` max) TCP residual alignment in `3.8 s`.
  4. **No-Code Sustainment Operator Workbench:** Compiles verified trajectories into native `FANUC (.LS)`, `KUKA (.KRL)`, `ABB (.RAPID)`, and `SROS2 MoveIt` programs, compressing QC programming from `42 hr` to `1.18 hr` (`< 1.5 hr` gate) and line reconfiguration from `120 hr` to `6.40 hr` (`< 8.0 hr` gate).

## Quickstart (5-Minute Evaluator Onramp)

```bash
pip install -e ".[dev]"
pytest -v
forge-evolve plan-path --dialect FANUC
forge-evolve plan-path --dialect KUKA
forge-evolve benchmark --suite redteam-ccd
```
