"""Geomagnetic-index fetcher for the Gannon storm window.

The module is named ``swpc`` because NOAA SWPC is the operational US source
of the Kp index, but for the May 2024 archive we use the upstream source that
keeps the full history:

- **Kp** — GFZ Helmholtz Centre for Geosciences,
  ``https://kp.gfz.de/app/files/Kp_ap_since_1932.txt``. CC BY 4.0; GFZ asks
  users to cite Matzka et al. (2021), https://doi.org/10.1029/2020SW002641.
  Three-hourly resolution. Same series SWPC publishes for the current
  30-day window, with the full historical archive available.

The source is freely accessible without authentication. A fixture file is
shipped under ``tests/fixtures/`` so unit tests do not hit the network.

Kp is the only index this package reads. Version 0.1.0 also downloaded the
hourly Dst index from the World Data Center for Geomagnetism, Kyoto. That
centre's data service does not allow commercial applications of its indices,
so the fetcher, its parser and its fixture were removed in 0.2.0.
"""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta
from pathlib import Path

import httpx
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

KP_ARCHIVE_URL: str = "https://kp.gfz.de/app/files/Kp_ap_since_1932.txt"
"""GFZ Kp archive (CC BY 4.0). One line per 3-hour Kp interval."""

GANNON_WINDOW_START: date = date(2024, 5, 8)
"""First UTC date of the analysis window."""

GANNON_WINDOW_END: date = date(2024, 5, 14)
"""Last UTC date of the analysis window."""


def _kp_from_index(kp: float) -> str:
    """Return the NOAA G-scale letter for a given Kp value.

    Reference: https://www.swpc.noaa.gov/noaa-scales-explanation
    """
    if kp < 5.0:
        return "G0"
    if kp < 6.0:
        return "G1"
    if kp < 7.0:
        return "G2"
    if kp < 8.0:
        return "G3"
    if kp < 9.0:
        return "G4"
    return "G5"


def fetch_kp(
    start: date = GANNON_WINDOW_START,
    end: date = GANNON_WINDOW_END,
    *,
    client: httpx.Client | None = None,
    cache_path: Path | None = None,
) -> pd.DataFrame:
    """Fetch GFZ Kp data and slice to ``[start, end]`` inclusive.

    Returns:
        DataFrame indexed by UTC datetime with columns:
            kp: float Kp value (0.0-9.0 in 1/3 increments)
            ap: int ap-index (geomagnetic equivalent amplitude, nT)
            g_scale: str NOAA G-scale (e.g. "G5")
    """
    text = _fetch_text(KP_ARCHIVE_URL, client=client, cache_path=cache_path)
    rows: list[tuple[datetime, float, int]] = []
    for line in text.splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split()
        if len(parts) < 8:
            continue
        try:
            y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
            hh = float(parts[3])
            kp = float(parts[7])
            ap = int(parts[8])
        except (IndexError, ValueError):
            continue
        if kp < 0:  # missing data sentinel
            continue
        dt = datetime(y, m, d) + timedelta(hours=hh)
        rows.append((dt, kp, ap))
    if not rows:
        raise RuntimeError("Parsed zero rows from GFZ Kp archive")
    df = pd.DataFrame(rows, columns=["time_utc", "kp", "ap"])
    df = df.set_index("time_utc")
    start_dt = datetime.combine(start, datetime.min.time())
    end_dt = datetime.combine(end, datetime.max.time())
    df = df.loc[start_dt:end_dt].copy()
    df["g_scale"] = df["kp"].apply(_kp_from_index)
    return df


def _fetch_text(
    url: str,
    *,
    client: httpx.Client | None,
    cache_path: Path | None,
    timeout_sec: float = 60.0,
) -> str:
    """Fetch a text resource, with optional on-disk cache."""
    if cache_path is not None and cache_path.exists():
        logger.debug("cache hit %s", cache_path)
        return cache_path.read_text(encoding="utf-8", errors="replace")
    own_client = client is None
    cli = client or httpx.Client(timeout=timeout_sec)
    try:
        resp = cli.get(url)
        resp.raise_for_status()
        text = resp.text
    finally:
        if own_client:
            cli.close()
    if cache_path is not None:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(text, encoding="utf-8")
    return text


def join_kp_to_minute_grid(kp_df: pd.DataFrame, *, minute_freq: str = "1min") -> pd.DataFrame:
    """Upsample 3-hourly Kp to a minute-cadence index.

    Kp is constant within each 3-hour interval, so forward-fill is the
    physically correct interpolation.
    """
    if kp_df.empty:
        return kp_df.copy()
    start = kp_df.index.min()
    end = kp_df.index.max() + pd.Timedelta(hours=3)
    grid = pd.date_range(start=start, end=end, freq=minute_freq, inclusive="left")
    out = kp_df.reindex(grid, method="ffill")
    out.index.name = "time_utc"
    return out


def kp_severity_color(kp: float) -> str:
    """Return a matplotlib color string for a given Kp value (G-scale ramp)."""
    # Severity ramp: green (quiet) -> yellow -> orange -> red -> magenta (G5)
    if not np.isfinite(kp):
        return "#cccccc"
    if kp < 4.0:
        return "#2ca02c"  # green
    if kp < 5.0:
        return "#bcbd22"  # olive
    if kp < 6.0:
        return "#ff7f0e"  # orange (G1)
    if kp < 7.0:
        return "#d62728"  # red (G2)
    if kp < 8.0:
        return "#9467bd"  # purple (G3)
    if kp < 9.0:
        return "#e377c2"  # pink (G4)
    return "#7f0000"  # dark red (G5)
