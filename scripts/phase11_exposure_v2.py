"""
Phase 11 / Fig 11 v2: National population exposure map, editorial palette.

Rebuilds KM/ET buffers inline from the 2023 facility geo CSV + XLSB parent
panel (no pickle, safer to re-run). Keeps the informational layers:
tract-density basemap (ghost greys, log scale) → state outlines → KM/ET
10 km union buffers → KM/ET facility dots.
"""
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.colors import LogNorm
import json
from shapely.geometry import shape
from shapely.ops import unary_union
from pyxlsb import open_workbook

RAW_CB = '/Users/olatunde/CoWorker/Geoworks/data/raw/census_boundaries'
RAW_POP = '/Users/olatunde/CoWorker/Geoworks/data/raw/census_population'
RAW_XLSB = '/Users/olatunde/CoWorker/Geoworks/data/raw/epa_ghgrp/ghgp_data_parent_company.xlsb'
PROC = '/Users/olatunde/CoWorker/Geoworks/ghgrp-repo/data/processed'
GEO_CSV = f'{PROC}/ghgrp_2023_geo.csv'
OUT = '/Users/olatunde/CoWorker/Geoworks/salamituns.github.io/ghgrp/figures/ghgrp_exposure_map_2023.png'

PAPER = '#F6F3EB'
INK = '#0E0E0E'
CLAY = '#A23B2A'
AMBER = '#C57B35'
MUTED = '#7A7368'
FAINT = '#D9D2C4'

# ---- Identify KM/ET facility IDs from 2023 parent panel -----------------
print('Loading parent panel 2023...')
with open_workbook(RAW_XLSB) as wb:
    with wb.get_sheet('2023') as sheet:
        rows = list(sheet.rows())
        headers = [c.v for c in rows[0]]
        data = [[c.v for c in r] for r in rows[1:]]
raw = pd.DataFrame(data, columns=headers)
raw = raw.dropna(subset=['GHGRP FACILITY ID', 'PARENT COMPANY NAME']).copy()
raw['GHGRP FACILITY ID'] = raw['GHGRP FACILITY ID'].astype(int)

km_set = set(raw[raw['PARENT COMPANY NAME'].str.contains('KINDER MORGAN', case=False, na=False)]['GHGRP FACILITY ID'])
et_set = set(raw[raw['PARENT COMPANY NAME'].str.contains('ENERGY TRANSFER', case=False, na=False)]['GHGRP FACILITY ID'])

# ---- Facility geo points -------------------------------------------------
geo = pd.read_csv(GEO_CSV)
geo = geo[geo['Latitude'].notna() & geo['Longitude'].notna()].copy()
geo['Facility Id'] = geo['Facility Id'].astype(int)
km_geo = geo[geo['Facility Id'].isin(km_set)].copy()
et_geo = geo[geo['Facility Id'].isin(et_set) & ~geo['Facility Id'].isin(km_set)].copy()
print(f'KM with coords: {len(km_geo)} / {len(km_set)} total')
print(f'ET (non-JV) with coords: {len(et_geo)} / {len(et_set - km_set)} total')

km_gdf = gpd.GeoDataFrame(km_geo, geometry=gpd.points_from_xy(km_geo['Longitude'], km_geo['Latitude']),
                          crs='EPSG:4326').to_crs('EPSG:5070')
et_gdf = gpd.GeoDataFrame(et_geo, geometry=gpd.points_from_xy(et_geo['Longitude'], et_geo['Latitude']),
                          crs='EPSG:4326').to_crs('EPSG:5070')

# 10 km buffers, unioned per operator
km_10km = unary_union(km_gdf.geometry.buffer(10_000).values)
et_10km = unary_union(et_gdf.geometry.buffer(10_000).values)

# ---- Load canned exposure stats for the card row ------------------------
with open(f'{PROC}/phase3_results.json') as f:
    results = json.load(f)

# ---- Tract density basemap ----------------------------------------------
print('Loading tracts...')
tracts = gpd.read_file(f'{RAW_CB}/cb_2023_us_tract_500k/cb_2023_us_tract_500k.shp')
pop = pd.read_csv(f'{RAW_POP}/ACSDT5Y2023.B01003_2026-04-15T155942/ACSDT5Y2023.B01003-Data.csv',
                  skiprows=[1])
pop['GEOID'] = pop['GEO_ID'].str[-11:]
pop['population'] = pd.to_numeric(pop['B01003_001E'], errors='coerce')
tracts = tracts.merge(pop[['GEOID', 'population']], on='GEOID', how='left')
tracts['population'] = tracts['population'].fillna(0)

tracts_albers = tracts.to_crs('EPSG:5070')
tracts_albers['area_m2'] = tracts_albers.geometry.area
tracts_albers['density'] = (tracts_albers['population'] / (tracts_albers['area_m2'] / 2.59e6))

CONUS_STATES = ['AL','AR','AZ','CA','CO','CT','DE','FL','GA','IA','ID','IL','IN','KS','KY',
                'LA','MA','MD','ME','MI','MN','MO','MS','MT','NC','ND','NE','NH','NJ','NM',
                'NV','NY','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VA','VT','WA',
                'WI','WV','WY','DC']
conus_tracts = tracts_albers[tracts_albers['STUSPS'].isin(CONUS_STATES)].copy()
print(f'CONUS tracts: {len(conus_tracts)}')

