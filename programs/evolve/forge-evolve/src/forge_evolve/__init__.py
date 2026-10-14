"""577 Industries — Evolve Core Modernization Engine."""
from .discovery import discover_dependency_graph, tarjan_scc
from .clar import ClarNode, ClarModule, lift_to_clar
from .equivalence import DifferentialOracle, EquivalenceReport
from .governance import ProvenanceHashchain

__all__ = [
    "discover_dependency_graph",
    "tarjan_scc",
    "ClarNode",
    "ClarModule",
    "lift_to_clar",
    "DifferentialOracle",
    "EquivalenceReport",
    "ProvenanceHashchain",
]
