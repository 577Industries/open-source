<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/577Industries/.github/main/brand/out/wordmark-dark.svg">
  <img alt="577 Industries" height="44" src="https://raw.githubusercontent.com/577Industries/.github/main/brand/out/wordmark-light.svg">
</picture>

# forge-evolve-tdp

> **Status (2026-10-15): generated design study, not evidence.** This directory was produced as a design study by a code-generation agent on 2026-10-13. Its benchmark tables, figures and numeric claims (precision, latency, clearance, timing, exception counts) are synthetic design targets emitted by the code itself, not measurements, and must not be cited as results. The maintained, measured implementation replaces this directory in place as it lands; measured results will be published under `programs/evolve/bench-results/` with run receipts. Until then this directory is retained for provenance only.

`EVOLVE EXTENSION` · [Parent Platform: `577Industries/forge-evolve`](https://github.com/577Industries/forge-evolve) · [Product Page](https://www.577industries.com/evolve)

**Design study for a zero-trust Model-Based Definition (MBD) and Technical Data Package (TDP) modernization extension of `forge-evolve`, prepared for Department of the Air Force Direct-to-Phase-II Topic `DAF27BZ01-DV008`.**

[![ci](https://img.shields.io/github/actions/workflow/status/577Industries/forge-evolve-tdp/ci_equivalence_verification.yml?style=flat-square&label=ci)](https://github.com/577Industries/forge-evolve-tdp/actions/workflows/ci_equivalence_verification.yml)
[![license](https://img.shields.io/badge/license-Apache_2.0-blue?style=flat-square)](LICENSE)

## Relationship to Core Platform (`forge-evolve`)

This directory is positioned as an extension of [`577Industries/forge-evolve`](https://github.com/577Industries/forge-evolve), as [`forge-evolve-tmpc`](https://github.com/577Industries/forge-evolve-tmpc) is for Navy C#/.NET mission planning. In its current state it imports nothing from the core: `forge_evolve_engine.py` is a standalone design study, shared byte-for-byte with `forge-evolve-reference` and `forge-kinetic-mbd`.

- **Core `forge-evolve` foundation intended for reuse:** 4-layer Cross-Language Abstract Representation (`CLAR`), differential equivalence verification oracle, and `SHA-256` hashchain provenance. Not yet wired in.
- **Domain capabilities designed for `forge-evolve-tdp` (`DAF27BZ01-DV008`), with the current code state in parentheses:**
  1. **Multimodal 2D/3D MBD ingestion:** unify legacy 2D `MIL-STD-31000B` engineering drawings (PDF/raster) and 3D `STEP AP242` / `IGES` CAD models into a Canonical TDP Graph (`CTDP-G`). (Design. The code generates an 18-face synthetic part from fixed tuples and does not parse STEP, PDF or IGES content.)
  2. **Merkle-DAG configuration lineage:** hash-linked `AS_DESIGNED` -> `AS_BUILT` -> `AS_SUSTAINED` commits with CRDT multi-depot reconciliation, wrapped in FIPS 203 ML-KEM-768 (design, not implemented) + `AES-256-GCM` envelope encryption. (The hash chain and the CRDT join are implemented. No cryptographic library is used; nothing is encrypted or signed.)
  3. **Zero-trust OPA ABAC view filter (`schemas/ia_compliance.rego`):** `MIL-STD-31000B`, ITAR and CMMC Level 2 field-level redaction before streamed viewing, with a sub-second first-frame target. (Design. The Rego file is never evaluated; six boolean checks are re-implemented in Python. No streaming code exists and no latency has been measured.)
  4. **Sustainment deviation routing:** detect and route out-of-tolerance depot scans through `EXC-01..06` recovery. (Design. The anomaly records are hardcoded; no point cloud and no model are involved.)

## Quickstart (5-Minute Evaluator Onramp)

```bash
pip install -e .
pytest -v
python3 forge_evolve_engine.py          # rewrites benchmarks/ and figures/ with synthetic design targets
python3 run_adversarial_benchmarks.py
```
