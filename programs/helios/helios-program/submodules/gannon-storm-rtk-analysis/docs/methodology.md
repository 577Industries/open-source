# Methodology

This document explains what the v1 model of `gannon-storm-rtk-analysis`
actually computes, what it does **not** compute, and what v2 will add. It
describes version 0.2.0; what changed from 0.1.0 is at the end.

## What is SPP?

Single Point Positioning (SPP) is the GPS solution available to any receiver
with no augmentation. The receiver observes pseudo-ranges to four or more GPS
satellites and solves a system of four equations (three position coordinates
plus receiver-clock bias). Quiet-time 2D horizontal accuracy is typically
**1-3 m** for an L1-only receiver after Klobuchar ionospheric correction.

## What is RTK?

Real-Time Kinematic positioning fuses carrier-phase observations from a rover
receiver against simultaneous observations from a fixed base station (or a
network of base stations). When the carrier-phase integer ambiguities are
correctly resolved ("fixed"), 2D horizontal accuracy reaches **1-2 cm** —
the regime precision agriculture depends on for row spacing, planter offsets,
and spray boom positioning. The Gannon storm story is about the breakdown of
ambiguity resolution at the precise hours during the May 2024 planting season
when operators most needed centimetre accuracy.

## What this release computes

For each NGS CORS station in the corridor, the v1 pipeline:

1. **Fetches the published daily RINEX observation file** from the NGS public
   archive (`https://geodesy.noaa.gov/corsdata/rinex/`). This is real, audit-
   able I/O — the manifest of fetched files is provenance for every result.
2. **Parses the RINEX header** with `georinex` to recover the station's
   published ITRF2014 truth coordinates and the per-day observation epoch grid.
3. **Computes per-epoch 2D horizontal error** using a *climatological model*
   tied to the contemporaneous Kp index (the real series, from GFZ):

   ```
   sigma_2d(t) = sigma_quiet + alpha * f_kp(Kp(t))

   f_kp(Kp) = 0                       if Kp <  4
            = exp(0.55 * (Kp - 4))     if Kp >= 4
   ```

   `sigma_2d` is multiplied by 1.25 for stations at or above 42 deg N. The
   error at each epoch is then drawn at random: two independent normal
   components with that standard deviation, combined into a 2D magnitude.

   Constants `sigma_quiet` and `alpha` are calibrated against (a)
   OEM-published RTK accuracy specifications (~2 cm baseline) and (b)
   field-reported error excursions during the May 2024 Gannon storm
   (30 cm to multi-metre during peak hours).

4. **Aggregates per-station daily 95th-percentile error** and counts
   "station-hours over threshold" — the citable summary statistic.

5. **Renders four figures** with `data + method + timestamp` footer:
   - Regional median + p95 error vs time, above the Kp index (headline).
   - Per-station error grid (one panel per station, Kp-coloured points).
   - Stacked station-hours bar chart by UTC date.
   - Station map showing peak severity by location.

## What this release does **not** compute

- It does **not** linearise pseudo-range observables from the RINEX file.
  The RINEX file is consumed for its header (truth + epoch grid + metadata)
  and as evidence-of-fetch in the manifest.
- It does **not** perform PPP, RTK ambiguity resolution, or any carrier-phase
  processing.
- It does **not** use real satellite ephemerides. (.sp3 SP3 files from CDDIS
  are out of scope for v1.)
- It does **not** apply equipment-specific transfer functions. The error
  series produced is a corridor-average climatological response, not a per-
  receiver-family prediction.

## Why v1 is climatological

A full PPP/RTK pipeline is roughly an additional 1500 lines of Python plus
~3-5 GB of ancillary data (precise orbits, clock products, antenna
phase-centre files). It changes the per-station error trajectory but does
**not** change the qualitative regional story the artifact wants to tell:
that the May 10-12, 2024 storm drove 2D RTK error across the IA/IL/IN/OH
corridor up by 1-2 orders of magnitude for an aggregate of about 1,280
station-hours.

