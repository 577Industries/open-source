# Contributing to 577 Industries

Thanks for your interest. Everything public in this organization ships with a license, CI, and citable evidence — contributions are held to the same bar we hold ourselves to.

## How the organization is laid out

Work is grouped into **programs**, each marked by a `577i-program-*` topic on its repositories:

| Program | Topic | What it is |
|---|---|---|
| HELIOS | `577i-program-helios` | Calibrated heliophysics fusion (NASA SBIR) |
| FORGE EVOLVE | `577i-program-forge-evolve` | AI-assisted legacy modernization (Navy SBIR) |
| AEGIS | `577i-program-aegis` | Secure-messaging assessment (DARPA ASEMA) |
| FORGE OS | `577i-program-forge-os` | Reusable TypeScript agent-infrastructure libraries |

Conventions that every repo follows (topics, badges, README shape, releases) are written down in [`docs/repo-standards.md`](https://github.com/577Industries/.github/blob/main/docs/repo-standards.md).

## Ground rules

- **Conventional commits** — `feat:`, `fix:`, `docs:`, `test:`, `chore:`, `refactor:` (you'll see `docs(plan):`-style scopes throughout the history).
- **PRs over pushes** — branch, open a PR, let CI run. Squash-merge is the norm.
- **Tests ride along** — a behavior change without a test needs a stated reason.
- **Claims need evidence** — if a README or doc states a number, it must be reproducible from the repo or cited. This is a firm house rule.

## Evaluation-frozen repositories

Repositories under active government evaluation say so in their READMEs (currently the AEGIS program repos). During an evaluation window they **accept issues but not external PRs**, and their names, URLs, and descriptions are frozen. Security reports are always welcome — see [SECURITY.md](SECURITY.md).

## Questions and contact

- Bugs and feature requests → the repo's issue templates
- Security → [SECURITY.md](SECURITY.md)
- Everything else → [info@577industries.com](mailto:info@577industries.com)
