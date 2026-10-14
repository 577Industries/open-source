# 0001 Repo Split

Decision: maintain `01_TIER3_RESEARCH/AegisGraph_Tier3_Research/` as the public/open-core engineering repo and preserve `02_PUBLIC_RELEASE/ASEMA_Public_GitHub_Artifacts/` as the sanitized evaluator-facing artifact repo.

Rationale: Tier 3 work introduces ReproChain, PolyDiff, extraction, benchmark, and disclosure outputs with different release classifications. The engineering implementation can be public/open-core, while gated evidence classes remain excluded from the sanitized feasibility release until `make export-public-sanitized`, sanitize-check, and human review approve publication. The public artifact repo remains stable until a sanitized export is approved.

Status: accepted.

## Source map

The machine-readable release map is `docs/source-map/aegisgraph-open-core-source-map.json`. It pins:

- engineering open-core repo: `v1.0.0-tier3-research` / `d91c1df6`
- sanitized public artifact repo: `v1.0.0-asema-dp2-feasibility` / `ac83e3f5`
- proposal Volume 2 v1.1 sources under `03_PROPOSAL/active-package/`
- evidence tiers: `backed_now`, `backed_with_caveat`, `planned_gated`

Verification commands:

```bash
python3 -m json.tool docs/source-map/aegisgraph-open-core-source-map.json >/tmp/aegisgraph-open-core-source-map.pretty.json
make tooling-strict
python3 -m pytest -q
make validate
make reproduce
python3 -m validator.cli sanitize-check exports/public-sanitized/
node 05_verification/validate-evidence.mjs --version v0.4
node 05_verification/validate-cetm.mjs --version v0.4 04_evidence/v0.4/cetm.json
python3 05_verification/render-volume2.py
```

## Safety boundary

The open-core boundary does not authorize live probing, credentialed testing, raw third-party target-source redistribution, or raw crash-byte publication. Crash-triggering bytes remain hash-only, and planned-gated outputs require written authorization plus the public-export human gate before they can leave the engineering side.

## Related

- 0002 — private ReproChain handling (defines gated evidence classes excluded from sanitized release by default)
- 0011 — public-export human gate (the human-approved sanitized-export boundary referenced above)
- 0012 — integration merge-ready (defines the merge surface used by the Tier-3 engineering repo)

## Proposal claims

- C-EVAL-2 — sanitize-gate posture is downstream of the repo-split decision (open-core engineering vs. sanitized-release boundary).
- C-NOT-1 — the boundary table in the proposal is consistent with this split.
