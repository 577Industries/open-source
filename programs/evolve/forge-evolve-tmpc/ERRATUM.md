# ERRATUM (2026-10-15)

This erratum corrects statements made in this repository, in its companion site and in the proposal materials that cited it. It applies to every revision up to and including the tag `v0.1.0-sbir-DON26BZ01-NV013`.

## (a) The cited Evolve paper is withdrawn as a citation

Earlier versions of `NOTICE`, `README.md`, `RELEASE_APPROVAL.md`, `evidence/cetm.json` (rows `C-FORGE-BENCH` and `C-AIRGAP-QUALITY`), `clar-spec/profiles/vb6.md`, `surrogate/DEBT.md` and a comment in `surrogate/tmpc-surrogate-mds/legacy/GeoFixedPoint.bas` referred to "prior published results", "internal prior art" and an internal draft paper (`forge-evolve.pdf`). That draft reported 30 codebases, 3.257M LOC, 4,972 extracted rules, pass rates of 99.x% and a local-model mode at "~94% of cloud-frontier quality". Its figures and tables were produced by a script from random draws, not measured, and no code in any 577 Industries repository reproduces them. No published results exist; an internal draft paper cited here earlier contained generated figures and is withdrawn as a citation (see ERRATUM.md). Every sentence that leaned on it now carries that statement instead.

## (b) The CLAR lifter is template-based

`src/ForgeEvolve.Clar/ClarLifter.cs` emits a fixed mission-domain CLAR document whatever module it is given. The document validates against the frozen `clar-spec/CLAR.schema.json`, but its content is not derived from the parsed source. Nothing downstream consumes the CLAR document except a hash used for routing.

## (c) The rule-extraction F1 and the latent-defect precision and recall are circular

`src/ForgeEvolve.Discovery/RuleExtractor.cs` recognizes the surrogate by name (`ProcessMission`, `WrapDlon`, `TurnAngleDeg`, `InitialBearingDeg`, and the literals `"MST"` and `"SSN"`). The gold set in `surrogate/gold/business-rules.gold.ttl` was authored together with those probes and keyed to the same surrogate identifiers, so the reported F1 of 1.0 measures agreement between two artifacts written by the same hand. Likewise, `src/ForgeEvolve.Validation/DivergenceDetector.cs` re-implements the rule in `surrogate/reference/reference.py` that produced the 321 "ground truth" divergent vectors, so precision = recall = 1.0 is a tautology, not a detection result.

## (d) The "AI transformation" replays pre-written files and no language model is called

`src/ForgeEvolve.Transformation/TransformationEngine.cs` copies the hand-refactored files in `tmpc-modern-mds/src` into the result and sets `CompiledClean = true` and `QualityEstimate = 1.0` as constants. The orchestrator's live bridge, `orchestrator/src/cli.ts`, hardcodes `liveRuntimeAvailable = false` and exits with status 3 before any model call, so the local and cloud modes select a model but never invoke one. The recorded "transcript" holds no prompt, no response and no model identifier. The Thompson-sampling priors in `CapabilityRegistry.cs` are illustrative and were not derived from telemetry.

## (e) What the 137 tests and the 2000/2000 equivalence result do show

The 137 xUnit cases pass, and the differential run of the legacy surrogate against the hand-refactored modern component is equivalent on 2000 of 2000 corpus vectors, with the expected intentional divergences classified as such. The cyclomatic-complexity reduction from 49 to 6 is measured by Roslyn on both sides. These results stand as a demonstration of the verification harness on a hand-written surrogate pair. They are not evidence of automated or AI-assisted modernization, because no model produced the modern component.

## (f) Funding and status

Topic DON26BZ01-NV013, for which this repository was built, was never submitted. The work is internally funded by 577 Industries Inc. and carries no government validation or endorsement.

## What is unchanged

`EXCLUSIONS.md` and `REPRODUCIBILITY.md` remain accurate: the surrogate is synthetic and unclassified, and `make demo` reproduces the harness results offline. The frozen contracts, the Roslyn analyzer, the hash chain with Merkle root, the review gates and the seeded corpus generator are real code and remain available for reuse.
