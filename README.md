# 577 Industries — Open Source

Canonical public monorepo for **577 Industries Inc.** open-source packages, reference implementations, standards specifications, and reproducible research artifacts.

---

## Repository Structure

### `packages/` — Core Open-Source Libraries

| Path | Description |
|---|---|
| [`packages/forge-os-libs/`](packages/forge-os-libs/) | The five FORGE OS open-source TypeScript libraries, published independently to npm: `@577-industries/agent-memory`, `@577-industries/model-router`, `@577-industries/tool-guardrails`, `@577-industries/workflow-dag` and `@577-industries/hashchain-audit`. |

### `programs/` — Research Programs & Reference Implementations

| Program | Path | Contents |
|---|---|---|
| **Evolve** | [`programs/evolve/`](programs/evolve/) | `forge-evolve` (modernization engine core; the public code is a Python surrogate), `forge-evolve-tmpc` (the Evolve reference for a Theater Mission Planning Center (TMPC) modernization on a synthetic C#/.NET surrogate; see its `ERRATUM.md`), `forge-evolve-tdp` (technical data package modernization design study), and `forge-evolve-reference` (combined Evolve and Kinetic TDP and robotic-path design study, superseded). |
| **Kinetic** | [`programs/kinetic/`](programs/kinetic/) | `forge-kinetic` (physical autonomy and robotic task execution core; the public code is a placeholder) and `forge-kinetic-mbd` (model-based definition to robot trajectory design study). |
| **HELIOS** | [`programs/helios/`](programs/helios/) | `helios-program` (program meta-repo: master plan, orchestration scripts and design specs), `helios-fusion-engine` (model-agnostic probabilistic fusion of space-weather model outputs), `helios-provenance-spec` (JSON Schema for feature-level provenance in heliophysics fusion systems), `helios-spaceweather-connectors` (Python adapters for NASA DONKI, CCMC SEP Scoreboards, NOAA SWPC, CDDIS GIMs, GOES and DSCOVR), and `gannon-storm-rtk-analysis` (retrospective RTK-GNSS positioning error analysis of the May 2024 Gannon G5 superstorm). |
| **FORGE QBit** | [`programs/qbit/`](programs/qbit/) | `forge-qbit-qsparx` (a synthetic cryptographic mission twin for planning post-quantum migration: cryptographic inventory, prioritization and effect-free simulation on fictional data). |
| **AEGIS** | [`programs/aegis/`](programs/aegis/) | `aegisgraph`, one project: graph-driven vulnerability discovery for secure messaging applications (engine, validator and schemas), with its sanitized review collection in [`aegisgraph/review-collection/`](programs/aegis/aegisgraph/review-collection/). |
| **FORGE Intelligence** | [`programs/intelligence/`](programs/intelligence/) | `forge-intelligence` (an OSINT fusion console: a WebGL globe over public-domain intelligence feeds with a passive-first reconnaissance toolkit). |
| **Counter-Swarm** | [`programs/counter-swarm/`](programs/counter-swarm/) | Unclassified synthetic surrogate benchmark data for decentralized counter-swarm target deduplication. |

Status of the Evolve and Kinetic entries: forge-evolve, forge-evolve-reference, forge-evolve-tdp, forge-kinetic and forge-kinetic-mbd are generated design studies (2026-10-13), relabeled 2026-10-15; their numbers are not measurements. Measured implementations replace them in place.

### `.github-org/` — Organization Profile & Brand Assets

Organization-level profile metadata and public brand assets for [`github.com/577Industries`](https://github.com/577Industries).

---

## License

Unless otherwise noted in a subdirectory's `LICENSE` file (such as specific research data releases), code in this repository is licensed under the Apache License, Version 2.0 or MIT License as specified per package. See [`LICENSE`](LICENSE) for details.