For a customer-discovery artifact and a public-facing blog
post, the climatological model is honest, reproducible, and traceable to
the real Kp time series that anyone can verify against GFZ.

## How to read the per-station table

The model knows two things about a station: whether it lies at or above
42 deg N, and which random draws it was given. Kp is the same for every
station at every epoch. So two stations on the same side of 42 deg N have the
same distribution of error, and the differences between their rows in
`results/quantitative.md` (2.30 to 2.43 m below the line, 2.90 to 3.00 m at or
above it, storm-window p95) are the spread of 2,880 random draws. The table is
not a ranking of stations, and the station with the highest value is not a
station that fared worst.

The table's two columns are, for each station, the highest daily 95th
percentile of the modeled error within the window.

The draws are seeded per station from a key that is the same on every run, so
`make analyze` regenerates the table from the same inputs. A station is given
the same sequence of draws on every day, two for each of the day's 2,880
epochs. Days with the same Kp therefore give the
same errors: May 8, 9 and 14, where Kp stays below 4, are identical for each
station, and each shows 88 station-hours over the 2.5 cm threshold across the
25 stations, about 15% of the day. That share is the quiet-period draws alone,
and the storm-window total of 1,283 station-hours includes it.

## What v2 will add

- **Real SPP from RINEX observables.** Pseudo-range linearisation,
  satellite-position solution from SP3 ephemerides, ionosphere-free L1/L2
  combination, weighted least-squares with elevation-mask outlier rejection.
- **PPP refinement** using IGS final precise orbits and clock products
  (CDDIS Earthdata download via Artifact B's connector library).
- **RTK simulation** by computing double-differenced carrier-phase
  observations between station pairs and recovering integer ambiguities,
  with explicit tracking of "fix vs float vs single-point" status per epoch.
- **Equipment-specific transfer functions** for the John Deere StarFire
  6000/7000, Trimble RTK, and AgLeader Surefire/Versa families, calibrated
  against documented receiver behaviour during the May 2024 storm. This
  artifact prepares the data infrastructure that a later training pipeline
  for those transfer functions will consume.

## References

- GFZ Kp index (GFZ Helmholtz Centre for Geosciences, CC BY 4.0). Matzka, J.,
  Stolle, C., Yamazaki, Y., Bronkalla, O. and Morschhauser, A. (2021). *The
  geomagnetic Kp index and derived indices of geomagnetic activity.* Space
  Weather 19. https://doi.org/10.1029/2020SW002641. Data publication:
  https://doi.org/10.5880/Kp.0001
- NGS CORS. National Geodetic Survey Continuously Operating Reference
  Stations. https://geodesy.noaa.gov/CORS/
- American Farm Bureau Federation (2024). *Precision Agriculture Technology
  Survey Results.*
- OSU Extension (2024). *Space Weather Disturbances and Farm GPS Interruptions.*

## What changed in 0.2.0

- **No Dst index.** Version 0.1.0 added a third term to the model,
  `beta * |Dst(t)| / 100` with `beta = 0.0015`, driven by the hourly Dst index
  of the World Data Center for Geomagnetism, Kyoto, and plotted that index
  under the headline figure. That centre's data service does not allow
  commercial applications of its indices, and 577 Industries is a commercial
  entity. The index is no longer downloaded, stored, plotted or used. The term
  was about 6 mm at the storm's minimum, against a Kp term above 1 m; removing
  it lowers storm-window p95 by 0.4 to 0.7%. With the term gone, the quiet
  days of the window come out identical (see the section above): the term had
  varied from day to day.
- **Repeatable draws.** The table of 0.1.0 came from draws seeded with
  Python's per-process string hash and could not be regenerated. The seed is
  stable now, and the table was rerun. That moves individual station values by
  up to 4.9% and leaves the ranges where they were. See `CHANGELOG.md`.
