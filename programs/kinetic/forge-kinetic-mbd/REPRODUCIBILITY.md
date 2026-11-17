# Reproducibility Guide (`forge-kinetic-mbd`)

The commands below re-run the design-study code. They reproduce constants and a clamped analytic curve, not measurements.

```bash
pip install -e .
pytest -v
forge-evolve plan-path --dialect FANUC      # text template; tool orientation is hardcoded
forge-evolve benchmark --suite redteam-ccd  # clearance is max(55.04, sinusoid); calibration is a Monte Carlo on assumed noise
```
