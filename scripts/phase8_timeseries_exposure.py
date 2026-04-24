"""
Phase 8 — 14-year exposure time series.

For each reporting year (2010-2023):
  - Filter animation_yearly_facilities.csv to that year's CONUS reporters
  - Build 3km + 10km union buffers in EPSG:5070
  - Intersect with 2023 ACS tract populations (frozen reference layer)
  - Area-weighted pop into buffer, de-duplicated via union

Methodological choice: population layer is FROZEN at ACS 2019-2023
(corresponding to the existing cb_2023 tract shapefile on disk).
This isolates the signal to facility entry/exit. Population change
over 14 years in these buffers is <20%; the facility signal dominates.

Output: phase8_timeseries_exposure.csv + .json
"""
import warnings
warnings.filterwarnings('ignore')
import json
import pandas as pd
import geopandas as gpd

GEOWORKS = '/Users/olatunde/CoWorker/Geoworks'
PROC = f'{GEOWORKS}/ghgrp-repo/data/processed'
RAW_CB = f'{GEOWORKS}/data/raw/census_boundaries'
RAW_POP = f'{GEOWORKS}/data/raw/census_population'
OUT_CSV = f'{PROC}/phase8_timeseries_exposure.csv'
OUT_JSON = f'{PROC}/phase8_timeseries_exposure.json'

# ---------- 1. Load the 14-year facility panel ----------
panel = pd.read_csv(f'{PROC}/animation_yearly_facilities.csv')
panel.columns = ['facility_id', 'year', 'category', 'lat', 'lon']
print(f"Panel: {len(panel):,} facility-year rows across "
      f"{panel['year'].nunique()} years, {panel['facility_id'].nunique():,} unique facilities")

# ---------- 2. Load tracts + 2023 ACS population (frozen) ----------
print("Loading tracts + ACS 2019-2023 population (frozen reference)...")
tracts = gpd.read_file(f'{RAW_CB}/cb_2023_us_tract_500k/cb_2023_us_tract_500k.shp')
pop = pd.read_csv(
    f'{RAW_POP}/ACSDT5Y2023.B01003_2026-04-15T155942/ACSDT5Y2023.B01003-Data.csv',
    skiprows=[1],
)
pop['GEOID'] = pop['GEO_ID'].str[-11:]
pop['population'] = pd.to_numeric(pop['B01003_001E'], errors='coerce')
tracts['GEOID_str'] = tracts['GEOID'].astype(str)
tracts = tracts.merge(pop[['GEOID', 'population']], left_on='GEOID_str', right_on='GEOID', how='left')
tracts['population'] = tracts['population'].fillna(0)
tracts_albers = tracts.to_crs('EPSG:5070')
tracts_albers['tract_area_m2'] = tracts_albers.geometry.area
us_total = tracts['population'].sum()
print(f"Tracts: {len(tracts_albers):,}   US pop (tract-sum): {us_total:,.0f}")
sindex = tracts_albers.sindex


def exposure(buffer_geom):
    """Area-weighted tract population inside a union buffer."""
    cand_idx = sindex.query(buffer_geom, predicate='intersects')
    cand = tracts_albers.iloc[cand_idx].copy()
    clipped = cand.geometry.intersection(buffer_geom)
    overlap_m2 = clipped.area
    frac = (overlap_m2 / cand['tract_area_m2']).clip(0, 1)
    return float((cand['population'] * frac).sum())


# ---------- 3. Year-by-year buffer + exposure ----------
rows = []
for year, sub in panel.groupby('year'):
    pts = gpd.GeoDataFrame(
        sub, geometry=gpd.points_from_xy(sub['lon'], sub['lat']), crs='EPSG:4326'
    ).to_crs('EPSG:5070')
    buf_3 = pts.geometry.buffer(3000).union_all()
    buf_10 = pts.geometry.buffer(10000).union_all()
    pop_3 = exposure(buf_3)
    pop_10 = exposure(buf_10)
    area_3 = buf_3.area / 1e6
    area_10 = buf_10.area / 1e6
    rows.append({
        'year': int(year),
        'facilities': len(sub),
        'pop_3km': pop_3,
        'pop_10km': pop_10,
        'buffer_3km_km2': area_3,
        'buffer_10km_km2': area_10,
        'pct_us_pop_10km': 100 * pop_10 / us_total,
    })
    print(f"  {year}: {len(sub):,} facilities   "
          f"3km {pop_3:>11,.0f}   10km {pop_10:>12,.0f}   "
          f"({100 * pop_10 / us_total:.2f}% of US pop)")

df = pd.DataFrame(rows)
df.to_csv(OUT_CSV, index=False)
with open(OUT_JSON, 'w') as f:
    json.dump({
        'method': 'frozen_2023_population',
        'notes': (
            'Population layer = ACS 2019-2023 B01003, tract-level, '
            'applied to every reporting year. Isolates facility entry/exit signal.'
        ),
        'us_total_pop': float(us_total),
        'years': rows,
    }, f, indent=2)
print(f"\nWrote {OUT_CSV} and {OUT_JSON}")
