# Changelog

All notable changes to the HELIOS program meta-repo are documented here, following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This repository is documents-first; the version reflects milestone polish or structural shifts in the program-level orchestration, not code releases of the artifact repos (those have their own CHANGELOGs).

Release `v0.3.0` (2026-05-18, the evidence package under `phase-ii/`) was tagged in the standalone repository, which is archived. It has no section here, and the notes published with that tag are not reproduced.

## [Unreleased]

### Changed
- **The copies under `submodules/` no longer carry Kyoto's Dst data (2026-11-16).** The copies of `gannon-storm-rtk-analysis`, `helios-spaceweather-connectors` and `helios-fusion-engine` were refreshed from this repository's own copies of those projects. The first is `v0.2.0`, which no longer downloads, stores, plots or uses the Dst index; the second tests its Dst path against invented values, and its GFZ fixture no longer carries the sunspot numbers, which are CC BY-NC 4.0; the third brings its manuscript, rebuilt from the current source. The World Data Center for Geomagnetism, Kyoto, does not allow commercial applications of its indices.
- The companion's footnote on the Gannon analysis, the landing page and the README give the regenerated headline (1,283 station-hours; 1,302 in `v0.1.0`), and the blog post copy is updated with a dated note. The companion's artifact table names `v0.2.0` of the analysis and links to this repository's copy of it, as do the README, the landing page and the blog post copy. Dated records are left as written: the review packs under `specs/`, the plan, the social posts, other working documents and this folder's `CLAUDE.md` (whose release table is a dated snapshot) still describe `v0.1.0`, and one review pack quotes the Dst minimum it reported.
- **Links lead to this repository (2026-11-16).** The README, the companion document, the landing-page template, the pre-registration template, `mkdocs.yml` and the files under `templates/` linked the standalone repositories of the connectors, the fusion engine and this program, and their documentation sites. They link the folders under `programs/helios/`. The README's badges for the standalone repository's CI and releases are gone, and its quick start clones this repository.
- **`companion/footnotes.yaml` is kept by hand (2026-11-16).** `orchestration/companion_sync.py` generated it from the standalone repositories' releases; that script now does nothing unless it is given `--standalone`, since it would write those addresses back. Its entries for the connectors, the fusion engine and the storm analysis name their folders in this repository, the analysis is at 0.2.0, and its `pypi` fields are empty because none of the packages is on PyPI.
- The copies under `submodules/` of the same three projects were refreshed again from their sibling folders, the storm analysis now with link changes made after `v0.2.0`. The README's list says of each copy what changed after the version it names, the schema's copy included (wording, on 2026-11-10, in six files).
- Left as written, because the standalone repositories are their subject: `CLAUDE.md`, `OPERATOR_TODO.md`, `docs/operations.md`, `.gitmodules`, the dated entries of this file, and the dated working folders (`specs/`, `plan/`, `phase-ii/`, the social posts). `CLAUDE.md`, `OPERATOR_TODO.md`, `docs/operations.md` and four documents under `phase-ii/` carry a dated note at their head saying so, and that their links to the standalone repositories may no longer resolve.
- The companion's footnote on the fusion engine gives today's test count and coverage (176 tests, 89%); it gave those of the first release. Its footnote on the schema says that the RFC's issue is read-only now. Its stamp gives what changed on 2026-11-16 and the date the text was last revised, 2026-11-10.

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
