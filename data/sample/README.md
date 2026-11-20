# Sample data

## File

| File | Description |
|------|-------------|
| `monza_2025_q_lap_telemetry.csv` | Telemetry of one lap: the fastest lap of Monza 2025 Qualifying |

Status: **not generated yet.** The values below are filled in only after notebook 02 runs
successfully against the FastF1 servers.

## Session

- Season: 2025
- Event: Monza (Italian Grand Prix)
- Session: Q (Qualifying)
- Driver: TBD
- Lap time: TBD

## Columns

| Column | Unit | Type | Description |
|--------|------|------|-------------|
| `Distance` | m | float | Distance from the first sample of the lap |
| `X` | 1/10 m | float | Track position, X |
| `Y` | 1/10 m | float | Track position, Y |
| `Speed` | km/h | float | Car speed |
| `Throttle` | % | float | Throttle pedal position (0–100) |
| `Brake` | bool | bool | Brake applied |
| `nGear` | – | int | Gear number |

No index column. Rows are in time order. Values are the output of FastF1 telemetry
merging for a single lap and are not resampled.

## How it was generated

- Notebook: `notebooks/02_telemetry_track_map.ipynb`
- Cell: section 6 ("Save the lap for the next notebooks"), which calls `save_lap_csv` from `src/f1sim/data.py`
- FastF1 version: 3.9.2

## Source

Data comes from [FastF1](https://github.com/theOehrly/Fast-F1), which provides Formula 1
official timing data. This is an unofficial project. See the Disclaimer in the top-level README.
