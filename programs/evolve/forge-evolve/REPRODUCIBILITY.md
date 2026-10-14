# Reproducibility Guide

All stages of `forge-evolve` execute deterministically offline with zero external API keys:

```bash
python3 -m pytest -v
forge-evolve discover
forge-evolve clar-lift
forge-evolve compare
forge-evolve audit
```
