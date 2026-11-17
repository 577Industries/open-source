<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/577Industries/.github/main/brand/out/wordmark-dark.svg">
  <img alt="577 Industries" height="44" src="https://raw.githubusercontent.com/577Industries/.github/main/brand/out/wordmark-light.svg">
</picture>

# helios-program

`HELIOS` · [program overview](https://github.com/577Industries#helios--calibrated-heliophysics-fusion)

**Program folder for HELIOS — 577 Industries' research program on calibrated space-weather decision intelligence: copies of its four public artifacts, per-artifact review packs, and the pre-registration text and constants for its hold-out evaluation.**

[![license](https://img.shields.io/badge/license-Apache_2.0-blue?style=flat-square)](LICENSE)

HELIOS (Heliophysics-Enhanced Location Integrity and Operations System) is a model-agnostic Bayesian-Model-Averaging fusion layer for space-weather model outputs, with two vertical slices (NASA SRAG mission-operations radiation risk and U.S. precision-agriculture GNSS). It does not replace SRAG's Acute Radiation Risk Tool (ARRT): it produces fused inputs designed to be compatible with that tool's dose-rate computation. This folder gathers the public artifacts that back its technical claims.

## For technical reviewers (5-minute onramp)

To check the program's technical claims, go to the artifact that carries each one:

1. **Empirical evidence**: see [`gannon-storm-rtk-analysis`](../gannon-storm-rtk-analysis/) for the 25-station NGS CORS analysis (1,283 station-hours headline; `results/quantitative.md`).
2. **Framework code**: [`helios-fusion-engine`](../helios-fusion-engine/) (BMA + isotonic + Mondrian conformal) and [`helios-spaceweather-connectors`](../helios-spaceweather-connectors/) (6 data adapters).
3. **Provenance schema**: [`helios-provenance-spec`](https://github.com/577Industries/helios-provenance-spec) (feature-level lineage JSON Schema).
4. **Pre-registration**: [`orchestration/osf_preregistration.template.md`](orchestration/osf_preregistration.template.md) is the text to file before any hold-out evaluation, with the hypotheses and the three hold-out events; [`orchestration/kill_gate.py`](orchestration/kill_gate.py) holds the same events and the pass thresholds as constants. The text has not been filed and the evaluation has not been run: `kill_gate.py` is a placeholder that raises when called.

Trained model weights, BMA priors, and equipment transfer functions are held in the private `helios-fusion-internal` repo (commercial-license gated); the framework code is fully open.

## Quick start

```bash
git clone https://github.com/577Industries/open-source.git
cd open-source/programs/helios/helios-program
```

This folder was the umbrella repository of HELIOS, which bundled the 4 public HELIOS artifacts as git submodules pinned at release tags. In this monorepo the four are plain copies under [`submodules/`](./submodules/), not submodules, and each artifact's own folder is a sibling of this one under `programs/helios/`.

Three of the copies were refreshed on 2026-11-16 from those sibling folders: `gannon-storm-rtk-analysis` (its state after `v0.2.0`), `helios-spaceweather-connectors` (its state after `v0.2.1`) and `helios-fusion-engine` (its state after `v0.2.0`). The first two had carried a month of the Dst index of the World Data Center for Geomagnetism, Kyoto, which does not allow commercial applications of its indices; the copies no longer do.

## Contents

- [`submodules/`](./submodules/) — copies of the 4 public HELIOS artifacts, each with changes made in this repository after the version it names:
  - [`helios-provenance-spec`](./submodules/helios-provenance-spec/) @ `v0.1.0` plus the unreleased changes made to this copy on 2026-11-10 (wording, in six files)
  - [`helios-spaceweather-connectors`](./submodules/helios-spaceweather-connectors/) @ `v0.2.1` plus the unreleased changes of [`../helios-spaceweather-connectors`](../helios-spaceweather-connectors/) as of 2026-11-16
  - [`helios-fusion-engine`](./submodules/helios-fusion-engine/) @ `v0.2.0` plus the unreleased changes of [`../helios-fusion-engine`](../helios-fusion-engine/) as of 2026-11-16
  - [`gannon-storm-rtk-analysis`](./submodules/gannon-storm-rtk-analysis/) @ `v0.2.0` plus the unreleased changes of [`../gannon-storm-rtk-analysis`](../gannon-storm-rtk-analysis/) as of 2026-11-16 (`v0.2.0` was cut in this repository; the standalone repository stopped at `v0.1.0`)
- [`specs/`](./specs/) — review packs: one per piece of completed work, written for the operator who reviewed it. They are dated records, left as written apart from the root of the local paths they give (`/path/to/workspace`) and one removed value: some refer to a master plan, a companion document and operator notes that were removed from this repository on 2026-11-16.
- [`orchestration/`](./orchestration/) — scaffolding for the hold-out evaluation: `osf_preregistration.template.md` is the text to file on the Open Science Framework before any hold-out evaluation runs (not filed); `kill_gate.py` holds the hold-out events and the HSS and reliability-slope thresholds, and is a placeholder that raises when called; `schema_diff.py` is a placeholder as well.
- [`results/`](./results/) — one record, the coverage matrix of the SEP Scoreboard archive probed on 2026-05-17. It holds no evaluation result.
- [`.github/workflows/`](./.github/workflows/) — the documentation build of the standalone repository. GitHub runs no workflow from this folder.

## Artifact repositories

| Artifact | Repo | Status |
|---|---|---|
| Provenance schema (JSON Schema 2020-12 + pydantic ref impl + RFC) | [`helios-provenance-spec`](https://github.com/577Industries/helios-provenance-spec) | public |
| Space-weather data adapters (DONKI, SEP Scoreboards, NOAA SWPC, CDDIS GIMs, GOES, DSCOVR) | [`helios-spaceweather-connectors`](../helios-spaceweather-connectors/) | public |
| Fusion engine (BMA + isotonic + conformal + severity-stratified validation) | [`helios-fusion-engine`](../helios-fusion-engine/) | public |
| Trained weights, BMA priors, equipment transfer functions | `helios-fusion-internal` | private (IP) |
| May 2024 Gannon storm retrospective on NGS CORS data | [`gannon-storm-rtk-analysis`](../gannon-storm-rtk-analysis/) | public |

## Status

As of 2026-05-18, all 4 public HELIOS artifacts have shipped initial releases and were bundled here as submodules (plain copies in this repository).

## License

Apache 2.0 — see [LICENSE](./LICENSE). Document content (review packs) is provided for reference and citation; please attribute 577 Industries Inc. when quoting.

## Contact

Engineering: <engineering@577industries.com>
Principal Investigator: Thomas Waweru, 577 Industries Inc., Columbus OH
