---
title: "NLHI Core: a small, reusable library for computing a regional health index"
tags:
  - public health
  - epidemiology
  - Python
authors:
  - name: Mirza Niaz Zaman Elin
    ORCID ID: https://orcid.org/0000-0001-9577-7821
    affiliation: 1
affiliations:
  - name: AMAL Youth & Family Centre, St. John's, NL, Canada
    index: 1
date: 2025-09-05
bibliography: paper.bib
---

# Summary

NLHI Core is a lightweight Python package that computes the Newfoundland & Labrador Health Index (NLHI) from domain‑level inputs. It follows the general principles of composite indicators [@Nardo2005] and draws inspiration from burden-of-disease summaries like DALYs [@MurrayLopez1996] and prevalence-based health expectancy (Sullivan method) [@Sullivan1971] while remaining a regional, pragmatic index. It exposes both a programmatic API and a command‑line interface (CLI), enabling reproducible analyses in notebooks and pipelines. A separate Qt application can provide data entry and dashboards, but this package focuses strictly on the reusable computation and data model—suitable for research reuse and testing.

# Statement of need

Public health and community organizations often collect domain‑specific indicators (e.g., respiratory, cardiovascular) and wish to summarize burden and change over time at a regional level. Analysts need a transparent, *scriptable* tool—rather than a GUI‑only app—to compute a consistent index and integrate it into automated workflows. By shipping as a small Python library that depends on the scientific Python ecosystem [@Harris2020; @McKinney2010], NLHI Core can be embedded into notebooks and pipelines. NLHI Core provides a small, dependency‑light library with tests and examples to meet this need.

# Functionality

Given mean age, population size, and average life expectancy, and a table of domains with TLIPHS values (and units) and domain‑level mortality counts, NLHI Core computes for each domain *d* (conceptually similar to year-equivalent burden components used in DALY-style accounting [@MurrayLopez1996; @Sullivan1971]):

- TLIPHS in years (converting from days/weeks/months),
- **DSTLYA** = TLIPHS(years) + Mortality × (LifeExpectancy − MeanAge),
- **DSAV** (%) = 100 × DSTLYA / (MeanAge × Population),

and reports the NLHI as the average DSAV across domains for a region/date record. A minimal JSON store and helpers allow building time series per region, and a CLI subcommand optionally renders a time‑series PNG (plotting is an optional extra).

# Quality control

The package includes unit tests covering unit conversions, record computation (including edge cases where life expectancy ≤ mean age), and JSON store round‑trip. Continuous integration runs tests on each push/PR. Examples are provided for quick CLI trials.

# State of the field

NLHI Core aims for pragmatic reuse and transparency rather than novel methodology, aligning with best practices in the construction and reporting of composite indicators [@Nardo2005]. It complements broader epidemiological toolkits by packaging a concrete composite‑index computation with a uniform API and CLI.

# Acknowledgements

We thank the maintainers of NumPy and pandas for the scientific Python ecosystem that enables this work.

# Conflict of interest

The author declares no competing interests.
