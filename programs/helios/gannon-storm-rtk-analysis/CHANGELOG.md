# Changelog

All notable changes to this project are documented here, following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Links to the program, the connectors and the review pack lead to their folders in this repository, under `programs/helios/`. They led to the standalone repositories; links to `helios-provenance-spec` are unchanged. `CONTRIBUTING.md` clones this repository, `SECURITY.md` names it in its scope sentence, and the entry for 0.1.0 no longer points to a release page of the standalone repository.

## [0.2.0] — 2026-11-16

### Removed
- **The Dst index.** Version 0.1.0 downloaded the hourly Dst index from the World Data Center for Geomagnetism, Kyoto, kept May 2024 of it as a test fixture, used it as a third term of the positioning model and plotted it in the headline figure. That centre's data service does not allow commercial applications of its indices, and 577 Industries is a commercial entity. The fetcher, its parser, the fixture, the model term (`beta * |Dst| / 100`, `beta = 0.0015`), the curve and every Dst value quoted in this project's documents are gone. Kp is the only index the package reads.

### Changed
- **The model has two inputs:** the station's latitude band and the Kp index. `sigma_2d(t) = sigma_quiet + alpha * f_kp(Kp(t))`. `solve_spp` and `_per_epoch_sigma` take no Dst argument, and no output carries a Dst column.
- **Results regenerated** (`results/quantitative.md` and the four figures). Every station's printed values change, for two reasons that should not be confused:
  - *The random draws are repeatable now.* The table of 0.1.0 came from draws seeded with Python's per-process string hash, so it could not be regenerated; the seed was made stable in the source afterwards, but the table was not rerun. Rerunning with the stable seed moves station values by up to 4.9% (storm-window p95).
  - *The Dst term is gone.* That lowers storm-window p95 by 0.4 to 0.7% and pre-storm p95 by at most 1 mm.
  - The ranges are unchanged in substance: storm-window p95 from 2.30 to 3.00 m (2.30 to 3.01 m in 0.1.0), pre-storm p95 from 2.8 to 3.8 cm (2.9 to 3.8 cm).
- **Headline:** 1,283 station-hours over the 2.5 cm planting threshold during May 10-12, 2024 (1,302 in 0.1.0); peak storm-window 95th-percentile 2D error 3.0 m.
- **Kp credit.** Figures and the results file name the holder, the licence and the citation GFZ asks for (GFZ Helmholtz Centre for Geosciences, CC BY 4.0, Matzka et al., 2021).
- The headline figure's lower panel shows Kp alone, each bar over its own three-hour interval (the bars were centred on the interval's start).
- The headline sentence names its quiet-period figure for what it is, the average of the pre-storm station-day medians (it said "mean 2D error"), and prints it to the millimetre: 0.015 m. At two decimals it rounded to 0.02 m in 0.1.0 and would round to 0.01 m now.
- **The results file prints the count for every day of the window**, quiet days included, and says what its table's columns are (the highest daily 95th percentile in each window). On May 8, 9 and 14, where Kp stays below 4, the model puts 88 station-hours a day over the 2.5 cm threshold, about 15% of the day: the storm-window total of 1,283 includes that share.
- **A station gets the same random draws on every day**, as in 0.1.0, where the Dst term changed from day to day and hid it. Without the term the three quiet days are identical, in the results file and in figures 1 to 3. The methodology and the module's notes now say so.
- **Links.** This project's citation, package metadata, badges, documentation index and blog post point to this repository (`577Industries/open-source`), which holds 0.2.0. The standalone repository of the same name is archived at 0.1.0. The CI and release badges, which reported on that repository, are replaced by a version badge.

### Fixed
- The comment on `ALPHA_KP` stated values for the Kp term (0.25, 1.1 and 1.9 m at Kp 6, 8 and 9) that the coefficient does not produce. It now states what it gives: 0.23, 0.68 and 1.17 m, and a test checks those values against the formula.
- The module notes named two functions that do not exist and said that epochs are taken from the observations in each RINEX file. The one function is `solve_spp`, and the epochs are laid out from the file's sampling interval and day, as `docs/methodology.md` already said.
- The headline figure and the blog post said NOAA issued a G5 watch at 17:23 UT on May 10. NOAA's notices record no such event: the first CME arrived at 16:37 UT, G4 conditions were observed at 17:39 UT and G5 conditions at 22:54 UT. The figure's shaded window starts at the CME's arrival, and its note gives that time and the first G5 observation; the post is corrected.
- Three more statements in the blog post did not match the model's output. Error did not stay below the 2.5 cm threshold throughout May 8-9: the corridor's median did, its 95th percentile did not. The modeled error steps up at 15:00 UT on May 10, where the three-hour Kp interval begins, not around 18:00 UT, and that is the index's resolution, not a sign that error rose before NOAA's notice. And it was last above the quiet level until 06:00 UT on May 13, not late on May 12. 21:00 UT is 4 PM Central, not 5 PM.

### Added
- `docs/methodology.md`: how to read the per-station table. Stations differ only by latitude band and by their random draws.
- Tests: the model's two functions take latitude and Kp and no other input; no module of the package names anything after Dst, and the addresses the package names are held to a list; the same inputs give the same solution in processes with different hash seeds. 42 tests.

Regenerated with Python 3.12, numpy 2.5 and pandas 3.1 from the 175 cached RINEX files and the GFZ Kp archive.

## [0.1.0] — 2026-05-17

### Added
- Reproducible retrospective of the May 10-12, 2024 Gannon G5 superstorm across **25 NGS CORS stations** in the IA/IL/IN/OH corridor.
- 25-station catalog with ITRF2014 truth coordinates derived from real day-131 RINEX headers.
- Fetchers: NGS CORS RINEX (175 real files cached for May 8-14 2024), GFZ Potsdam Kp (CC-BY-4.0), Kyoto WDC Dst.
- v1 positioning model is **climatological/empirical**, transparently disclosed in `docs/methodology.md` and the blog post. v2 will swap in full pseudo-range SPP via `helios-spaceweather-connectors` CDDIS adapter.
- **Headline**: 1,302 station-hours over the 2.5 cm planting threshold; 95th-percentile peak 3.0 m; ~150× quiet-period baseline.
- 40 tests at 80% line+branch coverage; `mypy --strict`, `ruff` clean.
- 1,707-word blog post draft: `blog-post/2026-05-17-when-the-sky-stopped-the-tractors.md`.
- 4 result figures committed (`results/figures/`) + per-station quantitative table (`results/quantitative.md`).
