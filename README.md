# NLHI Core

Reusable **Newfoundland & Labrador Health Index** computation library — a small, importable Python package plus CLI. **No GUI** is bundled (keep any Qt app in a separate repo that depends on this core).

## What it computes
For each domain *d* with inputs TLIPHS, unit, and domain-specific mortality:
- Convert TLIPHS to **years** by the unit factor.
- Compute **DSTLYA** = TLIPHS(years) + Mortality × (LifeExpectancy − MeanAge)
- Compute **DSAV** (%) = 100 × DSTLYA / (MeanAge × Population)
- The **NLHI** is the *average* DSAV across all entered domains.

## Install
```bash
pip install .
# optional for plotting:
pip install ".[plot]"
```

## CLI quickstart
```bash
# 1) Compute NLHI from a domains CSV (columns: name,tliphs,unit,mortality)
nlhi compute --age 32.5 --pop 52000 --le 80.7 examples/domains.csv

# 2) Add a record to a JSON store under a region & date
nlhi add-record --region "Avalon" --date 2025-06-01 --age 32.5 --pop 52000 --le 80.7 examples/domains.csv store.json

# 3) Summarize/plot a region's time series
nlhi summarize --region "Avalon" store.json
nlhi plot --region "Avalon" store.json  # writes PNG (requires matplotlib)
```

## Python API
```python
import pandas as pd
from nlhi import core, io

domains = pd.DataFrame([
    {"name":"Respiratory","tliphs":120,"unit":"Day(s)","mortality":12},
    {"name":"Cardio","tliphs":40,"unit":"Week(s)","mortality":8},
])
record = core.compute_record(age=32.5, population=52000, life_expectancy=80.7, domains_df=domains)
store = io.Store("store.json")
store.upsert("Avalon", "2025-06-01", record)
```

## License
MIT © 2025 Mirza Niaz Zaman Elin
