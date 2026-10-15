# Reviewer Companion: `forge-evolve-tdp` (`DAF27BZ01-DV008`)

Design elements of the study and where the placeholder code lives. No row below is evidence of a measured result.

| Design element | Backing File / Module | Self-check test | Status |
|---|---|---|---|
| Canonical TDP Graph (`CTDP-G`) and `AS_DESIGNED -> AS_BUILT -> AS_SUSTAINED` hash-chained lineage | `forge_evolve_engine.py` (`ZeroTrustMerkleLedger`), `schemas/CTDP_Graph_and_URTS_Schema_Specification.md` (unimplemented draft) | `tests/test_ctdpg_merkle.py::test_deterministic_merkle_dag_lineage_and_pydantic_schema` | Hash chain and Merkle root are real; signing and encryption are not implemented |
| Zero-trust OPA ABAC policy gate (`MIL-STD-31000B` / ITAR / CMMC L2) | `schemas/ia_compliance.rego` (never evaluated); six Python booleans in `forge_evolve_engine.py` | `tests/test_ctdpg_merkle.py::test_six_opa_ia_compliance_gates_pass_100pct` | The 99.4 "score" is a constant |
| Multi-format TDP exception recovery (`EXC-01` .. `EXC-06`) | `forge_evolve_engine.py` (`TDPExceptionRecoveryEngine`) | `tests/test_exception_recovery.py` | EXC-01, 02, 04, 05 and 06 are trivial arithmetic; EXC-03 and the 225-case totals are lookup tables |
