# GHGRP Ownership Consolidation Analysis

**A reproducible 14-year analysis of ownership concentration in the U.S. EPA Greenhouse Gas Reporting Program (2010-2023)**

Olatunde Salami | [@salamituns](https://x.com/salamituns) | Stratdevs (Tareony)

---

## What This Is

This repository contains the complete analytical pipeline behind a seven-phase investigation of who owns America's industrial emissions infrastructure. Every number, chart, and map in the published analysis can be regenerated from the scripts and data here.

**Key findings:**

- The top 10 parent companies increased their share of GHGRP facilities from 11.7% to 16.7% between 2010 and 2023 (43% relative growth)
- Two companies (Kinder Morgan and Energy Transfer) together hold 415 facilities. 7.7 million Americans live within 10 km of them
- Petroleum refining: 10 parents control 54% of facilities and 80% of emissions, yet the sector's HHI (849) falls below the DOJ threshold for "moderately concentrated"
- Upstream oil and gas is fragmented at the basin level (Permian: 130 operators, top-1 share = 3.2%). Midstream pipeline infrastructure is consolidated. These are different structural pictures
- EPA's September 2025 proposal to remove 46 source categories would terminate the dataset that makes this analysis possible

## Publications

- **Substack long-form:** [The Oligopoly of Pollution](link-to-be-added)
- **SSRN Working Paper:** [Top-N Concentration vs. HHI in US Industrial Emissions Infrastructure](link-to-be-added)
- **Interactive Map:** [Explore all 7,538 geocoded facilities](link-to-be-added)

## Repository Structure

```
scripts/                     # All analysis and rendering scripts
  build_charts.py            # Phase 0: initial bar charts
  render_hero_map.py         # Phase 1: national facility map
  render_corridor_map.py     # Phase 2: Gulf Coast corridor
  render_exposure_map.py     # Phase 3: population exposure buffers
  phase3_analysis.py         # Phase 3: buffer computation
  phase4_og_analysis.py      # Phase 4a: oil & gas concentration
  phase4b_sector_analysis.py # Phase 4b: cross-sector comparison
  phase5_trend_recompute.py  # Phase 5: 14-year trend
  phase6_emissions_weighted.py # Phase 6: emissions-weighted
  phase6b_hhi.py             # Phase 6b: HHI computation
  phase7_basin_analysis.py   # Phase 7: basin-level drill-down

data/
  raw/                       # Source data (not included; see Data Sources)
  processed/                 # Intermediate outputs (JSON, CSV)

viz/                         # All generated figures
  ghgrp_hero_map_2023.png
  ghgrp_corridor_map_2023.png
  ghgrp_exposure_map_2023.png
  ghgrp_sector_concentration_2023.png
  ghgrp_refineries_map_2023.png
  ghgrp_emissions_weighted_2023.png
  ghgrp_basin_ownership_2023.png
  ghgrp_14yr_trend_recomputed.png
  ghgrp_top10_barchart.png
  ghgrp_hero_map_publication.png      # 4K QGIS cartographic output
  ghgrp_corridor_map_publication.png  # 4K QGIS cartographic output
  ghgrp_consolidation_timelapse.mp4   # 14-year animation
  ghgrp_consolidation_timelapse.gif
  ghgrp_interactive_map.html          # Folium interactive map

posts/                       # Substack, SSRN, LinkedIn, X content drafts

methodology/                 # Per-phase methodology notes with self-audit tables
```

## Data Sources

Raw data is not included in this repository due to file size. All source data is publicly available:

1. **EPA GHGRP Parent Company Dataset** (`ghgp_data_parent_company.xlsb`)
   Download from: [EPA Envirofacts GHGRP](https://www.epa.gov/ghgreporting)

2. **EPA GHGRP 2023 Data Summary Spreadsheets** (`ghgp_data_2023.xlsx`)
   Download from: [EPA GHGRP Data Publication](https://www.epa.gov/ghgreporting/data-sets)

3. **U.S. Census Population Estimates**
   - County: `co-est2023-alldata.csv` from [Census PEP](https://www.census.gov/programs-surveys/popest.html)
   - Tract: ACS 5-year Table B01003 from [data.census.gov](https://data.census.gov)

4. **U.S. Census Cartographic Boundary Files**
   - States, counties, tracts from [Census Boundary Files](https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html)

## Methodology

**Concentration metrics:**
- **Any-stake union rule** for facility-count concentration: a facility counts toward a parent if the parent appears in any ownership row
- **Ownership-percentage-weighted allocation** for emissions metrics
- **HHI** (Herfindahl-Hirschman Index) computed on both count and emissions bases

**Spatial analysis:**
- All distance/area calculations in EPSG:5070 (NAD83 Conus Albers Equal Area)
- Area-weighted tract population allocation for buffer exposure estimates

**Validation:**
- Tract population sum: 335.6M (within 0.3% of Census national total)
- County join: 97.2% match rate
- Tract join: 99.8% match rate

See `methodology/` for per-phase self-audit tables documenting the confidence level of every claim.

## Requirements

```
python >= 3.10
pandas
geopandas
matplotlib
shapely
pyxlsb
openpyxl
contextily
folium
```

## License

The analysis code in this repository is released under the MIT License. EPA and Census data are U.S. government works in the public domain.

## Citation

If you use this analysis in your work:

```
Salami, O. (2026). Top-N Concentration vs. HHI in US Industrial Emissions
Infrastructure: A Reproducible 14-Year Analysis of the EPA Greenhouse Gas
Reporting Program. SSRN Working Paper. Available at: [SSRN link]
```

## Contact

Olatunde Salami
- X/Twitter: [@salamituns](https://x.com/salamituns)
- Email: salamituns@gmail.com
- Stratdevs (Tareony)
