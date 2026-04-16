"""
GHGRP Phase 2 — Gulf Coast Corridor Map
County-level population density chloropleth + GHGRP facility overlay.
"""
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import LogNorm
import matplotlib.patches as mpatches
from matplotlib.cm import ScalarMappable
import json
from shapely.geometry import shape
from pyxlsb import open_workbook

# ---------- Extent (Gulf Coast corridor) ----------
# Trimmed south boundary to 28.5N - cuts Gulf of Mexico dead space
# while keeping Houston, southern FL JVs, New Orleans visible
WEST, EAST = -97, -81
SOUTH, NORTH = 28.5, 35.5

# ---------- Paths ----------
GEOWORKS = '/sessions/wonderful-amazing-volta/mnt/CoWorker/Geoworks'
RAW_EPA  = f'{GEOWORKS}/data/raw/epa_ghgrp'
RAW_CB   = f'{GEOWORKS}/data/raw/census_boundaries'
RAW_POP  = f'{GEOWORKS}/data/raw/census_population'
PROC     = f'{GEOWORKS}/data/processed'
VIZ      = f'{GEOWORKS}/viz'

# ---------- Load GHGRP geodata ----------
geo = pd.read_csv(f'{PROC}/ghgrp_2023_geo.csv')
geo = geo[geo['Latitude'].notna() & geo['Longitude'].notna()].copy()

with open_workbook(f'{RAW_EPA}/ghgp_data_parent_company.xlsb') as wb:
    with wb.get_sheet('2023') as sheet:
        rows = list(sheet.rows())
        headers = [c.v for c in rows[0]]
        data = [[c.v for c in r] for r in rows[1:]]
raw = pd.DataFrame(data, columns=headers)
km_set = set(raw[raw['PARENT COMPANY NAME']=='KINDER MORGAN INC']['GHGRP FACILITY ID'].astype(int))
et_set = set(raw[raw['PARENT COMPANY NAME']=='ENERGY TRANSFER LP']['GHGRP FACILITY ID'].astype(int))
jv_set = km_set & et_set
km_only = km_set - jv_set
et_only = et_set - jv_set

geo['Facility Id'] = geo['Facility Id'].astype(int)
def classify(fid):
    if fid in jv_set: return 'jv'
    if fid in km_only: return 'km'
    if fid in et_only: return 'et'
    return 'other'
geo['class'] = geo['Facility Id'].apply(classify)

# Filter to corridor extent
corridor = geo[(geo['Longitude'] >= WEST) & (geo['Longitude'] <= EAST) &
               (geo['Latitude'] >= SOUTH) & (geo['Latitude'] <= NORTH)].copy()
print(f"Facilities in corridor: {len(corridor)}")
print(f"  Other: {(corridor['class']=='other').sum()}")
print(f"  KM only: {(corridor['class']=='km').sum()}")
print(f"  ET only: {(corridor['class']=='et').sum()}")
print(f"  KM+ET JV: {(corridor['class']=='jv').sum()}")

# ---------- Load counties + population ----------
with open(f'{RAW_CB}/gz_2010_us_050_00_500k.json',
          encoding='latin-1') as f:
    gj = json.load(f)
rows = []
for feat in gj['features']:
    props = feat['properties']
    props['geometry'] = shape(feat['geometry'])
    rows.append(props)
counties = gpd.GeoDataFrame(rows, crs='EPSG:4326')
counties['fips5'] = counties['GEO_ID'].str[-5:]

pop = pd.read_csv(f'{RAW_POP}/co-est2023-alldata.csv',
                  dtype={'STATE':str,'COUNTY':str,'SUMLEV':str}, encoding='latin-1')
county_rows = pop[pop['SUMLEV'] == '050'].copy()
county_rows['fips5'] = county_rows['STATE'].str.zfill(2) + county_rows['COUNTY'].str.zfill(3)

counties = counties.merge(
    county_rows[['fips5','STNAME','CTYNAME','POPESTIMATE2023']], on='fips5', how='left'
)
counties['density'] = counties['POPESTIMATE2023'] / counties['CENSUSAREA']

# Clip counties to extent (for speed - only render what we'll show)
# But include a small buffer so county polygons crossing the edge aren't cut off
BUFFER = 1.0
bbox_counties = counties.cx[WEST-BUFFER:EAST+BUFFER, SOUTH-BUFFER:NORTH+BUFFER].copy()
print(f"\nCorridor counties: {len(bbox_counties)}")
print(f"With population: {bbox_counties['density'].notna().sum()}")

# ---------- Load states for outline ----------
with open(f'{RAW_CB}/gz_2010_us_040_00_5m.json',
          encoding='latin-1') as f:
    sj = json.load(f)
srows = []
for feat in sj['features']:
    props = feat['properties']
    props['geometry'] = shape(feat['geometry'])
    srows.append(props)
states = gpd.GeoDataFrame(srows, crs='EPSG:4326')

# ---------- Render ----------
fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
fig.patch.set_facecolor('#fafafa')
# Subtle ocean tint so the Gulf reads as water, not empty void
ax.set_facecolor('#e6eef4')

