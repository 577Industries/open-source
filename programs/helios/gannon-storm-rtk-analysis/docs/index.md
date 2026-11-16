# gannon-storm-rtk-analysis

A reproducible analysis of how RTK-GNSS positioning error evolved across the
Iowa / Illinois / Indiana / Ohio corridor during the May 10-12, 2024 Gannon
G5 superstorm. The artifact is one of four in the HELIOS program (577
Industries' data-driven space weather research-to-operations-to-research
work); it converts the Gannon case study from a story into a citable
result with code, data manifests, and figures any operator can examine.

## Headline

> Across 25 of 25 NGS CORS stations spanning the IA, IL, IN, OH corridor,
> the v1 climatological model produced 2D horizontal SPP error exceeding
> the agronomic 2.5 cm threshold for an aggregate of 1,283 station-hours
> during May 10-12, 2024 (peak Kp=9.0).

(See [`results/quantitative.md`](https://github.com/577Industries/open-source/blob/main/programs/helios/gannon-storm-rtk-analysis/results/quantitative.md) for the per-station breakdown on GitHub.)

## What's in here

- [`stations.py`](https://github.com/577Industries/open-source/blob/main/programs/helios/gannon-storm-rtk-analysis/src/gannon_analysis/stations.py) — 25-station catalog, truth coordinates from each station's day-131 RINEX header.
- [`fetch.py`](https://github.com/577Industries/open-source/blob/main/programs/helios/gannon-storm-rtk-analysis/src/gannon_analysis/fetch.py) — polite NGS CORS RINEX downloader with on-disk caching.
- [`swpc.py`](https://github.com/577Industries/open-source/blob/main/programs/helios/gannon-storm-rtk-analysis/src/gannon_analysis/swpc.py) — GFZ Kp archive fetcher.
- [`positioning.py`](https://github.com/577Industries/open-source/blob/main/programs/helios/gannon-storm-rtk-analysis/src/gannon_analysis/positioning.py) — v1 climatological 2D-error model. See [methodology](methodology.md).
- [`analysis.py`](https://github.com/577Industries/open-source/blob/main/programs/helios/gannon-storm-rtk-analysis/src/gannon_analysis/analysis.py) — orchestrator that ties fetch + the Kp index + positioning + aggregates into one pipeline.
- [`plotting.py`](https://github.com/577Industries/open-source/blob/main/programs/helios/gannon-storm-rtk-analysis/src/gannon_analysis/plotting.py) — four figures with data/method/timestamp footers.
- Three Jupyter notebooks for interactive exploration ([`notebooks/`](https://github.com/577Industries/open-source/tree/main/programs/helios/gannon-storm-rtk-analysis/notebooks)).
- A blog post draft of about 1,700 words under [`blog-post/`](https://github.com/577Industries/open-source/tree/main/programs/helios/gannon-storm-rtk-analysis/blog-post).
- Tests with >70% coverage; v1 ships at ~80%.

## Reproducibility

```bash
make all       # fetch + analyze + plot, end-to-end
make fetch     # cache RINEX + the Kp index only
make analyze   # aggregate without re-fetching
make test      # pytest + coverage
```

Cold-cache full run: ~5-10 min on a typical broadband connection.
Warm-cache run: <30 s.

## Status

v0.2.0. Pre-stable. Since 0.2.0 the Dst index is not used (see the
[methodology](methodology.md)), and the results are regenerated with random
draws that are the same on every run. RTK-style equipment transfer functions
and full PPP/RTK refinement are scheduled for v2 once the HELIOS fusion
engine (`helios-fusion-engine`) ships its companion training infrastructure.
