"""Shared pytest fixtures for helios-connectors tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

FIXTURES_ROOT = Path(__file__).parent / "fixtures" / "donki"
SWPC_FIXTURES_ROOT = Path(__file__).parent / "fixtures" / "swpc"


@pytest.fixture(scope="session")
def swpc_fixtures_root() -> Path:
    """Return the directory holding SWPC fixtures (real + archive)."""
    return SWPC_FIXTURES_ROOT


@pytest.fixture(scope="session")
def swpc_kp_realtime_fixture() -> list[dict[str, object]]:
    """Real SWPC Kp planetary index response (current month snapshot)."""
    return json.loads((SWPC_FIXTURES_ROOT / "kp-realtime.json").read_text())


@pytest.fixture(scope="session")
def swpc_plasma_fixture() -> list[dict[str, object]]:
    """Real SWPC RTSW wind response (newest-first, ~20 min, multi-observatory).

    Captured 2026-08-31 after NOAA retired /products/solar-wind. One active
    (SOLAR1) row has ``proton_density`` nulled by hand so the None-handling
    path stays covered (the live capture had no natural null that day).
    """
    return json.loads((SWPC_FIXTURES_ROOT / "rtsw_wind_1m.json").read_text())


@pytest.fixture(scope="session")
def swpc_mag_fixture() -> list[dict[str, object]]:
    """Real SWPC RTSW mag response (newest-first, ~16 min, multi-observatory)."""
    return json.loads((SWPC_FIXTURES_ROOT / "rtsw_mag_1m.json").read_text())


@pytest.fixture(scope="session")
def swpc_protons_fixture() -> list[dict[str, object]]:
    """Real SWPC GOES integral-protons-7-day response (40 rows)."""
    return json.loads((SWPC_FIXTURES_ROOT / "goes-protons-7-day.json").read_text())


@pytest.fixture(scope="session")
def swpc_sep_forecast_fixture() -> str:
    """Real SWPC 3-day forecast text product."""
    return (SWPC_FIXTURES_ROOT / "sep-forecast.txt").read_text()


@pytest.fixture(scope="session")
def gfz_kp_archive_fixture() -> str:
    """GFZ Potsdam Kp archive slice for May 2024 (31 days).

    Hand edit, 2026-11-16: the sunspot-number column holds the file's missing-data
    value, -1. GFZ's file is CC BY 4.0 except that column, which is CC BY-NC 4.0
    (WDC-SILSO); the adapter does not read it. The file's header says so.
    """
    return (SWPC_FIXTURES_ROOT / "gfz-kp-2024-05.txt").read_text()


@pytest.fixture(scope="session")
def dst_wdc_layout_fixture() -> str:
    """A month of invented hourly values in the layout of a WDC monthly Dst file.

    Not observations. The values are made up (a slow wave, and a straight-line
    dip to -500 at noon on day 11 so that four-character negative fields adjoin), and
    the file says so on its first line. The real May 2024 file was removed:
    the World Data Center for Geomagnetism, Kyoto, does not allow commercial
    applications of its indices.
    """
    return (SWPC_FIXTURES_ROOT / "dst-wdc-layout-synthetic-2405.txt").read_text()


@pytest.fixture(scope="session")
def donki_fixtures_root() -> Path:
    """Return the directory holding DONKI JSON fixtures."""
    return FIXTURES_ROOT


@pytest.fixture(scope="session")
def donki_cme_fixture() -> list[dict[str, object]]:
    """Real DONKI CME response captured during the May 2024 Gannon storm."""
    return json.loads((FIXTURES_ROOT / "CME_sample.json").read_text())


@pytest.fixture(scope="session")
def donki_flr_fixture() -> list[dict[str, object]]:
    """Real DONKI FLR response captured during the May 2024 Gannon storm."""
    return json.loads((FIXTURES_ROOT / "FLR_sample.json").read_text())


@pytest.fixture(scope="session")
def donki_gst_fixture() -> list[dict[str, object]]:
    """Real DONKI GST response captured during the May 2024 Gannon storm.

    Contains the Gannon G5 entry (2024-05-10T15:00:00-GST-001) with
    rich ``linkedEvents`` traceback to 5 originating CMEs plus an IPS.
    """
    return json.loads((FIXTURES_ROOT / "GST_sample.json").read_text())


@pytest.fixture(scope="session")
def donki_sep_fixture() -> list[dict[str, object]]:
    """Real DONKI SEP response captured during the May 2024 Gannon storm."""
    return json.loads((FIXTURES_ROOT / "SEP_sample.json").read_text())


@pytest.fixture(scope="session")
def donki_cme_analysis_fixture() -> list[dict[str, object]]:
    """Real DONKI CMEAnalysis response from the Gannon storm window."""
    return json.loads((FIXTURES_ROOT / "CMEAnalysis_sample.json").read_text())


@pytest.fixture(scope="session")
def donki_ips_fixture() -> list[dict[str, object]]:
    """Real DONKI IPS response from the Gannon storm window."""
    return json.loads((FIXTURES_ROOT / "IPS_sample.json").read_text())


@pytest.fixture(scope="session")
def donki_mpc_fixture() -> list[dict[str, object]]:
    """Real DONKI MPC response from the Gannon storm window."""
    return json.loads((FIXTURES_ROOT / "MPC_sample.json").read_text())


@pytest.fixture(scope="session")
def donki_rbe_fixture() -> list[dict[str, object]]:
    """Real DONKI RBE response from the Gannon storm window."""
    return json.loads((FIXTURES_ROOT / "RBE_sample.json").read_text())


@pytest.fixture(scope="session")
def donki_notifications_fixture() -> list[dict[str, object]]:
    """Real DONKI notifications response from the Gannon storm window."""
    return json.loads((FIXTURES_ROOT / "notifications_sample.json").read_text())
