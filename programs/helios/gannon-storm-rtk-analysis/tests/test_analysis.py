"""End-to-end tests for the analysis orchestrator and plotting.

These do not hit the network: they pre-seed the on-disk cache from the
committed fixtures before invoking ``run_analysis``.
"""

from __future__ import annotations

import shutil
from datetime import date
from pathlib import Path

import pytest

from gannon_analysis.analysis import (
    HeadlineClaim,
    run_analysis,
    utc_window_summary,
    write_quantitative_md,
)
from gannon_analysis.fetch import local_cache_path
from gannon_analysis.stations import station_by_id


def _seed_cache_for_iaal_one_day(data_dir: Path, rinex_fixture: Path, kp_fixture: Path) -> None:
    # RINEX: seed all 7 days using the same fixture file (model is what's tested,
    # not RINEX content). Filenames must follow the canonical pattern for the
    # date so the SPP code reads the date from the name.
    for d in (
        date(2024, 5, 8),
        date(2024, 5, 9),
        date(2024, 5, 10),
        date(2024, 5, 11),
        date(2024, 5, 12),
        date(2024, 5, 13),
        date(2024, 5, 14),
    ):
        target = local_cache_path("iaal", d, data_dir)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(rinex_fixture, target)
    swpc = data_dir / "swpc"
    swpc.mkdir(parents=True, exist_ok=True)
    shutil.copy(kp_fixture, swpc / "kp.txt")


def test_run_analysis_end_to_end(
    tmp_path: Path,
    rinex_fixture: Path,
    kp_fixture: Path,
) -> None:
    _seed_cache_for_iaal_one_day(tmp_path, rinex_fixture, kp_fixture)
    bundle = run_analysis([station_by_id("iaal")], data_dir=tmp_path)
    assert "solutions" in bundle
    assert "headline" in bundle
    assert isinstance(bundle["headline"], HeadlineClaim)
    h = bundle["headline"]
    assert h.peak_kp == pytest.approx(9.0, abs=0.01)
    assert h.n_stations == 1
    assert h.aggregate_hours_over_threshold > 0
    # Kp is the only index in the bundle, its frames and its sentence.
    assert "dst" not in bundle
    assert not {c for c in bundle["solutions"].columns if "dst" in c.lower()}
    assert not {c for c in bundle["daily"].columns if "dst" in c.lower()}
    assert "dst" not in h.sentence().lower()
    # The run reads nothing from the cache but the RINEX files and the Kp archive.
    assert sorted(p.name for p in (tmp_path / "swpc").iterdir()) == ["kp.txt"]


def test_quantitative_md_writes(
    tmp_path: Path,
    rinex_fixture: Path,
    kp_fixture: Path,
) -> None:
    _seed_cache_for_iaal_one_day(tmp_path, rinex_fixture, kp_fixture)
    bundle = run_analysis([station_by_id("iaal")], data_dir=tmp_path)
    out = tmp_path / "results" / "quantitative.md"
    write_quantitative_md(bundle, out)
    text = out.read_text()
    assert "Headline" in text
    assert "iaal" in text.lower()
    assert "CC BY 4.0" in text and "10.1029/2020SW002641" in text
    assert "dst" not in text.lower() and "kyoto" not in text.lower()
    # The count behind the headline is printed for every day of the run, quiet days included.
    assert "## Station-hours over the threshold, by day" in text
    assert "| 2024-05-11 | 9.0 |" in text
    # The figure before the semicolon is named for what it is: an average of station-day medians.
    assert "median 2D error of a station-day averaged" in text
    assert "mean 2D error" not in text


def test_utc_window_summary(
    tmp_path: Path,
    rinex_fixture: Path,
    kp_fixture: Path,
) -> None:
    _seed_cache_for_iaal_one_day(tmp_path, rinex_fixture, kp_fixture)
    bundle = run_analysis([station_by_id("iaal")], data_dir=tmp_path)
    summary = utc_window_summary(bundle)
    assert "kp_max" in summary.columns
    # 7 days in window
    assert len(summary) == 7


def test_plotting_renders_without_error(
    tmp_path: Path,
    rinex_fixture: Path,
    kp_fixture: Path,
) -> None:
    from gannon_analysis.plotting import (
        plot_per_station_error_grid,
        plot_regional_error_vs_time,
        plot_threshold_crossings_bars,
    )

    _seed_cache_for_iaal_one_day(tmp_path, rinex_fixture, kp_fixture)
    bundle = run_analysis([station_by_id("iaal")], data_dir=tmp_path)
    out = tmp_path / "fig"
    plot_regional_error_vs_time(bundle, out_path=out / "fig01.png")
    plot_per_station_error_grid(bundle, out_path=out / "fig02.png")
    plot_threshold_crossings_bars(bundle, out_path=out / "fig03.png")
    assert (out / "fig01.png").stat().st_size > 1000
    assert (out / "fig02.png").stat().st_size > 1000
    assert (out / "fig03.png").stat().st_size > 1000