# ---- State outlines ------------------------------------------------------
with open(f'{RAW_CB}/gz_2010_us_040_00_5m.json', encoding='latin-1') as f:
    sj = json.load(f)
srows = []
for feat in sj['features']:
    p = feat['properties']
    p['geometry'] = shape(feat['geometry'])
    srows.append(p)
states = gpd.GeoDataFrame(srows, crs='EPSG:4326').to_crs('EPSG:5070')
conus_states = states[~states['NAME'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]

# ---- Render --------------------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 8), dpi=300, facecolor=PAPER)
ax.set_facecolor(PAPER)

conus_tracts.plot(
    ax=ax, column='density', cmap='bone_r',
    norm=LogNorm(vmin=20, vmax=5000),
    edgecolor='none', zorder=1, alpha=0.55
)
conus_states.plot(ax=ax, color='none', edgecolor=INK, linewidth=0.5, zorder=2, alpha=0.6)

et_buf = gpd.GeoSeries([et_10km], crs='EPSG:5070')
km_buf = gpd.GeoSeries([km_10km], crs='EPSG:5070')
et_buf.plot(ax=ax, color=AMBER, alpha=0.40, edgecolor=AMBER, linewidth=0.5, zorder=3)
km_buf.plot(ax=ax, color=CLAY, alpha=0.45, edgecolor=CLAY, linewidth=0.5, zorder=4)

et_gdf.plot(ax=ax, color=AMBER, markersize=6, zorder=5, edgecolor=PAPER, linewidth=0.3)
km_gdf.plot(ax=ax, color=CLAY, markersize=6, zorder=6, edgecolor=PAPER, linewidth=0.3)

ax.set_xlim(-2.4e6, 2.3e6)
ax.set_ylim(2.8e5, 3.2e6)
ax.set_aspect('equal')
ax.set_xticks([]); ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# ---- Title block ---------------------------------------------------------
fig.text(0.04, 0.955, "7.7 million Americans, within 10 km.",
         fontsize=22, color=INK, fontfamily='serif', fontweight='medium')
fig.text(0.04, 0.915,
         "Of a facility owned by Kinder Morgan or Energy Transfer, the two "
         "pipeline operators that gained the most GHGRP reporters between 2010 and 2023.",
         fontsize=11, color=MUTED, fontfamily='sans-serif')

# ---- Stat cards ----------------------------------------------------------
def card(x, top, value, label, color=INK):
    fig.text(x, top,       value, fontsize=18, color=color,
             fontfamily='serif', fontweight='medium')
    fig.text(x, top-0.028, label, fontsize=9.5, color=MUTED, fontfamily='sans-serif')

card(0.04, 0.863, f"{results['exposures']['Combined 3km']/1e3:,.0f}K", 'within 3 km', CLAY)
card(0.17, 0.863, f"{results['exposures']['Combined 10km']/1e6:,.1f}M", 'within 10 km', CLAY)
card(0.30, 0.863, f"{results['combined_facilities_with_coords']}", 'KM + ET facilities')
card(0.45, 0.863, f"{results['buffer_areas_km2']['combined_10km']/1e3:,.0f}K km²", '10 km buffer area')

# ---- Legend --------------------------------------------------------------
legend_elems = [
    Patch(facecolor=CLAY, alpha=0.45, label='Kinder Morgan 10 km buffer'),
    Patch(facecolor=AMBER, alpha=0.40, label='Energy Transfer 10 km buffer'),
    Line2D([0],[0], marker='o', color='w', markerfacecolor=CLAY,
           markeredgecolor=PAPER, markersize=7, label=f'KM facilities ({len(km_gdf)} with coords)'),
    Line2D([0],[0], marker='o', color='w', markerfacecolor=AMBER,
           markeredgecolor=PAPER, markersize=7, label=f'ET facilities ({len(et_gdf)} with coords)'),
]
leg = fig.legend(handles=legend_elems, loc='lower center', frameon=False,
                 fontsize=9.5, labelcolor=INK, bbox_to_anchor=(0.5, 0.10),
                 ncol=4, columnspacing=1.4, handletextpad=0.5)
for t in leg.get_texts():
    t.set_fontfamily('sans-serif')

# ---- Footer --------------------------------------------------------------
fig.text(0.04, 0.055,
         "Sources: EPA GHGRP 2023 Data Summary Spreadsheets + Parent Company dataset; "
         "US Census ACS 2019–2023 5-year Tract Population (B01003); Census Cartographic Boundaries.",
         fontsize=8, color=MUTED, fontfamily='sans-serif')
fig.text(0.04, 0.035,
         "Methodology: 3 km and 10 km Euclidean buffers around each KM/ET facility in EPSG:5070 "
         "(US Albers Equal Area), unioned per operator, area-weighted tract population allocation.",
         fontsize=8, color=MUTED, fontfamily='sans-serif')
fig.text(0.04, 0.018,
         "Kinder Morgan facilities without reported coordinates are excluded. CONUS only. "
         "Buffer proximity \u2260 emission exposure. Analysis: @salamituns.",
         fontsize=8, color=MUTED, fontfamily='sans-serif')

plt.subplots_adjust(left=0.02, right=0.98, top=0.82, bottom=0.16)
plt.savefig(OUT, facecolor=PAPER, dpi=300, bbox_inches='tight')
print(f"wrote {OUT}")
