<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/577Industries/.github/main/brand/out/wordmark-dark.svg">
  <img alt="577 Industries" height="44" src="https://raw.githubusercontent.com/577Industries/.github/main/brand/out/wordmark-light.svg">
</picture>

# forge-evolve

`EVOLVE` · [Product page on 577industries.com](https://www.577industries.com/evolve) · [Work reference](https://www.577industries.com/work/forge-evolve)

**Deterministic legacy software and engineering artifact modernization engine: dependency discovery, Cross-Language Abstract Representation (CLAR), risk-scored decomposition, differential behavioral comparison, and tamper-evident provenance.**

[![ci](https://img.shields.io/github/actions/workflow/status/577Industries/forge-evolve/ci.yml?style=flat-square&label=ci)](https://github.com/577Industries/forge-evolve/actions/workflows/ci.yml)
[![license](https://img.shields.io/badge/license-Apache_2.0-blue?style=flat-square)](LICENSE)

## Architecture & Domain Extensions

`forge-evolve` is the core modernization engine maintained by **577 Industries Inc.** It separates source discovery and intermediate representation from target code/artifact generation and differential verification:

```text
Ingest -> Discovery (AST/SCCs) -> CLAR IR (4-Layer) -> Migration Planner
       -> Transformation -> Differential Equivalence Oracle -> Hashchain Provenance
```

### Official Domain Extensions

| Extension Repository | Domain / Program Scope | Target Artifacts |
|---|---|---|
| [`577Industries/forge-evolve-tmpc`](https://github.com/577Industries/forge-evolve-tmpc) | U.S. Navy `DON26BZ01-NV013` (Theater Mission Planning Center) | Legacy C#/.NET/JS/SQL mission-planning software -> modern .NET 8 microservices + cATO artifacts |
| [`577Industries/forge-evolve-tdp`](https://github.com/577Industries/forge-evolve-tdp) | U.S. Air Force / Space Force `DAF27BZ01-DV008` (Technical Data Packages) | Legacy 2D MIL-DTL-31000 PDF/raster drawings + STEP AP242 CAD -> Zero-Trust Canonical TDP Graph (`cTDPg`) + `ML-KEM-768` Merkle-DAG |

## Quickstart (Offline, Deterministic)

```bash
pip install -e ".[dev]"
pytest -v
forge-evolve discover --source surrogate/legacy_navigation.py
forge-evolve clar-lift --source surrogate/legacy_navigation.py
forge-evolve compare --corpus results/equivalence-report.json
forge-evolve audit --manifest results/provenance-ledger.json
```

## Reading Order

1. [`companion/companion.md`](companion/companion.md) — Maps core engine contracts to files and tests.
2. [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) — Instructions to reproduce every verification output offline.
3. [`EXCLUSIONS.md`](EXCLUSIONS.md) — Publication boundary (100% synthetic, unclassified corpora).
