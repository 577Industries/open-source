# Reproducibility Guide (`forge-evolve-tdp`)

The commands below re-run the design-study code. They reproduce seeded synthetic draws and constants, not measurements.

```bash
pip install -e .
pytest -v
forge-evolve ingest --step benchmarks/AF_ACP_7740_Bulkhead.stp   # returns the built-in 18-face part whatever the file holds
forge-evolve verify-ia --policy schemas/ia_compliance.rego        # Python booleans; the Rego file is not evaluated
forge-evolve benchmark --suite d2p2-50                            # 50 rows from np.random.default_rng(2026)
```
