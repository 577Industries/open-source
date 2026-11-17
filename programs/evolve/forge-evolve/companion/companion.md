# Reviewer Companion — `forge-evolve` Core Engine

| Engine Stage | Module | Verification Test | Output Artifact |
|---|---|---|---|
| 1. Dependency & Boundary Discovery | `src/forge_evolve/discovery.py` | `tests/test_forge_evolve_core.py::test_tarjan_scc_and_discovery` | `results/discovery-report.json` |
| 2. Cross-Language Abstract Representation (CLAR) | `src/forge_evolve/clar.py` | `tests/test_forge_evolve_core.py::test_clar_precision_tagging` | `results/clar-graph.json` |
| 3. Differential Equivalence Harness (Signed-Angle & Numerical Boundaries) | `src/forge_evolve/equivalence.py` | `tests/test_forge_evolve_core.py::test_signed_angle_and_ulp_equivalence` | `results/equivalence-report.json` |
| 4. Hashchain Provenance & Review Ledger | `src/forge_evolve/governance.py` | `tests/test_forge_evolve_core.py::test_hashchain_provenance_integrity` | `results/provenance-ledger.json` |
