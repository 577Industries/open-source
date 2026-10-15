# Evolve and Kinetic design study: TDP and robotic task reference (synthetic, superseded)

> **Status (2026-10-15): generated design study, not evidence.** This directory was produced as a design study by a code-generation agent on 2026-10-13. Its benchmark tables, figures and numeric claims (precision, latency, clearance, timing, exception counts) are synthetic design targets emitted by the code itself, not measurements, and must not be cited as results. The maintained, measured implementation replaces this directory in place as it lands; measured results will be published under `programs/evolve/bench-results/` with run receipts. Until then this directory is retained for provenance only.

[![Design-study self-check (not evidence)](https://github.com/577Industries/forge-evolve-reference/actions/workflows/ci_equivalence_verification.yml/badge.svg)](https://github.com/577Industries/forge-evolve-reference/actions/workflows/ci_equivalence_verification.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-0D9488.svg)](https://www.python.org/)

**Move the baseline forward. Preserve what matters.**  
*Public design-study reference by [577 Industries Inc.](https://www.577industries.com) (Columbus, Ohio | PI: Dr. Thomas G. Waweru)*  
*Product pages: [Evolve (`/evolve`)](https://www.577industries.com/evolve) · [Kinetic (`/kinetic`)](https://www.577industries.com/kinetic)*

---

## Modular Product & Domain Extension Repositories

In addition to this combined design-study bundle (`forge-evolve-reference`), the architecture is decomposed into two core product engines and their domain-specific extensions. `forge-evolve`, `forge-evolve-tdp`, `forge-kinetic` and `forge-kinetic-mbd` are generated design studies (2026-10-13) relabeled on 2026-10-15; `forge-evolve-tmpc` is a hand-built harness with its own `ERRATUM.md`.

| Repository | Layer | Scope & Primary Surface |
| :--- | :--- | :--- |
| [**`577Industries/forge-evolve`**](https://github.com/577Industries/forge-evolve) | **Core Product (`Evolve`)** | Deterministic Code & Artifact Modernization Engine (`Discovery -> CLAR IR -> Planner -> Differential Equivalence Oracle -> Hashchain Provenance`). The current public code is a Python surrogate that returns fixed values. [`/evolve`](https://www.577industries.com/evolve) |
| [**`577Industries/forge-evolve-tdp`**](https://github.com/577Industries/forge-evolve-tdp) | **Evolve Extension (`DAF27BZ01-DV008`)** | **Evolve TDP** design: STEP AP242 / 2D PDF MBD modernization, hash-linked configuration lineage, FIPS 203 ML-KEM-768 + AES-256-GCM envelope encryption (design, not implemented), streamed viewing with a sub-second first-frame target, and planned NDI deviation routing. [`/work/forge-evolve-tdp`](https://www.577industries.com/work/forge-evolve-tdp) |
| [**`577Industries/forge-evolve-tmpc`**](https://github.com/577Industries/forge-evolve-tmpc) | **Evolve Extension (`DON26BZ01-NV013`)** | C#/.NET Mission-Planning Code Modernization & Split-Disposition Verification Harness on a synthetic surrogate (see its `ERRATUM.md`). [`/work/forge-evolve-tmpc`](https://www.577industries.com/work/forge-evolve-tmpc) |
| [**`577Industries/forge-kinetic`**](https://github.com/577Industries/forge-kinetic) | **Core Product (`Kinetic`)** | Physical AI design: multi-sensor operating envelopes, 6-DOF + AGV whole-body IK, swept-capsule collision checking, and multi-vendor URTS post-processors (`FANUC`, `KUKA`, `ABB`, `SROS2`). The current public code is a placeholder that returns fixed values. [`/kinetic`](https://www.577industries.com/kinetic) |
| [**`577Industries/forge-kinetic-mbd`**](https://github.com/577Industries/forge-kinetic-mbd) | **Kinetic Extension (`DAF27BZ01-DV012`)** | **Kinetic** TDP-to-robot workcell compiler design: GD&T-to-B-Rep binding, mobile base station clustering, Datum-A 3-fiducial docking calibration, and an operator interface. No binding precision or docking residual has been measured. [`/work/forge-kinetic-mbd`](https://www.577industries.com/work/forge-kinetic-mbd) |

---

## Overview

**Evolve** (code and technical data modernization) and **Kinetic** (physical AI and autonomous robotic execution) are designed to enforce a deterministic equivalence contract across software codebases, Model-Based Definition (MBD) Technical Data Packages (TDPs), and multi-axis robotic workcells.

Whether migrating legacy flight/scientific code (`Fortran`, `Ada`, `C++`, `COBOL`, `.NET`), modernizing heterogeneous 3D/2D TDPs into a zero-trust configuration ledger (**Evolve TDP**), or compiling GD&T tolerances into collision-checked multi-vendor robotic inspection trajectories (**Kinetic**), **small differences can change the contract**. A signed angle, surface normal vector, or bilateral tolerance zone can describe the same nominal geometry and still break a downstream rule or cause a physical link collision.

The intended three-stage verification contract. Each stage is a design goal; the parenthetical states what this directory's code does today.
1. **`01 / A Behavioral & Geometric Baseline`:** Parse 3D B-Rep topology (`STEP AP242`, `IGES`), 2D engineering blueprints (`PDF`), and source specifications into the **Canonical TDP Property Graph (`CTDP-G v2.4`)**, locking datum reference frames `[A|B|C]`, tolerances, and Attribute-Based Access Control (ABAC) security scopes. (The code generates an 18-face synthetic part from fixed tuples; it does not parse STEP, PDF or IGES content.)
2. **`02 / A Reviewed Working Slice`:** Transform bounded modules into progressive mesh streams (sub-second first-frame target) and **Unified Robotic Task Specifications (`URTS`)**, verifying swept-capsule obstacle clearance and Datum-A fiducial calibration in a physics sandbox. (The "clearance" series is a closed-form sinusoid clamped at 55.04 mm; there is no geometry, SDF or simulator. The calibration is a Kabsch Monte Carlo on assumed fiducial noise.)
3. **`03 / A Verified Migration & Sustainment Decision`:** *Separate repair from translation.* Log multi-format exceptions (`EXC-01`..`EXC-06`) and 3D NDI inspection deltas inside a hash-linked commit, with post-quantum envelope encryption (`ML-KEM-768` + `AES-256-GCM`) and hardware signing as design goals. (A SHA-256 hash chain with a Merkle root is implemented. No cryptographic library is used; nothing is encrypted or signed, and the "HSM signature" field is an unkeyed hash.)

---

## Design targets (not measured)

The table that previously stood here reported "measured" results under a "TRL 4" heading. Those values were emitted by this directory's own code from seeded random draws and constants, and they are withdrawn. Only thresholds survive, as targets.

| Design target | Source of threshold | Status |
| :--- | :--- | :--- |
| Encrypted viewer first frame under 1 s | DAF27BZ01-DV008 solicitation ("sub-second") | Not yet measured; no streaming code exists |
| Numerical QC programming under 1.5 hr per part | DAF27BZ01-DV012 solicitation | Not yet measured; the CSV column is a seeded formula |
| Line reconfiguration under 8 hr | DAF27BZ01-DV012 solicitation | Not yet measured; the CSV column is a seeded formula |
| GD&T-to-B-Rep binding precision and recall on the public NIST MBE PMI test cases (`CTC-01..05`, `FTC-06..11`) | Self-imposed gate of 95% | Not yet run; no NIST file is included and the per-case table in the code is hardcoded |
| Swept-capsule clearance above a cell-specific safety floor (45 mm in the design) | Self-imposed | Not yet measured; the code clamps a sinusoid at 55.04 mm |
| Datum-A 3-fiducial registration error under 25 um | Self-imposed | Simulation only (Kabsch Monte Carlo with an assumed 6.5 um fiducial noise); not an end-to-end TCP accuracy |
| Rules-based IA gate with audit trail | DAF27BZ01-DV008 solicitation | Six boolean checks re-implemented in Python; the Rego policy is never evaluated and the 99.4 "score" is a constant |
| Unattended parse envelope (file size, face count, BOM nesting depth) | DAF27BZ01-DV012 solicitation | Not yet measured |

Measured results, when they exist, will be published under `programs/evolve/bench-results/` with run receipts and will replace this directory in place.

---

## Quickstart & CLI Usage (Offline, Deterministic)

```bash
# Install package & CLI entry point
pip install -e .

# Run the pytest self-check (15 tests; the clearance, score and exception-count tests assert constants)
pytest -v

# Execute CLI subcommands
forge-evolve ingest --step benchmarks/AF_ACP_7740_Bulkhead.stp   # returns the built-in 18-face part regardless of file content
forge-evolve verify-ia --policy schemas/ia_compliance.rego        # Python booleans; the Rego file is not evaluated
forge-evolve plan-path --dialect FANUC
forge-evolve plan-path --dialect KUKA
forge-evolve plan-path --dialect ROS2
forge-evolve benchmark --suite nist-mbe                           # hardcoded per-case table
forge-evolve benchmark --suite d2p2-50                            # 50 rows from np.random.default_rng(2026)
forge-evolve benchmark --suite redteam-ccd                        # clamped analytic curve and Monte Carlo

# Or run the standalone scripts directly (they rewrite benchmarks/ and figures/ with synthetic targets)
python3 forge_evolve_engine.py
python3 run_adversarial_benchmarks.py
```

## Repository Structure

* `forge_evolve/`: installable Python package and `forge-evolve` CLI (`cli.py`, `models.py`).
* `forge_evolve_engine.py`: design-study engine. Synthetic STEP AP242 text generator (content is not parsed on ingest), Python re-implementation of six IA gate booleans (the Rego file is never evaluated), SHA-256 hash chain with a Merkle root and an LWW-map CRDT join, surface-normal viewpoint solver, two fixed mobile base stations, a clamped analytic "clearance" curve, Kabsch 3-fiducial registration Monte Carlo, FANUC/KUKA/ABB/ROS 2 text templates, six trivial EXC-01..06 handlers, hardcoded anomaly records, and a seeded generator for the 50-row design-target table.
* `run_adversarial_benchmarks.py`: chart and schematic generator; every plotted series is a hardcoded array or a closed-form curve.
* `tests/`: `pytest` self-check (`test_ctdpg_merkle.py`, `test_6link_swept_ccd.py`, `test_exception_recovery.py`, `test_urts_postprocessors.py`). The hash-chain determinism, CRDT and string-template tests exercise real code; the clearance, score and exception-count tests assert constants.
* `schemas/`: unimplemented design draft. Neo4j Cypher and PostgreSQL/PostGIS DDL, JSON Schema (Draft 2020-12), gRPC/Protobuf v3 (`ctdp_urts.proto`), and an Open Policy Agent policy (`ia_compliance.rego`) that nothing evaluates.
* `benchmarks/`: `synthetic_design_targets_generated.csv` and `synthetic_design_targets_generated.json`, written by the engine from a seeded RNG and constants (not measurements), plus the synthetic `AF_ACP_7740_Bulkhead.stp` text.
* `figures/`: empty in git. The scripts write charts of synthetic targets here; see `figures/README.md`.

---

## Export-Control & Public Release Hygiene Statement

All CAD geometry (`AF_ACP_7740_Bulkhead.stp`), GD&T callouts and tables in this public directory are **100% synthetic, unclassified mathematical test artifacts**. No NIST MBE PMI test-case file is included and none has been run. This directory contains zero classified, Controlled Unclassified Information (CUI), or ITAR defense article technical data; example identifiers, markings and key URIs in `schemas/` are placeholders.
