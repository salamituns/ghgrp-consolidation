"""
Phase 3 — Population exposure within 3km and 10km of KM + ET facilities.
National scope. Uses area-weighted tract-level population allocation.
"""
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from pyxlsb import open_workbook

GEOWORKS = '/sessions/wonderful-amazing-volta/mnt/CoWorker/Geoworks'
RAW_EPA  = f'{GEOWORKS}/data/raw/epa_ghgrp'
RAW_CB   = f'{GEOWORKS}/data/raw/census_boundaries'
RAW_POP  = f'{GEOWORKS}/data/raw/census_population'
PROC     = f'{GEOWORKS}/data/processed'
OUT_DIR  = PROC  # write outputs to processed/

# ---------- 1. Load KM+ET facility coordinates ----------
geo = pd.read_csv(f'{PROC}/ghgrp_2023_geo.csv')
geo = geo[geo['Latitude'].notna() & geo['Longitude'].notna()].copy()
geo['Facility Id'] = geo['Facility Id'].astype(int)

with open_workbook(f'{RAW_EPA}/ghgp_data_parent_company.xlsb') as wb:
    with wb.get_sheet('2023') as sheet:
        rows = list(sheet.rows())
        headers = [c.v for c in rows[0]]
        data = [[c.v for c in r] for r in rows[1:]]
raw = pd.DataFrame(data, columns=headers)
km_set = set(raw[raw['PARENT COMPANY NAME']=='KINDER MORGAN INC']['GHGRP FACILITY ID'].astype(int))
et_set = set(raw[raw['PARENT COMPANY NAME']=='ENERGY TRANSFER LP']['GHGRP FACILITY ID'].astype(int))

km_geo = geo[geo['Facility Id'].isin(km_set)].copy()
et_geo = geo[geo['Facility Id'].isin(et_set)].copy()
both_geo = geo[geo['Facility Id'].isin(km_set | et_set)].copy()

print(f"KM facilities with coords: {len(km_geo)} (of {len(km_set)} total)")
print(f"ET facilities with coords: {len(et_geo)} (of {len(et_set)} total)")
print(f"Combined unique (KM or ET): {len(both_geo)} (of {len(km_set | et_set)} total)")

# Build GeoDataFrames in WGS84, then reproject to Albers for accurate distance math
def to_gdf(df):
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']),
        crs='EPSG:4326'
    )
    return gdf.to_crs('EPSG:5070')  # NAD83 / Conus Albers Equal Area; meters

km_pts = to_gdf(km_geo)
et_pts = to_gdf(et_geo)
both_pts = to_gdf(both_geo)

# ---------- 2. Build buffers ----------
# 3km and 10km buffers, unioned per operator to avoid double-counting
def union_buffer(gdf, meters):
    return gdf.geometry.buffer(meters).union_all()

print("\nBuilding buffers...")
km_3km_union = union_buffer(km_pts, 3000)
km_10km_union = union_buffer(km_pts, 10000)
et_3km_union = union_buffer(et_pts, 3000)
et_10km_union = union_buffer(et_pts, 10000)
both_3km_union = union_buffer(both_pts, 3000)
both_10km_union = union_buffer(both_pts, 10000)

# Compute total buffer areas (sq km)
def area_km2(geom): return geom.area / 1e6
print(f"KM 3km buffer area: {area_km2(km_3km_union):,.0f} km²")
print(f"KM 10km buffer area: {area_km2(km_10km_union):,.0f} km²")
print(f"ET 3km buffer area: {area_km2(et_3km_union):,.0f} km²")
print(f"ET 10km buffer area: {area_km2(et_10km_union):,.0f} km²")
print(f"Combined 3km buffer area: {area_km2(both_3km_union):,.0f} km²")
print(f"Combined 10km buffer area: {area_km2(both_10km_union):,.0f} km²")

# ---------- 3. Load tracts + ACS population ----------
print("\nLoading tracts...")
tracts = gpd.read_file(f'{RAW_CB}/cb_2023_us_tract_500k/cb_2023_us_tract_500k.shp')
pop = pd.read_csv(f'{RAW_POP}/ACSDT5Y2023.B01003_2026-04-15T155942/ACSDT5Y2023.B01003-Data.csv',
                  skiprows=[1])
