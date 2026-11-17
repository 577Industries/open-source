# Reproducibility Guide

All kinematic, swept-capsule collision avoidance, and URTS post-processor tests execute deterministically offline:

```bash
python3 -m pytest -v
forge-kinetic envelope
forge-kinetic ik-solve
forge-kinetic swept-ccd
forge-kinetic urts-compile --dialect FANUC
```
