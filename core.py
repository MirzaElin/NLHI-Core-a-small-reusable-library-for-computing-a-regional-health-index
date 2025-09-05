from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List
import pandas as pd
from .units import UNIT_CONVERSION

def safe_float(x, default=None):
    try:
        return float(str(x).strip())
    except Exception:
        return default

@dataclass
class DomainInput:
    name: str
    tliphs: float
    unit: str
    mortality: float

@dataclass
class DomainResult:
    name: str
    tliphs_years: float
    dstlya: float
    dsav: float

def _tliphs_to_years(value: float, unit: str) -> float:
    return value * UNIT_CONVERSION.get(unit, 1.0)

def compute_domain(mean_age: float, population: float, life_expectancy: float, d: DomainInput) -> DomainResult:
    t_years = _tliphs_to_years(d.tliphs, d.unit)
    dstlya = t_years + (d.mortality * (life_expectancy - mean_age))
    denom = mean_age * population
    dsav = (dstlya * 100.0) / denom if denom != 0 else 0.0
    return DomainResult(name=d.name, tliphs_years=t_years, dstlya=dstlya, dsav=dsav)

def compute_record(age: float, population: float, life_expectancy: float, domains_df: pd.DataFrame) -> Dict:
    if any(x is None or x <= 0 for x in [age, population, life_expectancy]):
        raise ValueError("age, population, and life_expectancy must be positive numbers.")
    domains: List[DomainResult] = []
    for _, row in domains_df.iterrows():
        name = str(row.get("name","")).strip()
        if not name:
            continue
        di = DomainInput(
            name=name,
            tliphs=safe_float(row.get("tliphs"), 0.0),
            unit=str(row.get("unit","Year(s)")),
            mortality=safe_float(row.get("mortality"), 0.0),
        )
        domains.append(compute_domain(age, population, life_expectancy, di))
    if not domains:
        raise ValueError("At least one valid domain row is required.")
    nlhi = sum(d.dsav for d in domains) / float(len(domains))
    return {
        "MeanAge": age,
        "Population": population,
        "AvgLifeExpectancy": life_expectancy,
        "domains": [
            {"name": d.name, "TLIPHS_years": d.tliphs_years, "DSTLYA": d.dstlya, "DSAV": d.dsav}
            for d in domains
        ],
        "NLHI": nlhi,
    }
