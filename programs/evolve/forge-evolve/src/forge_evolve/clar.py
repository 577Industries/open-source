"""Cross-Language Abstract Representation (CLAR) 4-layer model."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

@dataclass(frozen=True)
class ClarNode:
    node_id: str
    layer: str  # syntax | control_flow | data_contract | domain_rule
    source_lang: str
    symbol: str
    precision_critical: bool
    unit_contract: str
    invariants: List[str]

@dataclass(frozen=True)
class ClarModule:
    schema_version: str
    module_name: str
    nodes: List[ClarNode]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

def lift_to_clar(module_name: str = "navigation_core", source_lang: str = "Fortran77/C") -> ClarModule:
    nodes = [
        ClarNode(
            node_id="CLAR-001",
            layer="domain_rule",
            source_lang=source_lang,
            symbol="wrap_longitude_deg",
            precision_critical=True,
            unit_contract="degrees [-180.0, +180.0)",
            invariants=["anti_meridian_180_maps_to_minus_180", "period_360_exact"],
        ),
        ClarNode(
            node_id="CLAR-002",
            layer="data_contract",
            source_lang=source_lang,
            symbol="geodesic_arc_distance_m",
            precision_critical=True,
            unit_contract="meters (WGS-84 ellipsoid)",
            invariants=["rel_error_le_1e_12", "non_negative_metric"],
        ),
    ]
    return ClarModule(schema_version="CLAR-2.4", module_name=module_name, nodes=nodes)