pop['GEOID'] = pop['GEO_ID'].str[-11:]
pop['population'] = pd.to_numeric(pop['B01003_001E'], errors='coerce')
tracts['GEOID_str'] = tracts['GEOID'].astype(str)
tracts = tracts.merge(pop[['GEOID','population']], left_on='GEOID_str', right_on='GEOID', how='left')
tracts['population'] = tracts['population'].fillna(0)
print(f"Tracts with population: {(tracts['population']>0).sum()} of {len(tracts)}")

# Reproject tracts to Albers
print("Reprojecting tracts to EPSG:5070...")
tracts_albers = tracts.to_crs('EPSG:5070')
tracts_albers['tract_area_m2'] = tracts_albers.geometry.area

# ---------- 4. Area-weighted population intersection ----------
def exposure_population(buffer_geom, label):
    """Compute population within buffer via area-weighted tract intersection."""
    # Bounding box prefilter via spatial index
    buf_gs = gpd.GeoSeries([buffer_geom], crs='EPSG:5070')
    # sindex-based candidates
    candidates_idx = tracts_albers.sindex.query(buffer_geom, predicate='intersects')
    candidates = tracts_albers.iloc[candidates_idx].copy()
    print(f"  {label}: {len(candidates)} candidate tracts")

    # Clip each candidate tract to the buffer, compute overlap area
    candidates['clipped_geom'] = candidates.geometry.intersection(buffer_geom)
    candidates['overlap_area_m2'] = candidates['clipped_geom'].area
    candidates['overlap_frac'] = (candidates['overlap_area_m2'] /
                                   candidates['tract_area_m2']).clip(0, 1)
    candidates['weighted_pop'] = candidates['population'] * candidates['overlap_frac']
    total_pop = candidates['weighted_pop'].sum()
    return total_pop, candidates

print("\nComputing exposure populations...")
results = {}
for label, geom in [
    ('KM 3km', km_3km_union),
    ('KM 10km', km_10km_union),
    ('ET 3km', et_3km_union),
    ('ET 10km', et_10km_union),
    ('Combined 3km', both_3km_union),
    ('Combined 10km', both_10km_union),
]:
    total, _ = exposure_population(geom, label)
    results[label] = total
    print(f"  {label}: {total:,.0f} people")

# ---------- 5. Sanity and share-of-US ----------
us_total = tracts['population'].sum()
print(f"\nUS total population (tract-sum): {us_total:,.0f}")
print(f"Combined 3km as % of US: {100*results['Combined 3km']/us_total:.2f}%")
print(f"Combined 10km as % of US: {100*results['Combined 10km']/us_total:.2f}%")

# Save results
import json
with open(f'{OUT_DIR}/phase3_results.json', 'w') as f:
    json.dump({
        'km_facilities_with_coords': len(km_geo),
        'et_facilities_with_coords': len(et_geo),
        'combined_facilities_with_coords': len(both_geo),
        'km_facilities_total': len(km_set),
        'et_facilities_total': len(et_set),
        'combined_facilities_total': len(km_set | et_set),
        'us_total_population_tracts': float(us_total),
        'exposures': {k: float(v) for k, v in results.items()},
        'buffer_areas_km2': {
            'km_3km': float(area_km2(km_3km_union)),
            'km_10km': float(area_km2(km_10km_union)),
            'et_3km': float(area_km2(et_3km_union)),
            'et_10km': float(area_km2(et_10km_union)),
            'combined_3km': float(area_km2(both_3km_union)),
            'combined_10km': float(area_km2(both_10km_union)),
        }
    }, f, indent=2)
print(f"\nSaved: {OUT_DIR}/phase3_results.json")

# Also save the buffer geometries for map rendering
import pickle
with open(f'{OUT_DIR}/phase3_buffers.pkl', 'wb') as f:
    pickle.dump({
        'km_3km': km_3km_union,
        'km_10km': km_10km_union,
        'et_3km': et_3km_union,
        'et_10km': et_10km_union,
        'both_3km': both_3km_union,
        'both_10km': both_10km_union,
        'km_pts_albers': km_pts,
        'et_pts_albers': et_pts,
    }, f)
print(f"Saved buffer geometries")
