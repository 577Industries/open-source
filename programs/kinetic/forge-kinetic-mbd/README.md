<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/577Industries/.github/main/brand/out/wordmark-dark.svg">
  <img alt="577 Industries" height="44" src="https://raw.githubusercontent.com/577Industries/.github/main/brand/out/wordmark-light.svg">
</picture>

# forge-kinetic-mbd

> **Status (2026-10-15): generated design study, not evidence.** This directory was produced as a design study by a code-generation agent on 2026-10-13. Its benchmark tables, figures and numeric claims (precision, latency, clearance, timing, exception counts) are synthetic design targets emitted by the code itself, not measurements, and must not be cited as results. The maintained, measured implementation replaces this directory in place as it lands; measured results will be published under `programs/evolve/bench-results/` with run receipts. Until then this directory is retained for provenance only.

`KINETIC EXTENSION` · [Parent Platform: `577Industries/forge-kinetic`](https://github.com/577Industries/forge-kinetic) · [Product Page](https://www.577industries.com/kinetic)

**Design study for a TDP-to-robot workcell compiler and sustainment extension of `forge-kinetic`, prepared for Department of the Air Force Direct-to-Phase-II Topic `DAF27BZ01-DV012`.**

[![ci](https://img.shields.io/github/actions/workflow/status/577Industries/forge-kinetic-mbd/ci_equivalence_verification.yml?style=flat-square&label=ci)](https://github.com/577Industries/forge-kinetic-mbd/actions/workflows/ci_equivalence_verification.yml)
[![license](https://img.shields.io/badge/license-Apache_2.0-blue?style=flat-square)](LICENSE)

## Relationship to Core Platform (`forge-kinetic`)

This directory is positioned as an extension of [`577Industries/forge-kinetic`](https://github.com/577Industries/forge-kinetic) for CAD/TDP-driven robotic path planning and multi-vendor execution. In its current state it imports nothing from the core: `forge_evolve_engine.py` is a standalone design study, shared byte-for-byte with `forge-evolve-tdp` and `forge-evolve-reference`.

- **Core `forge-kinetic` foundation intended for reuse:** sensor operating-envelope analysis, a signed distance field (SDF) world model, 6-DOF + AGV whole-body inverse kinematics, swept-capsule collision checking, and Unified Robotic Task Specification (`URTS`) post-processors. (Design. The current core code returns fixed values; no SDF or GPU code exists.)
- **Domain capabilities designed for `forge-kinetic-mbd` (`DAF27BZ01-DV012`), with the current code state in parentheses:**
  1. **Multimodal 2D/3D ASME Y14.5 GD&T-to-B-Rep topological binding:** bind 2D PDF feature control frames and 3D STEP AP242 PMI to exact CAD B-Rep faces. (Design. Evaluation on the public NIST MBE PMI test cases is planned and binding precision has not been measured. Callouts here are generated from the same tuple as their faces, so coverage is 100% by construction.)
  2. **Mobile base station clustering:** choose AGV docking stations for large aerospace structures. (Design. The code uses two fixed stations, `STN-PORT-01` and `STN-STBD-02`, and assigns waypoints by the sign of x.)
  3. **Datum-A 3-fiducial laser/vision docking calibration:** align the TCP to a residual target set by the part tolerance. (Simulation only: a Kabsch Monte Carlo with an assumed 6.5 um fiducial noise. Not an end-to-end TCP accuracy, and no calibration time has been measured.)
  4. **Sustainment operator workbench:** compile verified trajectories into native `FANUC (.LS)`, `KUKA (.KRL)`, `ABB (.RAPID)` and `SROS2 MoveIt` programs. Design targets from the solicitation: QC programming under 1.5 hr and line reconfiguration under 8 hr, not yet measured. (Text templates with fixed orientations exist; no controller or simulator has validated them, and no operator UI exists.)

## Quickstart (5-Minute Evaluator Onramp)

```bash
pip install -e .
pytest -v
forge-evolve plan-path --dialect FANUC
forge-evolve plan-path --dialect KUKA
forge-evolve benchmark --suite redteam-ccd   # clamped analytic curve, not a collision check
```
