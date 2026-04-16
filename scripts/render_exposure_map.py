"""
Phase 3 — National population exposure map.
KM and ET 10km buffers overlaid on tract-level population density.
"""
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.colors import LogNorm
from matplotlib.cm import ScalarMappable
import json
import pickle
from shapely.geometry import shape

GEOWORKS = '/sessions/wonderful-amazing-volta/mnt/CoWorker/Geoworks'
RAW_CB   = f'{GEOWORKS}/data/raw/census_boundaries'
RAW_POP  = f'{GEOWORKS}/data/raw/census_population'
PROC     = f'{GEOWORKS}/data/processed'
VIZ      = f'{GEOWORKS}/viz'

# Load pre-computed buffers + results
with open(f'{PROC}/phase3_buffers.pkl', 'rb') as f:
    buffers = pickle.load(f)
with open(f'{PROC}/phase3_results.json') as f:
    results = json.load(f)

km_10km = buffers['km_10km']
et_10km = buffers['et_10km']
km_pts_albers = buffers['km_pts_albers']
et_pts_albers = buffers['et_pts_albers']

# ---------- Tracts + population for basemap chloropleth ----------
print("Loading tracts...")
tracts = gpd.read_file(f'{RAW_CB}/cb_2023_us_tract_500k/cb_2023_us_tract_500k.shp')
pop = pd.read_csv(f'{RAW_POP}/ACSDT5Y2023.B01003_2026-04-15T155942/ACSDT5Y2023.B01003-Data.csv',
                  skiprows=[1])
pop['GEOID'] = pop['GEO_ID'].str[-11:]
pop['population'] = pd.to_numeric(pop['B01003_001E'], errors='coerce')
tracts['GEOID_str'] = tracts['GEOID'].astype(str)
tracts = tracts.merge(pop[['GEOID','population']], left_on='GEOID_str', right_on='GEOID', how='left')
tracts['population'] = tracts['population'].fillna(0)

# Compute density
tracts_albers = tracts.to_crs('EPSG:5070')
tracts_albers['area_m2'] = tracts_albers.geometry.area
tracts_albers['density'] = (tracts_albers['population'] /
                             (tracts_albers['area_m2'] / 2.59e6))  # people per sq mile

# Filter CONUS only for display
CONUS_STATES = [
    'AL','AR','AZ','CA','CO','CT','DE','FL','GA','IA','ID','IL','IN','KS','KY',
    'LA','MA','MD','ME','MI','MN','MO','MS','MT','NC','ND','NE','NH','NJ','NM',
    'NV','NY','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VA','VT','WA',
    'WI','WV','WY','DC'
]
conus_tracts = tracts_albers[tracts_albers['STUSPS'].isin(CONUS_STATES)].copy()
print(f"CONUS tracts: {len(conus_tracts)}")

# ---------- State outlines ----------
with open(f'{RAW_CB}/gz_2010_us_040_00_5m.json', encoding='latin-1') as f:
    sj = json.load(f)
srows = []
for feat in sj['features']:
    p = feat['properties']
    p['geometry'] = shape(feat['geometry'])
    srows.append(p)
