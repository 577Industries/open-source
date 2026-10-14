# Reproducibility Guide (`forge-evolve-tdp`)

```bash
pip install -e ".[dev]"
pytest -v
forge-evolve ingest --step benchmarks/AF_ACP_7740_Bulkhead.stp
forge-evolve verify-ia --policy schemas/ia_compliance.rego
forge-evolve benchmark --suite d2p2-50
```
