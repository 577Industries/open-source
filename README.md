# 577 Industries — Open Source

Canonical public monorepo for **577 Industries Inc.** open-source packages, reference implementations, standards specifications, and reproducible research artifacts.

---

## Repository Structure

### `packages/` — Core Open-Source Libraries

| Path | Description |
|---|---|
| [`packages/forge-os-libs/`](packages/forge-os-libs/) | Consolidated FORGE OS open-source Python packages: `forge-workflow-dag`, `forge-tool-guardrails`, `forge-model-router`, `forge-hashchain-audit`, and `forge-agent-memory`. |

### `programs/` — Research Programs & Reference Implementations

| Program | Path | Contents |
|---|---|---|
| **Evolve** | [`programs/evolve/`](programs/evolve/) | `forge-evolve` (modernization engine core; the public code is a Python surrogate), `forge-evolve-tmpc` (the Evolve reference for a Theater Mission Planning Center (TMPC) modernization on a synthetic C#/.NET surrogate; see its `ERRATUM.md`), `forge-evolve-tdp` (technical data package modernization design study), and `forge-evolve-reference` (combined Evolve and Kinetic TDP and robotic-path design study, superseded). |
| **Kinetic** | [`programs/kinetic/`](programs/kinetic/) | `forge-kinetic` (physical autonomy and robotic task execution core; the public code is a placeholder) and `forge-kinetic-mbd` (model-based definition to robot trajectory design study). |
| **HELIOS** | [`programs/helios/`](programs/helios/) | `helios-program` (overview & architecture), `helios-fusion-engine` (probabilistic multi-sensor space-weather fusion), `helios-provenance-spec` (cryptographic telemetry provenance specification), `helios-spaceweather-connectors` (NOAA/SWPC & GNSS data ingestion), and `gannon-storm-rtk-analysis` (May 2024 Gannon geomagnetic superstorm RTK positioning analysis). |
| **FORGE QBit** | [`programs/qbit/`](programs/qbit/) | `forge-qbit-qsparx` (quantum state preparation and circuit synthesis algorithms). |
| **AEGIS** | [`programs/aegis/`](programs/aegis/) | `aegisgraph` (binary vulnerability analysis & exploitability graph engine) and `asema-feasibility-artifacts` (formal verification & program analysis feasibility benchmarks). |
| **FORGE Intelligence** | [`programs/intelligence/`](programs/intelligence/) | `forge-intelligence` (multi-source analytical reasoning and structured evidence evaluation). |
| **Counter-Swarm** | [`programs/counter-swarm/`](programs/counter-swarm/) | `sbir-arm26bx04-nv008-public-evidence` (unclassified synthetic surrogate benchmark data for decentralized counter-swarm target deduplication). |

Status of the Evolve and Kinetic entries: forge-evolve, forge-evolve-reference, forge-evolve-tdp, forge-kinetic and forge-kinetic-mbd are generated design studies (2026-10-13), relabeled 2026-10-15; their numbers are not measurements. Measured implementations replace them in place.

### `.github-org/` — Organization Profile & Brand Assets

Organization-level profile metadata and public brand assets for [`github.com/577Industries`](https://github.com/577Industries).

---

## License

Unless otherwise noted in a subdirectory's `LICENSE` file (such as specific research data releases), code in this repository is licensed under the Apache License, Version 2.0 or MIT License as specified per package. See [`LICENSE`](LICENSE) for details.
