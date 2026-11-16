# Changelog

All notable changes to the HELIOS program meta-repo are documented here, following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This repository is documents-first; the version reflects milestone polish or structural shifts in the program-level orchestration, not code releases of the artifact repos (those have their own CHANGELOGs).

Release `v0.3.0` (2026-05-18, an evidence package under `phase-ii/`, removed since) was tagged in the standalone repository, which is archived. It has no section here, and the notes published with that tag are not reproduced.

## [Unreleased]

### Removed
- **Working files (2026-11-16).** Planning, operator and submission working material that stated plans and stages which no longer hold: the follow-on plan folder `phase-ii/` with its four documentation wrappers, the workflow that rendered it and the spec that assembled it; the companion document `companion/companion.md` with its registry, its renderer, its documentation wrapper, the registry's generator `orchestration/companion_sync.py` and the workflow that checked it, `.github/workflows/companion-check.yml`; `plan/master-plan.md` and its wrapper; `CLAUDE.md`, `OPERATOR_TODO.md`, `docs/operations.md` and two social-post drafts; and four forward-looking specs under `specs/` (the training sprint, the kill-gate sprint, TEC forecasting and the preprint draft), which described work to be dispatched; the training sprint and the preprint draft were carried out afterwards, the kill-gate run and TEC forecasting were not.

### Changed
- **The copies under `submodules/` no longer carry Kyoto's Dst data (2026-11-16).** The copies of `gannon-storm-rtk-analysis`, `helios-spaceweather-connectors` and `helios-fusion-engine` were refreshed from this repository's own copies of those projects, and have followed them since. The first is `v0.2.0`, which no longer downloads, stores, plots or uses the Dst index; the second tests its Dst path against invented values, and its GFZ fixture no longer carries the sunspot numbers, which are CC BY-NC 4.0; the third brings its manuscript, rebuilt from the current source. The World Data Center for Geomagnetism, Kyoto, does not allow commercial applications of its indices. The README's list says of each copy what changed after the version it names, the schema's copy included (wording, on 2026-11-10, in six files).
- The landing page and the README give the regenerated headline (1,283 station-hours; 1,302 in `v0.1.0`), and the blog post copy is updated with a dated note. Both link this repository's copy of the analysis.
- **Links lead to this repository (2026-11-16).** The README, the landing-page template, the pre-registration template, `mkdocs.yml` and the files under `templates/` linked the standalone repositories of the connectors, the fusion engine and this program, and their documentation sites. They link the folders under `programs/helios/`. The README's badges for the standalone repository's CI and releases are gone, and its quick start clones this repository.
- **The README describes what the folder holds now.** Its onramp starts from the four artifacts; it says that the pre-registration text has not been filed, that `orchestration/kill_gate.py` is a placeholder holding the hold-out events and thresholds (it said the script executes the evaluation), and that `results/` holds one coverage record and no evaluation result (it said kill-gate results). It carries one limit that only the companion stated: HELIOS does not replace SRAG's Acute Radiation Risk Tool.
- **`orchestration/kill_gate.py` says what it is.** Its notes named the master plan and a workflow that checks for a registration address; no such workflow exists. They name the pre-registration template, and say that nothing enforces the filing yet; the exception it raises names the template too, and says that the evaluation is not implemented where it named a sprint. The template states its two instructions about the runner as rules; it said the runner enforces them.
- The documentation's landing page and navigation, the landing-page template and the pull-request and issue templates no longer point to the removed files. The landing page loses a status snapshot of May 2026 that deferred to the master plan, and its template loses the status texts of the same month: the connectors' card and the dependency graph said one adapter of six was live (all six are in `v0.2.1`), a paragraph described a second wave as in progress, and two tiles gave a test count and a coverage bound that nothing here keeps current. Each card gives the version the README lists. The pre-registration template loses its sentence about a footnote in the companion. The documentation workflow loses the step that copied the companion's registry.
- Left as written: `.gitmodules`, the dated entries of this file, and the review packs under `specs/`, dated records which still describe `v0.1.0` (one review pack quotes the Dst minimum it reported) and refer to some of the removed files. The blog post copy keeps its sentence about the companion; its dated note says that the document was removed.

