"""Tests for f1sim.data.

Offline tests use small in-memory frames and stubs. They do not touch the
network. Checks on the sample CSV run only when the file exists.
"""

from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest

from f1sim.data import (
    TELEMETRY_COLUMNS,
    fastest_lap_telemetry,
    sample_filename,
    save_lap_csv,
)

SAMPLE_CSV = Path(__file__).resolve().parents[1] / "data" / "sample" / "monza_2025_q_lap_telemetry.csv"


def _fake_telemetry(n: int = 5) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Date": range(n),
            "Distance": [float(i * 10) for i in range(n)],
            "X": [float(i) for i in range(n)],
            "Y": [float(i) for i in range(n)],
            "Speed": [100.0 + i for i in range(n)],
            "Throttle": [50.0] * n,
            "Brake": [False, True, False, False, True],
            "nGear": [5] * n,
            "RPM": [11000.0] * n,
        }
    )


def test_sample_filename_follows_naming_rule():
    assert sample_filename("Monza", 2025, "Q", "lap_telemetry") == "monza_2025_q_lap_telemetry.csv"
    assert sample_filename("Las Vegas", 2025, "R", "tyre_laps") == "las_vegas_2025_r_tyre_laps.csv"


def test_save_lap_csv_writes_only_sample_columns(tmp_path):
    out = tmp_path / "lap.csv"
    rows = save_lap_csv(_fake_telemetry(), out)
    written = pd.read_csv(out)
    assert rows == 5
    assert list(written.columns) == TELEMETRY_COLUMNS


def test_save_lap_csv_rejects_missing_columns(tmp_path):
    tel = _fake_telemetry().drop(columns=["Speed"])
    with pytest.raises(KeyError, match="Speed"):
        save_lap_csv(tel, tmp_path / "lap.csv")


class _StubLap:
    def __init__(self, tel):
        self._tel = tel

    def get_telemetry(self):
        return self._tel


class _StubSession:
    def __init__(self, lap):
        self.laps = SimpleNamespace(pick_fastest=lambda: lap)


def test_fastest_lap_telemetry_keeps_existing_distance():
    tel = _fake_telemetry()
    lap, out = fastest_lap_telemetry(_StubSession(_StubLap(tel)))
    assert out is tel
    assert out["Distance"].tolist() == tel["Distance"].tolist()


def test_fastest_lap_telemetry_raises_without_fastest_lap():
    with pytest.raises(ValueError):
        fastest_lap_telemetry(_StubSession(None))


@pytest.mark.skipif(not SAMPLE_CSV.exists(), reason="sample CSV not generated yet (run notebook 02)")
class TestSampleCsv:
    @pytest.fixture(scope="class")
    def df(self):
        return pd.read_csv(SAMPLE_CSV)

    def test_required_columns_present(self, df):
        assert set(TELEMETRY_COLUMNS) <= set(df.columns)

    def test_no_missing_values(self, df):
        assert not df[TELEMETRY_COLUMNS].isna().any().any()

    def test_distance_is_non_decreasing(self, df):
        assert (df["Distance"].diff().dropna() >= 0).all()

    def test_speed_within_physical_range(self, df):
        assert df["Speed"].between(0, 400).all()
