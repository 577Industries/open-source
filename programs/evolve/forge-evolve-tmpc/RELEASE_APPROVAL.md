# Release Approval - Public Publication Gate

This repository is **publish-ready** but is held **pending PI authorization** (gate H6). It will be
pushed to **github.com/577Industries/forge-evolve-tmpc** under 577's own GitHub credentials. Agents
prepare the release; the Principal Investigator authorizes and executes the push.

## What is published
The entire repository, Apache-2.0. It is a **clean-room** TMPC-reference implementation containing
**no** 577 proprietary Evolve / FORGE OS engine internals, **no** model weights, and **no**
real/controlled TMPC data - so there is nothing to sanitize or split out. See `EXCLUSIONS.md`.

## Pre-publication verification (all PASS at the frozen commit)
- [x] `make build` - solution builds, 0 warnings / 0 errors (24 projects)
- [x] `make test` - 137 unit tests pass, 0 failures
- [x] `make demo` - runs offline, no API keys, end-to-end
- [x] `make verify` - byte-deterministic across runs
- [x] `make audit` - CETM `issues_count: 0`
- [x] Independent security/ITAR audit - **no secrets, no real/controlled data, Apache-2.0 clean, safe to publish**
- [x] No absolute build paths / usernames in committed artifacts (recursive username/home-path grep over `results/` → clean)
- [x] CI workflow (`.github/workflows/demo-offline.yml`) runs build + test + offline demo + secret scan on push

## Reviewer reproduction contract (what a reviewer does)
```bash
git clone https://github.com/577Industries/forge-evolve-tmpc
cd forge-evolve-tmpc            # checkout the frozen release commit
make demo                       # offline, no keys; prints the headline metrics
make verify                     # confirms byte-determinism
make test                       # 137 passing tests
```
Prerequisite: .NET SDK 8 (pinned in `global.json`), Node 18+. See `REPRODUCIBILITY.md`.

## Honest scope of claims (re-affirmed at release)
All quantitative results are measured on the **synthetic, unclassified surrogate**, are **preliminary**,
and are **not government-validated**. No published results exist; an internal draft paper cited here
earlier contained generated figures and is withdrawn as a citation (see ERRATUM.md). The C#/.NET/JS/SQL
capability here is the newly developed extension. When this approval was written, CMMC L2 (Self),
ITAR/DDTC registration and a facility clearance were not in place.

## PI authorization (H6)
- [ ] Frozen release commit: `__________________` (full SHA - set at push)
- [ ] Tag pushed: the v0.1.0 release tag, exactly as named in the deep links of `docs/artifacts.md`
- [ ] Repo set **public** on github.com/577Industries
- [ ] Approved by: Thomas Waweru, Ph.D. (PI) - date: __________
