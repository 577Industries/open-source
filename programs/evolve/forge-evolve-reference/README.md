# Forge Evolve & Forge Kinetic — Deterministic Engineering, TDP & Robotic Equivalence Reference

> **Status (2026-10-15): generated design study, not evidence.** This directory was produced as a design study by a code-generation agent on 2026-10-13. Its benchmark tables, figures and numeric claims (precision, latency, clearance, timing, exception counts) are synthetic design targets emitted by the code itself, not measurements, and must not be cited as results. The maintained, measured implementation replaces this directory in place as it lands; measured results will be published under `programs/evolve/bench-results/` with run receipts. Until then this directory is retained for provenance only.


[![Forge Evolve Equivalence & D2P2 Verification CI](https://github.com/577Industries/forge-evolve-reference/actions/workflows/ci_equivalence_verification.yml/badge.svg)](https://github.com/577Industries/forge-evolve-reference/actions/workflows/ci_equivalence_verification.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-0D9488.svg)](https://www.python.org/)
[![PQC FIPS 203](https://img.shields.io/badge/crypto-ML--KEM--768%20%2B%20AES--256--GCM-0F2942.svg)](https://www.577industries.com/evolve)

**Move the baseline forward. Preserve what matters.**  
*Public Reference Implementation by [577 Industries Inc.](https://www.577industries.com) (Columbus, Ohio | PI: Dr. Thomas G. Waweru)*  
*Interactive WebGL2 3D Studios: [Evolve 3D MBD Studio (`/evolve/studio`)](https://www.577industries.com/evolve/studio) · [Kinetic 3D Workcell Studio (`/kinetic/studio`)](https://www.577industries.com/kinetic/studio)*

---

## Modular Product & Domain Extension Repositories

In addition to this unified end-to-end benchmark bundle (`forge-evolve-reference`), the architecture is decomposed into two standalone core product engines and their domain-specific defense extensions:

| Repository | Layer | Scope & Primary Surface |
| :--- | :--- | :--- |
| [**`577Industries/forge-evolve`**](https://github.com/577Industries/forge-evolve) | **Core Product (`Evolve`)** | Deterministic Code & Artifact Modernization Engine (`Discovery → CLAR IR → Planner → Differential Equivalence Oracle → Hashchain Provenance`). [`/evolve`](https://www.577industries.com/evolve) |
| [**`577Industries/forge-evolve-tdp`**](https://github.com/577Industries/forge-evolve-tdp) | **Evolve Extension (`DAF27BZ01-DV008`)** | **Forge Evolve TDP** — Zero-Trust STEP AP242 / 2D PDF MBD modernization, `ML-KEM-768` + `AES-256-GCM` Merkle-DAG ledger, `<300 ms` WebGPU streaming, and 3D PointNet++ NDI sustainment AI. [`/work/forge-evolve-tdp`](https://www.577industries.com/work/forge-evolve-tdp) |
| [**`577Industries/forge-evolve-tmpc`**](https://github.com/577Industries/forge-evolve-tmpc) | **Evolve Extension (`DON26BZ01-NV013`)** | C#/.NET Mission-Planning Code Modernization & Split-Disposition Verification Harness. [`/work/forge-evolve-tmpc`](https://www.577industries.com/work/forge-evolve-tmpc) |
| [**`577Industries/forge-kinetic`**](https://github.com/577Industries/forge-kinetic) | **Core Product (`Kinetic`)** | Physical AI, Multi-Sensor Operating Envelopes, 6-DOF + AGV Whole-Body IK, 200 Hz 6-Link Swept-Capsule SDF Collision Avoidance, & Multi-Vendor URTS Post-Processors (`FANUC`, `KUKA`, `ABB`, `SROS2`). [`/kinetic`](https://www.577industries.com/kinetic) |
| [**`577Industries/forge-kinetic-mbd`**](https://github.com/577Industries/forge-kinetic-mbd) | **Kinetic Extension (`DAF27BZ01-DV012`)** | **Forge Kinetic** Autonomous TDP-to-Robot Workcell Compiler — 99.1% NIST MBE PMI topological binding, 2-station AGV reachability clustering, Datum-A 3-fiducial docking calibration (`0.0145 mm` p99 TCP residual), and no-code sustainment interface. [`/work/forge-kinetic-mbd`](https://www.577industries.com/work/forge-kinetic-mbd) |

---

## Overview

**Forge Evolve** (code & technical data modernization) and **Forge Kinetic** (physical AI & autonomous robotic execution) enforce a deterministic equivalence contract across software codebases, Model-Based Definition (MBD) Technical Data Packages (TDPs), and multi-axis robotic workcells.

Whether migrating legacy flight/scientific code (`Fortran`, `Ada`, `C++`, `COBOL`, `.NET`), modernizing heterogeneous 3D/2D TDPs into a Zero-Trust configuration ledger (**Forge Evolve TDP**), or compiling GD&T tolerances into collision-free multi-vendor robotic inspection trajectories (**Forge Kinetic**), **small differences can change the contract**. A signed angle, surface normal vector, or bilateral tolerance zone can describe the same nominal geometry and still break a downstream rule or cause a physical link collision.

Both platforms enforce a three-stage verification contract across every artifact:
1. **`01 / A Behavioral & Geometric Baseline`:** Parse 3D B-Rep topology (`STEP AP242`, `IGES`), 2D engineering blueprints (`PDF`), and source specifications into the **Canonical TDP Property Graph (`CTDP-G v2.4`)**, locking datum reference frames `[A|B|C]`, tolerances, and Attribute-Based Access Control (ABAC) security scopes.
2. **`02 / A Reviewed Working Slice`:** Transform bounded modules into progressive WebGPU BVH-Octree mesh streams (`<300 ms` time-to-first-frame) and **Unified Robotic Task Specifications (`URTS`)**, verifying continuous 200 Hz 6-link swept-capsule obstacle clearance and Datum-A fiducial calibration in a physics sandbox.
3. **`03 / A Verified Migration & Sustainment Decision`:** *Separate repair from translation.* Explicitly log multi-format exceptions (`EXC-01`..`EXC-06`) and 3D NDI point-cloud inspection deltas inside a hardware-signed, post-quantum (`ML-KEM-768` + `AES-256-GCM`) SHA-256 Merkle-DAG commit.

---

## Empirical Verification Summary (TRL 4 Baseline)

| Benchmark Suite | Dataset / Scope | Measured Forge Evolve Performance |
| :--- | :--- | :--- |
| **NIST MBE PMI Validation** | 11 Official NIST Test Cases (`CTC-01..05`, `FTC-06..11`) | **99.1%** mean 2D/3D GD&T-to-BRep binding precision; **2.7 μm** projection residual; **<1.5 s** parse time |
| **50-Assembly Aerospace TDP Corpus** | 50 Synthetic TDPs (250 to 28,000 B-Rep faces; 15 to 460 GD&T callouts) | **285.5 ms** mean encrypted WebGPU load; **0.43 hr (25.8 min)** mean total QC programming (**97.0x speedup** over 39.83 hr manual OLP); **2.11 hr** line reconfiguration setup |
| **Zero-Trust ABAC & Merkle Gate** | 1,000 Cross-Enclave Transactions (850 Authorized, 150 Adversarial) | **100.0%** policy accuracy (all 150 foreign-national, non-CMMC, tampered-mesh, and bad-mTLS attacks blocked); **1.24 ms** mean latency |
| **Multi-Vendor Kinematic Adaptation** | 4 Robot + Mobile Base Cells (`FANUC M-20iA`, `KUKA KR 16`, `ABB IRB 4600`, `UR10e/SROS2`) | **0.18–0.24 hr** programming time; **≥55.04 mm** 6-link swept-capsule clearance; **0.0145 mm** p99 TCP residual after 3.8 s Datum-A fiducial calibration |
| **Adversarial TDP Exception Engine** | 225 Fault-Injected Packages across 6 Industrial Exception Classes | **99.6%** auto-detection; **97.4%** GD&T binding accuracy on degraded 150-DPI blueprints; unattended scaling up to **1,250 MB / 42,000 faces / Level-8 BOM nesting** |

---

## Quickstart & CLI Usage (Offline Reproducible Reference)

```bash
# Install package & CLI entry point
pip install -e .

# Run full pytest equivalence suite (14 tests across CTDP-G, 6-Link CCD, Exceptions & URTS)
pytest -v

# Execute CLI subcommands
forge-evolve ingest --step benchmarks/AF_ACP_7740_Bulkhead.stp
forge-evolve verify-ia --policy schemas/ia_compliance.rego
forge-evolve plan-path --dialect FANUC
forge-evolve plan-path --dialect KUKA
forge-evolve plan-path --dialect ROS2
forge-evolve benchmark --suite nist-mbe
forge-evolve benchmark --suite d2p2-50
forge-evolve benchmark --suite redteam-ccd

# Or run standalone benchmark & figure generation scripts directly
python3 forge_evolve_engine.py
python3 run_adversarial_benchmarks.py
```

## Repository Structure

* `forge_evolve/` — Installable Python package & `forge-evolve` CLI (`cli.py`, `models.py`).
* `forge_evolve_engine.py` — End-to-end reference engine (STEP AP242 generator/parser, MIL-STD-31000B OPA validator, SHA-256 Merkle-DAG + CRDT ledger, surface-normal viewpoint solver, 2-station mobile base clustering, 200 Hz 6-link swept-capsule CCD, Datum-A 3-fiducial calibration, FANUC/KUKA/ABB/SROS2 post-processors, 6-class TDP exception recovery engine, 3D NDI anomaly detector, and 50-part benchmark harness).
* `run_adversarial_benchmarks.py` — Extended red-team verification suite generating architecture schematics, 6-link swept-capsule collision profiles, degraded 150–600 DPI blueprint OCR curves, and multi-vendor kinematic benchmarks.
* `tests/` — Automated `pytest` verification suite (`test_ctdpg_merkle.py`, `test_6link_swept_ccd.py`, `test_exception_recovery.py`, `test_urts_postprocessors.py`).
* `schemas/` — Full Neo4j Cypher & PostgreSQL/PostGIS DDL, JSON Schema (Draft 2020-12), gRPC/Protobuf v3 (`ctdp_urts.proto`), and Open Policy Agent (`ia_compliance.rego`) specifications.
* `benchmarks/` — Generated `D2P2_Empirical_Benchmark_50_Aerospace_TDPs.csv`, synthetic unclassified `AF_ACP_7740_Bulkhead.stp`, and `acp_7740_canonical_output.json`.
* `figures/` — High-resolution diagnostic charts and system architecture schematics.

---

## Export-Control & Public Release Hygiene Statement

All CAD geometries (`AF_ACP_7740_Bulkhead.stp`), GD&T callouts, and benchmark datasets included in this public repository are **100% synthetic, unclassified mathematical test artifacts** combined with public **NIST Model-Based Enterprise (MBE) PMI validation test cases (`CTC-01..05`, `FTC-06..11`)**. This repository contains zero classified, Controlled Unclassified Information (CUI), or ITAR defense article technical data.
