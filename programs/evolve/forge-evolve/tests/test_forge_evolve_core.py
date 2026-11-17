"""Unit & integration tests for the 577 Industries Evolve Core Modernization Engine."""
from forge_evolve import (
    discover_dependency_graph,
    lift_to_clar,
    DifferentialOracle,
    ProvenanceHashchain,
)

def test_tarjan_scc_and_discovery():
    disc = discover_dependency_graph()
    assert len(disc.modules) == 4
    assert any(len(scc) == 2 for scc in disc.sccs)

def test_clar_precision_tagging():
    clar = lift_to_clar()
    assert clar.schema_version == "CLAR-2.4"
    assert all(n.precision_critical for n in clar.nodes)

def test_signed_angle_and_ulp_equivalence():
    oracle = DifferentialOracle()
    inputs = [-180.0, -90.0, 0.0, 90.0, 180.0, 540.0]
    fn = lambda x: -180.0 if abs((((x + 180.0) % 360.0) - 180.0) - 180.0) < 1e-12 else (((x + 180.0) % 360.0) - 180.0)
    rep = oracle.compare_corpus("boundary_test", inputs, fn, fn)
    assert rep.passed_cases == len(inputs)
    assert rep.max_abs_error == 0.0

def test_hashchain_provenance_integrity():
    chain = ProvenanceHashchain()
    chain.append("discover", {"a": 1})
    chain.append("clar", {"b": 2})
    assert chain.verify() is True
    assert len(chain.steps) == 2
