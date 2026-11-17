"""Tests for the Kp index fetcher (GFZ archive)."""

from __future__ import annotations

import importlib
import re
from pathlib import Path

import pandas as pd
import pytest

import gannon_analysis
from gannon_analysis.swpc import (
    _kp_from_index,
    fetch_kp,
    join_kp_to_minute_grid,
    kp_severity_color,
)


def test_kp_g_scale_mapping() -> None:
    assert _kp_from_index(0.0) == "G0"
    assert _kp_from_index(3.0) == "G0"
    assert _kp_from_index(5.0) == "G1"
    assert _kp_from_index(6.0) == "G2"
    assert _kp_from_index(7.0) == "G3"
    assert _kp_from_index(8.0) == "G4"
    assert _kp_from_index(9.0) == "G5"


def test_fetch_kp_from_fixture(kp_fixture: Path, tmp_path: Path) -> None:
    cache = tmp_path / "kp.txt"
    cache.write_text(kp_fixture.read_text())
    df = fetch_kp(cache_path=cache)
    assert not df.empty
    assert df["kp"].max() == pytest.approx(9.0, abs=0.01)
    assert df["g_scale"].max() == "G5"
    # Kp is 7.667 in the 15:00-18:00 UT interval of 2024-05-10, 8.667 from
    # 18:00 UT, and reaches 9.000 on May 11.
    storm_window = df.loc[
        (df.index >= pd.Timestamp("2024-05-10 15:00"))
        & (df.index <= pd.Timestamp("2024-05-11 18:00"))
    ]
    assert storm_window["kp"].max() >= 8.0


def test_kp_is_the_only_index_this_package_reads() -> None:
    """The Dst index was removed in 0.2.0: no module has a fetcher, a parser or an address for it.

    Every module of the package is read, and the addresses they name are held to a list, so a
    new source cannot arrive in another module or under another name without failing this.
    """
    modules = sorted(Path(gannon_analysis.__file__).parent.glob("*.py"))
    assert {path.stem for path in modules} >= {
        "analysis",
        "fetch",
        "plotting",
        "positioning",
        "swpc",
    }
    hosts: set[str] = set()
    for path in modules:
        name = "gannon_analysis" if path.stem == "__init__" else f"gannon_analysis.{path.stem}"
        module = importlib.import_module(name)
        assert not {attr for attr in dir(module) if "dst" in attr.lower()}, path.name
        hosts.update(re.findall(r"https?://([^/\s\"'`)>]+)", path.read_text(encoding="utf-8")))
    assert hosts == {"doi.org", "geodesy.noaa.gov", "kp.gfz.de", "www.swpc.noaa.gov"}


def test_join_kp_to_minute_grid_forward_fills(kp_fixture: Path, tmp_path: Path) -> None:
    cache = tmp_path / "kp.txt"
    cache.write_text(kp_fixture.read_text())
    df = fetch_kp(cache_path=cache)
    minute = join_kp_to_minute_grid(df)
    # 7 days * 24 hours * 60 minutes = 10080, give or take.
    assert 5000 < len(minute) < 20000
    assert minute["kp"].notna().sum() / len(minute) > 0.95


def test_kp_severity_colors_distinct() -> None:
    colors = {
        kp_severity_color(0.0),
        kp_severity_color(5.5),
        kp_severity_color(7.5),
        kp_severity_color(9.0),
    }
    assert len(colors) == 4  # all distinct


@pytest.mark.integration
def test_fetch_kp_live(tmp_path: Path) -> None:
    """Live GFZ Kp archive fetch — opt-in."""
    df = fetch_kp(cache_path=tmp_path / "kp.txt")
    assert df["kp"].max() == pytest.approx(9.0, abs=0.01)
