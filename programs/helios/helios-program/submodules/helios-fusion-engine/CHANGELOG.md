# Changelog

All notable changes to this project are documented here, following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Releases `v0.1.1` and `v0.1.2` (2026-05-17) and `v0.2.0` (2026-05-18) were tagged in the project's standalone repository, which is archived. They have no section here, and the notes published with those tags are not reproduced. `docs/training.md` describes the training work of 0.1.1. The work of 0.1.2 (ground-truth labels from NOAA's archive of solar proton events, and a fallback per component) is described in the module notes of `src/helios_fusion/training/swpc_sep_archive.py` and `load_table_3_1.py`. `paper/` holds the manuscript draft that 0.2.0 added.

## [Unreleased]

### Changed
- `paper/main.pdf` is rebuilt from the current `paper/main.tex` (2026-11-16). The PDF in the repository had been built on 2026-05-18 and no longer matched its source.
- The manuscript no longer quotes a Dst value for the May 2024 storm. The index's source, the World Data Center for Geomagnetism in Kyoto, does not allow commercial applications of its indices.
- The manuscript, its reference and figure 1 name the storm analysis at `v0.2.0`, in this repository. The text had named 0.2.0 as a planned release with a full positioning solution; 0.2.0 is the climatological model without the Dst index, and the positioning solution is a later release.
- `docs/training.md` named Kyoto as the archive behind the Kp index. The connectors take Kp from GFZ.
- Three module notes no longer name a funding program.
- The `dev` extra takes `helios-spaceweather-connectors` from the sibling folder of the same checkout (`{root:parent:uri}`, which hatchling expands). Installing the extra builds that folder as it then is and copies it into the environment, so the suite runs against the checkout's connectors as of that install; uv does not rebuild them later unless told to (`--reinstall-package helios-spaceweather-connectors`). It took the standalone repository's `v0.2.1` tag. The connectors' source here differs from that tag in ten files, and this suite passes against it (176 tests). `docs/training.md` no longer has an install step for the connectors.
- `README.md` and `docs/index.md` gave `pip install helios-fusion-engine`, and no package of that name is on PyPI. They install this repository's `main` branch; nothing in this repository is tagged.
- The manuscript's references to the connectors, to this framework, to the program and to the storm analysis give their folders in this repository at the commit they describe (the address names it). The reference to the program and figure 1 name `v0.3.0`, its last release; they said `v0.2.0`. It no longer names a `feat/v0.2-paper` branch for the figure scripts, which are in `paper/figures/`. `paper/main.bbl` and `paper/main.pdf` are rebuilt.
- The manuscript describes the program's master plan and companion document, which were removed from this repository on 2026-11-16. Where it does, it now cites a revision: figure 1's caption and the decision-tree paragraph gain the citation, and its data-availability list points to the cited revision where it gave a link to the folder. Its four references to folders of this repository name one commit, and the storm analysis is cited as `v0.2.0` with later changes. Two comments in `paper/refs.bib` gave the companion's reference section as §8; it is §7.
- The README said that the kill-gate runner refuses to run without a recorded pre-registration address. The runner, `orchestration/kill_gate.py` in the program's folder, is a placeholder that raises when called, and nothing checks for the address. The README says so, and that the text has not been filed. The README, the documentation's first page and the baselines guide also said that the runner consumes or references this framework's functions; they say what it is meant to do.
- `.github/workflows/paper.yml` no longer lists the cover letter or the submission checklist among the files it uploads, and a comment in `pyproject.toml` no longer names a removed operator note. `docs/training.md` told the reader to enter a worktree on the author's machine; it names the folder in a clone of this repository. The destination it and the training notebook give for the weights, a folder under the home directory, is left as written. The training package's note points to `docs/training.md` and the pre-registration template where it named a spec of the program's folder, removed as well. Two lines of `docs/training.md` no longer cite that spec; comments in the training code and its tests that say "the spec" are left as written.
- The project's own addresses give this repository: `CITATION.cff`, the package metadata (`[project.urls]`), `mkdocs.yml` (no `site_url`; `repo_url` and `edit_uri`), `CONTRIBUTING.md` (the clone command), `SECURITY.md` (its scope sentence) and the README, which loses the badges that queried the standalone repository's CI and releases. The README says that no workflow runs here, that the 85% coverage it named was a target no workflow enforced, and what the suite measures, 89% (it said 92%). Links to the program and the connectors lead to their folders under `programs/helios/`; links to `helios-provenance-spec` are unchanged. Outside the manuscript, nothing here names the program's master plan as a document to read any more.

### Removed
- `paper/COVER_LETTER.md` and `paper/SUBMISSION_CHECKLIST.md` (2026-11-16): a draft cover letter with unfilled fields, and the operator's checklist for a submission that has not been made. The letter held one statement that the manuscript does not: that the authors have no other financial interests to disclose. The manuscript's acknowledgments state the funding only.

## [0.1.0] — 2026-05-17

### Added
- `BMAOrchestrator` with skill-weighted updates and missing-model renormalization.
- Calibrators: `IsotonicCalibrator`, `PlattCalibrator` (shipped for reproducible rejection rationale; tests assert isotonic beats Platt on tail-miscalibrated synthetic data), `SeverityStratifiedCalibrator`.
- Conformal regressors: `SplitConformalRegressor`, `MondrianConformalRegressor` with per-stratum coverage validation.
- CCMC-compatible metrics suite (HSS Donaldson 1975, TSS, POD, FAR, Brier, CRPS) with bootstrapped 95% CIs.
- `EvalReport` shape pinned to the OSF pre-registration template — quiet/moderate/extreme strata always present, NaN-stub records for empty strata.
- Best-component baseline (the kill-gate comparator).
- Explicit `to_state_dict` / `from_state_dict` on calibrators and conformal regressors (no pickle; JSON-friendly state for safe transport via helios-fusion-internal).
- 105 tests at 92% line+branch coverage. Hypothesis property tests for invariants (BMA weights sum to 1; isotonic monotone; HSS bounded in [-1, 1]).
- Synthetic-data demo notebook: isotonic brings reliability slope 1.0071 → 1.0772 (within ±0.15 target); Mondrian conformal achieves 91% aggregate coverage @ α=0.1.

**Public framework only.** Trained weights, BMA priors fitted on Table 3-1 events, and equipment transfer functions live in the private companion `helios-fusion-internal`.
