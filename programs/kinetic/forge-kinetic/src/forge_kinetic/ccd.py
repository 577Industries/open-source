"""Swept-capsule clearance profile stub.

Placeholder: returns fixed values; not a kinematics, collision or post-processing implementation.
The "clearance" series is a hand-shaped analytic curve clamped at 55.04 mm. No geometry, signed
distance field, robot model or control loop is involved; control_rate_hz is recorded but unused.
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

@dataclass(frozen=True)
class SweptCcdSummary:
    control_rate_hz: int
    safety_floor_mm: float
    min_clearance_kinetic_mm: float
    min_clearance_naive_mm: float
    naive_collisions: int
    kinetic_collisions: int
    clearance_series_mm: List[float]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

def evaluate_6link_swept_ccd(control_rate_hz: int = 200, safety_floor_mm: float = 45.0) -> SweptCcdSummary:
    """Placeholder: returns fixed values; not a kinematics, collision or post-processing implementation.

    The returned minimum is np.maximum(curve, 55.04), so it is 55.04 or higher by construction.
    """
    t = np.linspace(0.0, 1.0, 40)
    kinetic_curve = 62.0 - 6.96 * np.exp(-((t - 0.48) / 0.14) ** 2) + 4.5 * np.sin(2 * np.pi * t)
    kinetic_curve = np.maximum(kinetic_curve, 55.04)
    naive_curve = 54.0 - 72.3 * np.exp(-((t - 0.50) / 0.11) ** 2)
    return SweptCcdSummary(
        control_rate_hz=control_rate_hz,
        safety_floor_mm=safety_floor_mm,
        min_clearance_kinetic_mm=round(float(np.min(kinetic_curve)), 2),
        min_clearance_naive_mm=round(float(np.min(naive_curve)), 2),
        naive_collisions=int(np.sum(naive_curve < 0.0)),
        kinetic_collisions=int(np.sum(kinetic_curve < safety_floor_mm)),
        clearance_series_mm=[round(float(v), 2) for v in kinetic_curve],
    )
