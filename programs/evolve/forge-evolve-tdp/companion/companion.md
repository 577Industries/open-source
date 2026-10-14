# Reviewer Companion — `forge-evolve-tdp` (`DAF27BZ01-DV008`)

| Proposal Claim (DAF27BZ01-DV008) | Backing File / Module | Verification Test |
|---|---|---|
| Canonical TDP Graph (`cTDPg`) & `AS_DESIGNED -> AS_BUILT -> AS_SUSTAINED` Merkle-DAG | `forge_evolve_engine.py`, `schemas/canonical_tdp_graph.schema.json` | `tests/test_ctdpg_merkle.py` |
| Zero-Trust OPA ABAC Policy Gate (`MIL-STD-31000B` / ITAR / CMMC L2) | `schemas/ia_compliance.rego` | `tests/test_ctdpg_merkle.py::test_opa_ia_compliance_gates` |
| Multi-Format TDP Exception Recovery (`EXC-01` .. `EXC-06`) | `run_adversarial_benchmarks.py` | `tests/test_exception_recovery.py` |