# Chloropleth: county population density (log scale, Grays)
# Fill NaN densities with a very low value so they render as near-white
bbox_counties['density_plot'] = bbox_counties['density'].fillna(0.1)
bbox_counties.plot(
    ax=ax, column='density_plot', cmap='Greys',
    norm=LogNorm(vmin=5, vmax=5000),
    edgecolor='#d0d0d0', linewidth=0.2, zorder=1
)

# State outlines on top (for orientation)
states.plot(ax=ax, color='none', edgecolor='#5a5a5a', linewidth=0.9, zorder=2)

# Facility dots
other = corridor[corridor['class'] == 'other']
km = corridor[corridor['class'] == 'km']
et = corridor[corridor['class'] == 'et']
jv = corridor[corridor['class'] == 'jv']

# Give every facility dot a white halo so they stay legible over dark chloropleth cells
HALO_KW = dict(linewidth=1.2, edgecolor='white')

ax.scatter(other['Longitude'], other['Latitude'],
           s=10, c='#2a2a2a', alpha=0.7, linewidth=0.5, edgecolor='white', zorder=3)
ax.scatter(et['Longitude'], et['Latitude'],
           s=46, c='#ff8b2a', alpha=0.95, zorder=4, **HALO_KW)
ax.scatter(km['Longitude'], km['Latitude'],
           s=46, c='#e12828', alpha=0.95, zorder=5, **HALO_KW)
ax.scatter(jv['Longitude'], jv['Latitude'],
           s=75, c='#8f3fbd', alpha=1.0, linewidth=1.4, edgecolor='white',
           zorder=6, marker='D')

# Extent
ax.set_xlim(WEST, EAST)
ax.set_ylim(SOUTH, NORTH)
ax.set_aspect(1.18)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# Title block
fig.text(0.06, 0.93, 'The corridor sits where the people are',
         fontsize=22, fontweight='bold', color='#111', family='sans-serif')
fig.text(0.06, 0.89,
         '2023 GHGRP-reporting facilities over county-level population density. Gulf Coast extent.',
         fontsize=12.5, color='#444', family='sans-serif')

# Population density colorbar — placed in top-right title area (out of the way of legend below)
cbar_ax = fig.add_axes([0.72, 0.895, 0.22, 0.015])
sm = ScalarMappable(cmap='Greys', norm=LogNorm(vmin=5, vmax=5000))
sm.set_array([])
cbar = fig.colorbar(sm, cax=cbar_ax, orientation='horizontal')
cbar.set_label('County population density (people per sq. mile, log scale)',
               fontsize=9, color='#444', labelpad=4)
cbar.ax.tick_params(labelsize=8, colors='#444')
cbar.outline.set_visible(False)

# Facility legend
legend_elems = [
    Line2D([0],[0], marker='o', color='w', markerfacecolor='#e12828', markersize=10,
           label=f'Kinder Morgan  ({(corridor["class"]=="km").sum()} in corridor)'),
    Line2D([0],[0], marker='o', color='w', markerfacecolor='#ff8b2a', markersize=10,
           label=f'Energy Transfer  ({(corridor["class"]=="et").sum()} in corridor)'),
    Line2D([0],[0], marker='D', color='w', markerfacecolor='#8f3fbd', markersize=9,
           label=f'KM + ET joint venture  ({(corridor["class"]=="jv").sum()} in corridor, 17 nationally)'),
    Line2D([0],[0], marker='o', color='w', markerfacecolor='#3a3a3a', markersize=6, alpha=0.7,
           label=f'All other GHGRP reporters  ({(corridor["class"]=="other").sum()} in corridor)'),
]
# Legend placed BELOW the map axes so it never overlaps facility dots
leg = fig.legend(handles=legend_elems, loc='lower center', frameon=False,
                 fontsize=10, labelcolor='#222', bbox_to_anchor=(0.5, 0.14),
                 ncol=4, columnspacing=1.4, handletextpad=0.4)

# Footer
fig.text(0.06, 0.07,
         'Sources: EPA GHGRP 2023 Data Summary Spreadsheets + Parent Company Dataset; US Census Bureau County Population Estimates (2023); Census Cartographic Boundary Files (500k counties, 5m states).',
         fontsize=8.5, color='#666', family='sans-serif')
fig.text(0.06, 0.05,
         'Corridor extent: 97°W to 81°W, 27.5°N to 35.5°N. Connecticut counties excluded (state replaced counties with planning regions in 2020; not in view anyway).',
         fontsize=8.5, color='#666', family='sans-serif')
fig.text(0.06, 0.015,
         'Analysis: @salamituns  |  Stratdevs (Tareony)',
         fontsize=9, color='#888', family='sans-serif', style='italic')

plt.subplots_adjust(left=0.03, right=0.97, top=0.86, bottom=0.21)

OUT = f'{VIZ}/ghgrp_corridor_map_2023.png'
plt.savefig(OUT, dpi=200, bbox_inches='tight', facecolor='#fafafa')
print(f"\nSaved: {OUT}")
plt.close()
