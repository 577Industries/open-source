<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/577Industries/.github/main/brand/out/wordmark-dark.svg">
  <img alt="577 Industries" height="44" src="https://raw.githubusercontent.com/577Industries/.github/main/brand/out/wordmark-light.svg">
</picture>

# forge-evolve-tdp

`EVOLVE EXTENSION` · [Parent Platform: `577Industries/forge-evolve`](https://github.com/577Industries/forge-evolve) · [Product Page](https://www.577industries.com/evolve) · [Interactive 3D MBD Studio](https://www.577industries.com/evolve/studio)

**Zero-Trust Model-Based Definition (MBD) and Technical Data Package (TDP) modernization extension of the `forge-evolve` engine for Department of the Air Force Direct-to-Phase-II Topic `DAF27BZ01-DV008`.**

[![ci](https://img.shields.io/github/actions/workflow/status/577Industries/forge-evolve-tdp/ci_equivalence_verification.yml?style=flat-square&label=ci)](https://github.com/577Industries/forge-evolve-tdp/actions/workflows/ci_equivalence_verification.yml)
[![license](https://img.shields.io/badge/license-Apache_2.0-blue?style=flat-square)](LICENSE)

## Relationship to Core Platform (`forge-evolve`)

This repository extends [`577Industries/forge-evolve`](https://github.com/577Industries/forge-evolve) (just as [`forge-evolve-tmpc`](https://github.com/577Industries/forge-evolve-tmpc) extends `forge-evolve` for Navy C#/.NET mission planning):

- **Core `forge-evolve` Foundation Used:** 4-layer Cross-Language Abstract Representation (`CLAR`), differential equivalence verification oracle, and `SHA-256` hashchain provenance.
- **Domain Capabilities Added in `forge-evolve-tdp` (`DAF27BZ01-DV008`):**
  1. **Multimodal 2D/3D MBD Ingestion:** Unifies legacy 2D `MIL-DTL-31000` engineering drawings (PDF/raster) and 3D `STEP AP242` / `IGES` CAD models into a Canonical TDP Graph (`cTDPg`).
  2. **Post-Quantum Merkle-DAG Configuration Lineage:** Integrates **QBit** (`ML-KEM-768` + `AES-256-GCM`) envelope encryption and CRDT multi-depot reconciliation across `AS_DESIGNED` -> `AS_BUILT` -> `AS_SUSTAINED`.
  3. **Zero-Trust OPA ABAC View-Filter (`schemas/ia_compliance.rego`):** Enforces `MIL-STD-31000B`, ITAR, and CMMC Level 2 field-level redaction prior to `<300 ms` WebGPU streaming.
  4. **3D PointNet++ Sustainment Deviation Routing:** Detects and routes out-of-tolerance depot laser scans (`EXC-01..06` recovery).

## Quickstart (5-Minute Evaluator Onramp)

```bash
pip install -e ".[dev]"
pytest -v
python3 forge_evolve_engine.py
python3 run_adversarial_benchmarks.py
```
