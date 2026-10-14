# Reproducibility Guide (`forge-kinetic-mbd`)

```bash
pip install -e ".[dev]"
pytest -v
forge-evolve plan-path --dialect FANUC
forge-evolve benchmark --suite redteam-ccd
```
