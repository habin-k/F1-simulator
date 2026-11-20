"""Load FastF1 session data and export single-lap telemetry.

All functions here use only public FastF1 API calls. Network access to the
FastF1 servers is required for ``load_session``; the other functions work on
in-memory data.
"""

from __future__ import annotations

from pathlib import Path

import fastf1
import pandas as pd

# Columns written to the sample CSV. Units:
#   Distance [m], X/Y [1/10 m], Speed [km/h], Throttle [%], Brake [bool], nGear [int]
TELEMETRY_COLUMNS = ["Distance", "X", "Y", "Speed", "Throttle", "Brake", "nGear"]


def configure_cache(cache_dir: str | Path = "cache") -> None:
    """Create the FastF1 cache directory and point FastF1 at it.

    FastF1 3.9 raises if the directory does not exist, so it is created first.
    """
    path = Path(cache_dir)
    path.mkdir(parents=True, exist_ok=True)
    fastf1.Cache.configure(cache_dir=str(path))


def load_session(
    year: int,
    gp: str | int,
    session_kind: str = "Q",
    *,
    cache_dir: str | Path | None = None,
    telemetry: bool = True,
    weather: bool = False,
    messages: bool = False,
) -> fastf1.core.Session:
    """Return a loaded FastF1 session.

    Args:
        year: Season, e.g. 2025.
        gp: Event name (e.g. "Monza") or round number.
        session_kind: FastF1 session identifier, e.g. "Q" (qualifying) or "R" (race).
        cache_dir: Optional cache directory. If None, FastF1's current setting is kept.
        telemetry, weather, messages: Passed to ``Session.load``.
    """
    if cache_dir is not None:
        configure_cache(cache_dir)
    session = fastf1.get_session(year, gp, session_kind)
    session.load(telemetry=telemetry, weather=weather, messages=messages)
    return session


def fastest_lap_telemetry(session: fastf1.core.Session) -> tuple[fastf1.core.Lap, pd.DataFrame]:
    """Return the session's fastest lap and its merged telemetry.

    The telemetry already contains a ``Distance`` column (FastF1 computes it
    for single laps). It is only recalculated if it is missing.

    Raises:
        DataNotLoadedError: if the session's laps were not loaded.
        ValueError: if no fastest lap exists in the session.
    """
    lap = session.laps.pick_fastest()
    if lap is None:
        raise ValueError("No fastest lap found in this session.")
    tel = lap.get_telemetry()
    if "Distance" not in tel.columns:
        tel = tel.add_distance()
    return lap, tel


def sample_filename(gp: str, year: int, session_kind: str, kind: str) -> str:
    """Build a sample CSV name: ``{gp}_{year}_{session}_{kind}.csv``.

    Lowercase, underscores for spaces, no driver name.
    Example: ``sample_filename("Monza", 2025, "Q", "lap_telemetry")``
    returns ``"monza_2025_q_lap_telemetry.csv"``.
    """
    gp_part = gp.strip().lower().replace(" ", "_")
    return f"{gp_part}_{year}_{session_kind.strip().lower()}_{kind}.csv"


def save_lap_csv(tel: pd.DataFrame, path: str | Path) -> int:
    """Write the sample columns of a lap telemetry frame to CSV.

    Returns the number of rows written.
    """
    missing = [c for c in TELEMETRY_COLUMNS if c not in tel.columns]
    if missing:
        raise KeyError(f"Telemetry is missing columns: {missing}")
    out = tel[TELEMETRY_COLUMNS]
    out.to_csv(path, index=False)
    return len(out)
