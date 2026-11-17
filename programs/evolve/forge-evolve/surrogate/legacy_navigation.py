"""Synthetic legacy navigation & coordinate wrap surrogate (COBOL/Fortran/C port fixture)."""
import math

def legacy_wrap_longitude_deg(lon_deg: float) -> float:
    """Legacy half-open [-180, 180) wrap rule with anti-meridian sign quirk."""
    wrapped = ((lon_deg + 180.0) % 360.0) - 180.0
    return -180.0 if abs(wrapped - 180.0) < 1e-12 else wrapped

def candidate_wrap_longitude_deg(lon_deg: float) -> float:
    """Modernized candidate preserving exact [-180, 180) anti-meridian contract."""
    val = math.fmod(lon_deg + 180.0, 360.0)
    if val < 0.0:
        val += 360.0
    res = val - 180.0
    return -180.0 if abs(res - 180.0) < 1e-12 else res
