<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/577Industries/.github/main/profile/assets/banner-dark.png">
  <img alt="577 Industries — Engineering for missions where failure is not an option." src="https://raw.githubusercontent.com/577Industries/.github/main/profile/assets/banner-light.png" width="830">
</picture>

<br><br>

[![Website](https://img.shields.io/badge/577industries.com-visit-5eb5ff?style=flat-square)](https://577industries.com)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache_2.0-blue?style=flat-square)](https://www.apache.org/licenses/LICENSE-2.0)
[![Patents](https://img.shields.io/badge/patents-5_described-7c3aed?style=flat-square)](#forge-os--agent-infrastructure)
[![npm](https://img.shields.io/badge/npm-@577--industries-cb3837?style=flat-square)](https://www.npmjs.com/search?q=%40577-industries)

Columbus, Ohio · Dual-use commercial & defense

</div>

---

577 Industries works across four engineering domains where rigor, provenance, and calibration matter more than throughput:

- 🧠 **AI/ML R&D** — calibrated decision systems, agent infrastructure, and applied research at the model–physics boundary
- 🤖 **Robotics** — autonomy stacks, perception, manipulation, and swarm coordination
- 🔧 **Code modernization** — legacy migration, AI-assisted refactoring, and secure modernization
- ⚛ **Frontier research** — high-energy physics, quantum sensing, and post-quantum security

Every public artifact ships with a license, a CI badge, and citable evidence. Every internal artifact is gated by a documented IP boundary. Programs land in this org iteratively as they ship; the active set is below.

```mermaid
%%{init: {'theme':'neutral'}}%%
flowchart LR
    ORG(["577 Industries"]):::org
    ORG --- HELIOS["☀ HELIOS<br/>calibrated space-weather fusion"]
    ORG --- EVOLVE["⚙ FORGE EVOLVE<br/>verified legacy modernization"]
    ORG --- AEGIS["🛡 AEGIS<br/>secure-messaging assessment"]
    ORG --- FOS["⛭ FORGE OS<br/>agent infrastructure libraries"]
    ORG --- FI["🌐 FORGE INTELLIGENCE<br/>OSINT fusion console"]
    ORG --- QS["⚛ QSPARX<br/>post-quantum migration planning"]
    HELIOS --- hp["helios-program<br/>+ 4 artifact repos"]
    EVOLVE --- fe["forge-evolve-tmpc"]
    AEGIS --- ag["aegisgraph<br/>engine + review collection"]
    FOS --- fl["forge-os-libs<br/>5 packages, one repo"]
    FI --- fi["forge-intelligence"]
    QS --- qs["forge-qbit-qsparx"]
    classDef org font-weight:bold
```

---

## HELIOS — Calibrated Heliophysics Fusion

Multi-source space-weather fusion with feature-level provenance and calibrated uncertainty. Two vertical slices: mission-operations radiation risk and U.S. precision-agriculture GNSS reliability.

> [!NOTE]
> **Headline result.** During the May 2024 Gannon G5 superstorm, **1,302 station-hours** of U.S. row-crop GNSS pushed past the 2.5 cm RTK tolerance — the first citable quantification of solar-storm impact on U.S. agriculture. (Climatological v1; real-SPP v2 in progress.)

| Repository | Purpose |
|---|---|
| [`helios-program`](https://github.com/577Industries/helios-program) | Umbrella meta-repo · master plan, 4 submodules |
| [`helios-provenance-spec`](https://github.com/577Industries/helios-provenance-spec) | JSON Schema 2020-12 + W3C PROV-JSON RFC for feature-level lineage |
| [`helios-spaceweather-connectors`](https://github.com/577Industries/helios-spaceweather-connectors) | 6 production adapters · DONKI, SEP A/B/C, SWPC, GOES, DSCOVR, CDDIS GIMs |
| [`helios-fusion-engine`](https://github.com/577Industries/helios-fusion-engine) | BMA + isotonic + Mondrian conformal calibration · arXiv preprint draft |
| [`gannon-storm-rtk-analysis`](https://github.com/577Industries/gannon-storm-rtk-analysis) | May 2024 Gannon G5 retrospective on the NGS CORS network |

**Companion site →** [577industries.github.io/helios-program](https://577industries.github.io/helios-program/)

---

## FORGE EVOLVE for TMPC — a verification harness for modernized mission-planning software

[![demo-offline](https://img.shields.io/github/actions/workflow/status/577Industries/forge-evolve-tmpc/demo-offline.yml?style=flat-square&label=demo-offline)](https://github.com/577Industries/forge-evolve-tmpc/actions/workflows/demo-offline.yml)

A C#/.NET reference for the verification side of code modernization: a differential harness that runs a legacy mission-planning component against its modernized replacement, with continuous-ATO evidence generated as a byproduct. The workload is a synthetic, unclassified surrogate shaped like Theater Mission Planning Center (TMPC) software. It is the C#/.NET extension of 577's FORGE EVOLVE modernization framework and runs offline with no API keys. The repository's [`ERRATUM.md`](https://github.com/577Industries/open-source/blob/main/programs/evolve/forge-evolve-tmpc/ERRATUM.md) states what it does and does not show.

> [!NOTE]
> **Headline result.** On a synthetic, unclassified MDS-like surrogate, a hand-refactored .NET 8 component reproduces its legacy counterpart on **2000/2000 corpus vectors** (95% rule-of-three upper bound ≈1.5×10⁻³ on the per-vector deviation rate), and Roslyn measures cyclomatic complexity falling from 49 to 6. STIG, NIST 800-53, CycloneDX SBOM, and a tamper-evident provenance hashchain are emitted automatically. No language model produced the modern component, so the result demonstrates the harness, not automated modernization. Preliminary; **not government-validated**.

| Repository | Purpose |
|---|---|
| [`forge-evolve-tmpc`](https://github.com/577Industries/forge-evolve-tmpc) | Runnable C#/.NET reference · Roslyn discovery, differential equivalence validation and cATO artifacts on a synthetic MDS-like surrogate; the transform stage replays hand-refactored files (see `ERRATUM.md`) · `make demo` runs offline and byte-deterministic · 137 tests · Apache-2.0 |

Consumes [`@577-industries/model-router`](https://github.com/577Industries/forge-os-libs/tree/main/packages/model-router) for air-gappable, sovereign-profile model routing.

**Companion site →** [577industries.github.io/forge-evolve-tmpc](https://577industries.github.io/forge-evolve-tmpc/)

---

## AEGIS — Secure Messaging Assessment

Graph-based application-layer evidence platform for assessing Secure Messaging Applications (project codename **AEGIS**).

> [!IMPORTANT]
> Published artifacts are the sanitized reproducibility set only; other project materials are not published.

| Repository | Purpose |
|---|---|
| [`aegisgraph`](https://github.com/577Industries/aegisgraph) | Assessment evidence platform · sanitize-check gates every public export |
| [AegisGraph review collection](https://github.com/577Industries/asema-feasibility-artifacts) | Sanitized reproducibility artifacts for AegisGraph · consolidated into the org 2026-07. GitHub redirects the repository URL from the former founder-account path; GitHub Pages URLs are not redirected on transfer, so the documents are served at [the collection's GitHub Pages site](https://577industries.github.io/asema-feasibility-artifacts/) |

In the [`open-source`](https://github.com/577Industries/open-source) monorepo the two are one project: the collection lives inside AegisGraph at [`programs/aegis/aegisgraph/review-collection/`](https://github.com/577Industries/open-source/tree/main/programs/aegis/aegisgraph/review-collection).

---

## FORGE OS — Agent Infrastructure

![license](https://img.shields.io/badge/license-Apache_2.0-blue?style=flat-square) ![patents](https://img.shields.io/badge/patents-5_described-7c3aed?style=flat-square) ![npm](https://img.shields.io/badge/npm-@577--industries-cb3837?style=flat-square)

Reusable TypeScript libraries for production AI-agent applications. Each library implements an algorithm described in a 2025–2026 patent filing. All five live in [`forge-os-libs`](https://github.com/577Industries/forge-os-libs) and publish independently to npm.

| Package | What it does | Patent (described) |
|---|---|---|
| [`agent-memory`](https://github.com/577Industries/forge-os-libs/tree/main/packages/agent-memory) | Persistent memory · log-reinforcement, exponential decay, composite recall | Autonomous Memory Evolution · Dec 2025 |
| [`model-router`](https://github.com/577Industries/forge-os-libs/tree/main/packages/model-router) | Multi-provider routing · 6 strategies, sovereign profiles, cost ceiling | Adaptive Model Routing · Feb 2026 |
| [`tool-guardrails`](https://github.com/577Industries/forge-os-libs/tree/main/packages/tool-guardrails) | 4-level tool middleware (none/log/pause/block) + HITL approval | Governed Autonomy Framework · Jan 2026 |
| [`workflow-dag`](https://github.com/577Industries/forge-os-libs/tree/main/packages/workflow-dag) | YAML → DAG compiler · Kahn topological sort, cycle detection | Workflow DAG Compiler · Mar 2026 |
| [`hashchain-audit`](https://github.com/577Industries/forge-os-libs/tree/main/packages/hashchain-audit) | Tamper-evident audit · SHA-256 chaining + Ed25519 + Merkle anchoring | Hash-Chained Audit Ledger · Mar 2026 |

<sub>Consolidated into one repository 2026-08-09; the five original repos are archived and read-only, with their releases and history preserved. Package names and versions are unchanged — `npm i @577-industries/model-router` works exactly as before. A rebrand to `@577industries/forge-*` is on the 2026 roadmap.</sub>

---

## FORGE INTELLIGENCE — OSINT Fusion Console

![license](https://img.shields.io/badge/license-Apache_2.0-blue?style=flat-square) ![upstream](https://img.shields.io/badge/upstream-hardened_fork_of_Osiris-6e7681?style=flat-square)

Real-time open-source-intelligence fusion: a WebGL globe over public-domain intelligence feeds, with a passive-first reconnaissance toolkit. A hardened fork of the MIT-licensed [Osiris](https://github.com/simplifaisoul/osiris), with the security work carried in-tree.

> [!NOTE]
> **Design rule.** An unavailable source reports unavailable — feeds never fabricate a data point, and routes fail closed. Non-commercial-only feeds are disqualified regardless of data quality.

| Repository | Purpose |
|---|---|
| [`forge-intelligence`](https://github.com/577Industries/forge-intelligence) | Fusion console · layer catalog, SSRF-guarded egress, tiered reconnaissance access |

---

## QSPARX — Post-Quantum Migration Planning

![license](https://img.shields.io/badge/license-Apache_2.0-blue?style=flat-square) ![sbom](https://img.shields.io/badge/SBOM-CycloneDX-262d3a?style=flat-square)

Evidence-first synthetic cryptographic mission twin for planning post-quantum migration: cryptographic inventory, CycloneDX SBOM generation, and a digital twin of the migration surface.

> [!NOTE]
> **Waiver discipline.** Container vulnerability waivers are exact, versioned, and expiry-dated. Any change to the runtime dependency scope invalidates them and forces reassessment before CI can pass — the control is enforced in `scripts/check_container_waivers.py`, not by convention.

| Repository | Purpose |
|---|---|
| [`forge-qbit-qsparx`](https://github.com/577Industries/forge-qbit-qsparx) | Cryptographic inventory + mission twin · signed releases, reviewer Pages site |

---

## Recent

| Date | Update |
|---|---|
| **2026-08-09** | FORGE OS libraries consolidated into [`forge-os-libs`](https://github.com/577Industries/forge-os-libs) (npm packages unchanged); FORGE INTELLIGENCE and QSPARX added as programs; reproducibility fixes across the HELIOS toolchain |
| **2026-07-07** | GitHub presence consolidated: AEGIS artifacts transferred into the org (redirects preserved), org-wide brand system + repo standards shipped, `v1.0.0` releases tagged across the FORGE OS libraries |
| **2026-06-01** | FORGE EVOLVE for TMPC reference implementation published · `make demo` reproducible offline · CI green on Linux + Windows |
| **2026-03** | `forge-workflow-dag` and `forge-hashchain-audit` patents described |
| **2026-02** | `forge-model-router` patent described |
| **2025-12** | `forge-agent-memory` patent described · first FORGE OS library shipped to npm |

---

<div align="center">

**Contact** · [info@577industries.com](mailto:info@577industries.com) · [Security policy](https://github.com/577Industries/.github/blob/main/SECURITY.md) · [Contributing](https://github.com/577Industries/.github/blob/main/CONTRIBUTING.md) · [Repo standards](https://github.com/577Industries/.github/blob/main/docs/repo-standards.md)

<sub>© 2025–2026 577 Industries Incorporated · Columbus, Ohio · Apache 2.0 except where noted</sub>

</div>
