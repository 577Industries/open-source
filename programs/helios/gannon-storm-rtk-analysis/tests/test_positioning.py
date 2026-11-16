"""Tests for the climatological positioning model."""

from __future__ import annotations

import inspect
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from gannon_analysis.positioning import (
    ALPHA_KP,
    GEOMAG_LATITUDE_FACTOR,
    PRECISION_AG_PLANTING_THRESHOLD_M,
    SIGMA_QUIET_M,
    _kp_severity_function,
    _per_epoch_sigma,
    daily_p95_error,
    manifest_for_solution,
    solve_spp,
    threshold_crossings,
)
from gannon_analysis.stations import station_by_id
from gannon_analysis.swpc import fetch_kp, join_kp_to_minute_grid


def test_kp_severity_function_zero_below_4() -> None:
    out = _kp_severity_function(np.array([0.0, 2.0, 3.9]))
    assert np.all(out == 0.0)


def test_kp_severity_function_monotonic_above_4() -> None:
    grid = np.linspace(4.0, 9.0, 50)
    out = _kp_severity_function(grid)
    assert np.all(np.diff(out) >= 0)
    assert out[0] == pytest.approx(1.0)


def test_per_epoch_sigma_baseline_quiet() -> None:
    sigma = _per_epoch_sigma(
        kp=np.array([0.0, 1.0, 2.0]),
        geomag_lat_deg=39.0,
    )
    assert np.allclose(sigma, SIGMA_QUIET_M)


def test_per_epoch_sigma_storm_amplification() -> None:
    quiet = _per_epoch_sigma(kp=np.array([1.0]), geomag_lat_deg=39.0)
    storm = _per_epoch_sigma(kp=np.array([9.0]), geomag_lat_deg=39.0)
    assert storm[0] > 50 * quiet[0]


def test_per_epoch_sigma_is_the_documented_formula() -> None:
    """sigma = sigma_quiet + alpha * exp(0.55 * (Kp - 4)) from Kp 4 up, and nothing else."""
    sigma = _per_epoch_sigma(kp=np.array([3.9, 4.0, 6.0, 8.0, 9.0]), geomag_lat_deg=39.0)
    expected = SIGMA_QUIET_M + ALPHA_KP * np.array(
        [0.0, 1.0, np.exp(1.1), np.exp(2.2), np.exp(2.75)]
    )
    assert np.allclose(sigma, expected)
    # The values the ALPHA_KP comment states.
    assert ALPHA_KP * np.exp(1.1) == pytest.approx(0.23, abs=0.005)
    assert ALPHA_KP * np.exp(2.2) == pytest.approx(0.68, abs=0.005)
    assert ALPHA_KP * np.exp(2.75) == pytest.approx(1.17, abs=0.005)


def test_the_model_takes_two_inputs_and_no_other() -> None:
    """A station's latitude and Kp. A further input, under any name, changes a signature here.

    Dst was a third input until 0.2.0: its source does not allow commercial applications.
    """
    assert set(inspect.signature(_per_epoch_sigma).parameters) == {"kp", "geomag_lat_deg"}
    assert set(inspect.signature(solve_spp).parameters) == {
        "rinex_path",
        "station",
        "kp_series",
        "rng_seed",
    }


def test_per_epoch_sigma_high_latitude_boost() -> None:
    low = _per_epoch_sigma(kp=np.array([8.0]), geomag_lat_deg=39.0)
    high = _per_epoch_sigma(kp=np.array([8.0]), geomag_lat_deg=44.0)
    assert high[0] == pytest.approx(low[0] * GEOMAG_LATITUDE_FACTOR, rel=1e-3)


def test_solve_spp_returns_expected_columns(
    rinex_fixture: Path,
    kp_fixture: Path,
    tmp_path: Path,
) -> None:
    cache_kp = tmp_path / "kp.txt"
    cache_kp.write_text(kp_fixture.read_text())
    kp = fetch_kp(cache_path=cache_kp)
    kp_minute = join_kp_to_minute_grid(kp)

    station = station_by_id("iaal")
    df = solve_spp(rinex_fixture, station, kp_series=kp_minute)
    assert set(df.columns) >= {"station_id", "h_error_2d_m", "hdop", "kp"}
    assert not {column for column in df.columns if "dst" in column.lower()}
    assert df["station_id"].nunique() == 1
    assert (df["h_error_2d_m"] >= 0).all()


