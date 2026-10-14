"""Dependency discovery and Tarjan strongly connected components (SCC) analysis."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List

@dataclass(frozen=True)
class DiscoverySummary:
    modules: List[str]
    sccs: List[List[str]]
    cyclomatic_estimate: int
    boundary_functions: List[str]

def tarjan_scc(graph: Dict[str, List[str]]) -> List[List[str]]:
    index = 0
    indices: Dict[str, int] = {}
    lowlink: Dict[str, int] = {}
    stack: List[str] = []
    on_stack = set()
    sccs: List[List[str]] = []

    def strongconnect(v: str):
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)
        for w in graph.get(v, []):
            if w not in indices:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], indices[w])
        if lowlink[v] == indices[v]:
            comp = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                comp.append(w)
                if w == v:
                    break
            sccs.append(comp)

    for node in graph:
        if node not in indices:
            strongconnect(node)
    return sccs

def discover_dependency_graph() -> DiscoverySummary:
    graph = {
        "legacy_CoordinateWrap": ["legacy_GeodesicStep"],
        "legacy_GeodesicStep": ["legacy_WaypointSolver"],
        "legacy_WaypointSolver": ["legacy_GeodesicStep"],
        "legacy_TelemetryExport": ["legacy_CoordinateWrap"],
    }
    sccs = tarjan_scc(graph)
    return DiscoverySummary(
        modules=list(graph.keys()),
        sccs=sccs,
        cyclomatic_estimate=18,
        boundary_functions=["legacy_wrap_longitude_deg", "geodesic_bearing_rad"],
    )