states = gpd.GeoDataFrame(srows, crs='EPSG:4326').to_crs('EPSG:5070')
conus_states = states[~states['NAME'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]

# ---------- Render ----------
fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
fig.patch.set_facecolor('#fafafa')
ax.set_facecolor('#e6eef4')

# Background: tract density chloropleth (subtle gray, log scale)
conus_tracts.plot(
    ax=ax, column='density', cmap='Greys',
    norm=LogNorm(vmin=10, vmax=5000),
    edgecolor='none', zorder=1
)

# State outlines on top of tract chloropleth
conus_states.plot(ax=ax, color='none', edgecolor='#6a6a6a', linewidth=0.7, zorder=2)

# 10km buffers: ET first (orange), KM on top (crimson)
et_buf_gs = gpd.GeoSeries([et_10km], crs='EPSG:5070')
km_buf_gs = gpd.GeoSeries([km_10km], crs='EPSG:5070')

et_buf_gs.plot(ax=ax, color='#ff8b2a', alpha=0.65, edgecolor='#6a2800',
               linewidth=0.7, zorder=3)
km_buf_gs.plot(ax=ax, color='#e12828', alpha=0.65, edgecolor='#5a0a0c',
               linewidth=0.7, zorder=4)

# Facility dots
# KM first then ET on top (or consistent order as in prior maps)
et_pts_albers.plot(ax=ax, color='#ff8b2a', markersize=6, zorder=5,
                   edgecolor='white', linewidth=0.3)
km_pts_albers.plot(ax=ax, color='#e12828', markersize=6, zorder=6,
                   edgecolor='white', linewidth=0.3)

# CONUS extent
ax.set_xlim(-2.4e6, 2.3e6)
ax.set_ylim(2.8e5, 3.2e6)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# Title block (tightened)
fig.text(0.06, 0.945, '7.7 million Americans live within 10 km',
         fontsize=24, fontweight='bold', color='#111', family='sans-serif')
fig.text(0.06, 0.905, 'of a facility owned by Kinder Morgan or Energy Transfer.',
         fontsize=13, color='#333', family='sans-serif')

# Metric cards (tighter vertical, one row)
def card(x, top, value, label, color='#111'):
    fig.text(x, top,     value, fontsize=17, fontweight='bold', color=color)
    fig.text(x, top-0.022, label, fontsize=9.5, color='#444')

card(0.06, 0.855, f"{results['exposures']['Combined 3km']/1e3:,.0f}K", 'within 3 km', '#c8292c')
card(0.18, 0.855, f"{results['exposures']['Combined 10km']/1e6:,.1f}M", 'within 10 km', '#c8292c')
card(0.30, 0.855, f"{results['combined_facilities_with_coords']}", 'KM + ET facilities', '#333')
card(0.42, 0.855, f"{results['buffer_areas_km2']['combined_10km']/1e3:,.0f}K km²", '10 km buffer area', '#333')

# Legend
legend_elems = [
    Patch(facecolor='#e12828', alpha=0.55, label='Kinder Morgan 10 km buffer'),
    Patch(facecolor='#ff8b2a', alpha=0.55, label='Energy Transfer 10 km buffer'),
    Line2D([0],[0], marker='o', color='w', markerfacecolor='#e12828',
           markersize=8, label='KM facilities (224 with coords)'),
    Line2D([0],[0], marker='o', color='w', markerfacecolor='#ff8b2a',
           markersize=8, label='ET facilities (184 with coords)'),
]
leg = fig.legend(handles=legend_elems, loc='lower center', frameon=False,
                 fontsize=10, labelcolor='#222', bbox_to_anchor=(0.5, 0.13),
                 ncol=4, columnspacing=1.4, handletextpad=0.4)

# Footer
fig.text(0.06, 0.07,
         'Sources: EPA GHGRP 2023 Data Summary Spreadsheets + Parent Company Dataset; US Census ACS 2019-2023 5-year Tract Population (Table B01003); Census Cartographic Boundary Files.',
         fontsize=8.5, color='#666')
fig.text(0.06, 0.05,
         'Methodology: 3 km and 10 km Euclidean buffers around each KM/ET facility in EPSG:5070 (US Albers Equal Area), unioned per operator, area-weighted tract population allocation.',
         fontsize=8.5, color='#666')
fig.text(0.06, 0.03,
         '7 Kinder Morgan facilities (3%) without reported coordinates are excluded. CONUS only. Buffer proximity does not mean emission exposure; see methodology note.',
         fontsize=8.5, color='#666')
fig.text(0.06, 0.01,
         'Analysis: @salamituns  |  Stratdevs (Tareony)',
         fontsize=9, color='#888', style='italic')

plt.subplots_adjust(left=0.03, right=0.97, top=0.80, bottom=0.18)

OUT = f'{VIZ}/ghgrp_exposure_map_2023.png'
plt.savefig(OUT, dpi=200, bbox_inches='tight', facecolor='#fafafa')
print(f"\nSaved: {OUT}")
plt.close()