def test_solve_spp_draws_do_not_depend_on_the_process(
    rinex_fixture: Path,
    kp_fixture: Path,
) -> None:
    """The same inputs give the same solution in every process.

    Version 0.1.0 offset the seed by ``hash(station_id)``, which Python salts per process, so
    its published table could not be regenerated. The draws are keyed on a SHA-256 of the
    station id instead; two interpreters with different hash seeds must agree.
    """
    script = (
        "import hashlib, sys\n"
        "from pathlib import Path\n"
        "from gannon_analysis.positioning import solve_spp\n"
        "from gannon_analysis.stations import station_by_id\n"
        "from gannon_analysis.swpc import fetch_kp, join_kp_to_minute_grid\n"
        "kp = join_kp_to_minute_grid(fetch_kp(cache_path=Path(sys.argv[2])))\n"
        "df = solve_spp(Path(sys.argv[1]), station_by_id('iaal'), kp_series=kp)\n"
        "print(hashlib.sha256(df['h_error_2d_m'].to_numpy().tobytes()).hexdigest())\n"
    )
    digests = set()
    for hash_seed in ("1", "2", "random"):
        result = subprocess.run(
            [sys.executable, "-c", script, str(rinex_fixture), str(kp_fixture)],
            capture_output=True,
            text=True,
            check=True,
            env={**os.environ, "PYTHONHASHSEED": hash_seed},
        )
        digests.add(result.stdout.strip())
    assert len(digests) == 1


def test_solve_spp_storm_window_exceeds_quiet(
    rinex_fixture: Path,
    kp_fixture: Path,
    tmp_path: Path,
) -> None:
    cache_kp = tmp_path / "kp.txt"
    cache_kp.write_text(kp_fixture.read_text())
    kp = fetch_kp(cache_path=cache_kp)
    kp_minute = join_kp_to_minute_grid(kp)

    station = station_by_id("iaal")
    df = solve_spp(rinex_fixture, station, kp_series=kp_minute)
    # Storm peak is May 11; pre-storm baseline May 10 early-UTC.
    storm = df.loc[
        (df.index >= pd.Timestamp("2024-05-10 18:00"))
        & (df.index <= pd.Timestamp("2024-05-10 23:59"))
    ]
    # Compare against the early-UTC of May 10 (Kp still low).
    quiet = df.loc[
        (df.index >= pd.Timestamp("2024-05-10 00:00"))
        & (df.index <= pd.Timestamp("2024-05-10 05:59"))
    ]
    assert storm["h_error_2d_m"].mean() > 10 * quiet["h_error_2d_m"].mean()


def test_daily_p95_error_one_row_per_day_per_station() -> None:
    times = pd.date_range("2024-05-10", periods=2880, freq="30s")
    df = pd.DataFrame(
        {
            "h_error_2d_m": np.linspace(0.005, 2.5, 2880),
            "station_id": "iaal",
            "kp": np.linspace(2, 9, 2880),
        },
        index=times,
    )
    df.index.name = "time_utc"
    out = daily_p95_error(df)
    assert len(out) == 1
    assert out["h_error_2d_p95_m"].iloc[0] > 1.5


def test_threshold_crossings_sums_correctly() -> None:
    # 2880 epochs at 30 s each = 24 hours. Half over threshold.
    times = pd.date_range("2024-05-11", periods=2880, freq="30s")
    err = np.concatenate(
        [np.full(1440, 0.10), np.full(1440, 0.01)]
    )  # first half over, second under
    df = pd.DataFrame(
        {
            "h_error_2d_m": err,
            "station_id": "iaal",
            "kp": np.full(2880, 6.0),
        },
        index=times,
    )
    df.index.name = "time_utc"
    cr = threshold_crossings(df, threshold_m=PRECISION_AG_PLANTING_THRESHOLD_M)
    assert len(cr) == 1
    # 1440 epochs * 30 s = 43200 s = 12 hours
    assert cr["hours_over_threshold"].iloc[0] == pytest.approx(12.0, abs=0.1)


def test_manifest_for_solution_round_trip() -> None:
    station = station_by_id("iaal")
    df = pd.DataFrame({"h_error_2d_m": [0.0]})
    m = manifest_for_solution(Path("/tmp/x.gz"), station, df)
    assert m.station_id == "iaal"
    assert m.observation_count == 1
    assert m.model == "climatological_v1"


def test_threshold_crossings_empty_df() -> None:
    empty = pd.DataFrame(columns=["h_error_2d_m", "station_id", "kp"])
    empty.index.name = "time_utc"
    cr = threshold_crossings(empty)
    assert "hours_over_threshold" in cr.columns


def test_model_constants_positive() -> None:
    assert ALPHA_KP > 0
    assert SIGMA_QUIET_M > 0
