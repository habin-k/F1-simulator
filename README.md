# F1-simulator

Lap time and energy simulation with FastF1

## Overview / Goal

Lap time and energy simulation with FastF1: a lap time simulator built from public F1
timing and telemetry data.

## Approach

TODO: pipeline overview (data → track → vehicle → solver → energy → validation → viz).

## Assumptions & Limitations

TODO: list the model assumptions and known limitations.

## Validation

TODO: simulated vs. measured telemetry, error metrics.

## Results

TODO: plots and summary numbers.

## How to Run

TODO: environment setup, then open the notebooks.

Notebooks are in `notebooks/`, numbered to match the write-up series. Each one has an
"Open in Colab" badge at the top.

```bash
pip install -r requirements.txt
pytest
```

## Roadmap

- [x] Data loading and single-lap telemetry export (notebook 02)
- [ ] Track discretization and curvature
- [ ] Forward-backward speed profile
- [ ] Validation against telemetry
- [ ] Energy and state of charge

## Disclaimer

Data is accessed through [FastF1](https://github.com/theOehrly/Fast-F1), which provides
Formula 1 official timing data. This is an unofficial, non-commercial project. It is not
affiliated with or endorsed by Formula 1 or any team. The sample data in `data/sample/` is
one lap of public timing data and is for demonstration only.

## License

MIT. See [LICENSE](LICENSE).