### Added
- `CHANGELOG.md` (this file) — back-filled to v0.1.0 from `gh release` history.

## [0.2.0] — 2026-05-17 — Visual polish

### Added
- **Custom MkDocs landing page** with hero (1,302-station-hours headline + climatological-v1 caveat preserved), 4 artifact status cards, 4-up stats strip, Mermaid dependency graph.
- **Custom sun-themed SVG logo + favicon** at `docs/assets/{logo,favicon}.svg` (deployed across all 5 HELIOS Pages sites for portfolio-wide visual consistency).
- **Custom CSS** at `docs/stylesheets/extra.css` covering hero, artifact-card grid, stats strip, dependency-graph section, dark-mode adjustments, print overrides.
- **MkDocs blog plugin** enabled at `docs/blog/` with the first post — the Gannon storm retrospective — and social-post drafts (LinkedIn long-form, 9-tweet thread).
- **New plugins**: `mkdocs-git-revision-date-localized-plugin` (Last-updated stamps), `mkdocs-include-markdown-plugin` (canonical content stays in `companion/`, `plan/`, `specs/` without build-time `cp`), `mkdocs-glightbox` (image lightboxes).
- **CLAUDE.md** at repo root — in-repo working context for future Claude sessions and developer onboarding (the org/user disambiguation, kill-gate discipline, agent dispatch patterns, daily checklist).
- **`.github/workflows/companion-check.yml`** earlier this session — yamllint + footnotes-sync check + lychee link-check.
- Shared meta-file templates at `templates/` (SECURITY.md, CHANGELOG.md.template, .github/PULL_REQUEST_TEMPLATE.md, .github/ISSUE_TEMPLATE/{bug,feature}.md, .github/FUNDING.yml) distributed to all 4 public artifact repos.

### Changed
- **Palette refresh**: `deep_purple/amber` → `blue/teal` (better dark-mode contrast; signals "credible engineering" register for the NASA-center + precision-ag audience).
- **Fonts**: Material defaults → Inter (text) + JetBrains Mono (code).
- **Nav restructure**: Home is now the custom landing; the companion document is a dedicated page; Blog added.
- **Workflow refactored**: `.github/workflows/pages.yml` dropped the 9-line `cp` aggregation step in favor of `mkdocs-include-markdown-plugin` directives in `docs/*.md` files. Only `companion/footnotes.yaml` is still copied (referenced as a relative download link in companion.md).
- **`companion/footnotes.yaml`** PyPI URL corrected: `helios-provenance` → `helios-provenance-spec` (the actual package name).

### Fixed
- Master plan `Decisions Locked` table updated to reflect the post-migration `577Industries` org URL (was the historical `577-Industries` user URL).

## [0.1.0] — 2026-05-17 — Initial pages publication

### Added
- Initial Pages publication at <https://577industries.github.io/helios-program/> via MkDocs Material with `actions/configure-pages` + `actions/deploy-pages` (workflow-source deployment, not branch-source Jekyll).
- Master plan committed to `plan/master-plan.md`.
- Companion document at `companion/companion.md` describing HELIOS with live artifact citations.
- Operations runbook at `docs/operations.md`.
- OSF pre-registration template at `orchestration/osf_preregistration.template.md` (binding text; the kill-gate runner refuses to execute without the OSF URL on file at `orchestration/osf_preregistration.url`).
- Four per-artifact Wave 1 review packs at `specs/2026-05-17-{A,B,C,D}-*-review-pack.md`.
- `orchestration/companion_sync.py` — rebuild the artifact registry from upstream GitHub release state; `--check` mode for CI.
- `orchestration/kill_gate.py` — intentional `NotImplementedError` stub until OSF pre-reg + B v0.2 + Sprint C-Training all complete.

### Context
This session completed Wave 1 of the HELIOS program: four public artifacts (helios-provenance-spec v0.1.0 RFC, helios-fusion-engine v0.1.0 framework, gannon-storm-rtk-analysis v0.1.0 retrospective, helios-spaceweather-connectors foundation+DONKI), plus the private helios-fusion-internal scaffolding and this meta-repo. All repos transferred from the user account `577-Industries` (the bootstrap mistake) to the organization `577Industries` (alongside aegisgraph, model-router, agent-memory, tool-guardrails).
