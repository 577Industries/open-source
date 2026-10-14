"""Sensor operating envelope, frustum visibility, and human takeover boundary."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass(frozen=True)
class SensorEnvelopeResult:
    standoff_mm: float
    fov_deg: float
    occluder_offset_ratio: float
    visible_target_fraction: float
    incident_angle_deg: float
    hitl_takeover_required: bool
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

def compute_sensor_envelope(
    standoff_mm: float = 780.0,
    fov_deg: float = 42.0,
    occluder_offset_ratio: float = 0.18,
) -> SensorEnvelopeResult:
    vis = max(0.0, min(1.0, 1.0 - max(0.0, 0.35 - occluder_offset_ratio) * 1.9))
    incident = 14.5 + (780.0 - standoff_mm) * 0.015
    takeover = vis < 0.85 or standoff_mm < 420.0 or standoff_mm > 1150.0
    reason = "nominal_autonomous_envelope" if not takeover else "operator_handoff_occlusion_or_standoff_limit"
    return SensorEnvelopeResult(
        standoff_mm=round(standoff_mm, 2),
        fov_deg=round(fov_deg, 2),
        occluder_offset_ratio=round(occluder_offset_ratio, 4),
        visible_target_fraction=round(vis, 4),
        incident_angle_deg=round(incident, 2),
        hitl_takeover_required=takeover,
        reason=reason,
    )
