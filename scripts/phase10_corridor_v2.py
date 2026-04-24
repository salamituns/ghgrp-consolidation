"""
Phase 10 / Fig 07 v2 \u2014 Gulf Coast Corridor, rebuilt.

Drops the Mapbox blue-ocean basemap in favour of the editorial paper/ink
palette. Zoomed to the Texas\u2013Louisiana\u2013Mississippi\u2013Alabama\u2013Florida arc.
Facilities classified into four ownership classes, layered so the Kinder
Morgan + Energy Transfer lattice reads as a lattice, not as noise.
"""
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from pyxlsb import open_workbook

GEO = '/Users/olatunde/CoWorker/Geoworks/ghgrp-repo/data/processed/ghgrp_2023_geo.csv'
RAW_XLSB = '/Users/olatunde/CoWorker/Geoworks/data/raw/epa_ghgrp/ghgp_data_parent_company.xlsb'
STATES = '/Users/olatunde/CoWorker/Geoworks/data/raw/census_boundaries/gz_2010_us_040_00_5m.json'
OUT = '/Users/olatunde/CoWorker/Geoworks/salamituns.github.io/ghgrp/figures/ghgrp_corridor_map_publication.png'

PAPER = '#F6F3EB'
INK = '#0E0E0E'
CLAY = '#A23B2A'          # Kinder Morgan
AMBER = '#C57B35'         # Energy Transfer
VIOLET = '#6B4E8A'        # KM + ET joint venture (stays distinct)
MUTED = '#7A7368'
FAINT = '#D9D2C4'         # land fill
GHOST = '#9E9689'         # other facilities

# Extent: Gulf Coast corridor
WEST, EAST = -97, -81
SOUTH, NORTH = 28.5, 35.6

# ---- Load facility geodata + 2023 KM/ET sets -----------------------------
geo = pd.read_csv(GEO)
geo = geo[geo['Latitude'].notna() & geo['Longitude'].notna()].copy()
geo['Facility Id'] = geo['Facility Id'].astype(int)

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
jv_set = km_set & et_set
km_only = km_set - jv_set
et_only = et_set - jv_set

def classify(fid):
    if fid in jv_set: return 'jv'
    if fid in km_only: return 'km'
    if fid in et_only: return 'et'
    return 'other'
geo['class'] = geo['Facility Id'].apply(classify)

# Filter to corridor bounding box
corr = geo[(geo['Longitude'] >= WEST) & (geo['Longitude'] <= EAST) &
           (geo['Latitude'] >= SOUTH) & (geo['Latitude'] <= NORTH)].copy()

print(f'Corridor total: {len(corr)}')
print(f'  Other:  {(corr["class"]=="other").sum()}')
print(f'  KM:     {(corr["class"]=="km").sum()}')
print(f'  ET:     {(corr["class"]=="et").sum()}')
print(f'  KM+ET:  {(corr["class"]=="jv").sum()}')

# ---- Render ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 6.8), dpi=300, facecolor=PAPER)
ax.set_facecolor(PAPER)

# State outlines \u2014 faint fill, ink strokes
states = gpd.read_file(STATES)
states = states[~states['NAME'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]
states.plot(ax=ax, color=FAINT, edgecolor=INK, linewidth=0.45, zorder=1, alpha=0.85)

# Facility layers, bottom-up
others = corr[corr['class'] == 'other']
km = corr[corr['class'] == 'km']
et = corr[corr['class'] == 'et']
jv = corr[corr['class'] == 'jv']

ax.scatter(others['Longitude'], others['Latitude'],
           s=7, c=GHOST, alpha=0.32, linewidth=0, zorder=2, marker='o')
ax.scatter(et['Longitude'], et['Latitude'],
           s=30, facecolor=AMBER, edgecolor=PAPER, linewidth=0.6, alpha=0.92, zorder=4, marker='o')
ax.scatter(km['Longitude'], km['Latitude'],
           s=30, facecolor=CLAY, edgecolor=PAPER, linewidth=0.6, alpha=0.95, zorder=5, marker='o')
ax.scatter(jv['Longitude'], jv['Latitude'],
           s=68, facecolor=VIOLET, edgecolor=PAPER, linewidth=0.9, alpha=0.98, zorder=6, marker='D')

# Extent + aesthetics
ax.set_xlim(WEST, EAST)
ax.set_ylim(SOUTH, NORTH)
ax.set_aspect(1.2)
ax.set_xticks([]); ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# Anchor city labels (hand-placed)
cities = [
    ('Houston',      -95.37, 29.76),
    ('New Orleans',  -90.07, 29.95),
    ('Baton Rouge',  -91.15, 30.45),
    ('Jackson',      -90.18, 32.30),
    ('Birmingham',   -86.80, 33.52),
    ('Tallahassee',  -84.28, 30.44),
    ('Corpus Christi', -97.40, 27.80),  # may be outside bbox; safe to drop if clipped
]
for name, lon, lat in cities:
    if WEST <= lon <= EAST and SOUTH <= lat <= NORTH:
        ax.scatter([lon], [lat], s=10, facecolor=INK, edgecolor=PAPER, lw=0.6, zorder=7)
        ax.text(lon + 0.15, lat + 0.12, name, fontsize=9, color=INK,
                fontfamily='sans-serif', fontweight='medium', zorder=8)

# ---- Title block ---------------------------------------------------------
fig.text(0.035, 0.96,
         "The pipeline corridor, mapped.",
         fontsize=18, color=INK, fontfamily='serif', fontweight='medium')
fig.text(0.035, 0.925,
         "Every 2023 GHGRP reporter along the Gulf Coast arc, classified by 2023 ultimate parent. "
         "Seventeen KM+ET joint-venture facilities form the shared backbone.",
         fontsize=10.5, color=MUTED, fontfamily='sans-serif')

# ---- Legend --------------------------------------------------------------
km_in = (corr['class']=='km').sum()
et_in = (corr['class']=='et').sum()
jv_in = (corr['class']=='jv').sum()
legend_handles = [
    Line2D([0],[0], marker='o', color='w', markerfacecolor=CLAY,
           markeredgecolor=PAPER, markersize=9, label=f"Kinder Morgan  ({km_in} in-frame)"),
    Line2D([0],[0], marker='o', color='w', markerfacecolor=AMBER,
           markeredgecolor=PAPER, markersize=9, label=f"Energy Transfer  ({et_in} in-frame)"),
    Line2D([0],[0], marker='D', color='w', markerfacecolor=VIOLET,
           markeredgecolor=PAPER, markersize=9, label=f"KM + ET joint venture  ({jv_in} in-frame)"),
    Line2D([0],[0], marker='o', color='w', markerfacecolor=GHOST,
           markeredgecolor='none', markersize=7, alpha=0.6,
           label=f"Other 2023 reporters  ({len(others):,} in-frame)"),
]
leg = fig.legend(handles=legend_handles, loc='lower center', frameon=False,
                 fontsize=9.5, labelcolor=INK, bbox_to_anchor=(0.5, 0.07),
                 ncol=4, columnspacing=2.0, handletextpad=0.7)
for t in leg.get_texts():
    t.set_fontfamily('sans-serif')

# ---- Footnote ------------------------------------------------------------
fig.text(0.035, 0.02,
         "Source: EPA GHGRP 2023 facility panel + Parent Company dataset (any-stake union per facility).  "
         "State outlines: Census 2010 5m cartographic.  "
         "Extent: 97\u00b0W\u201381\u00b0W, 28.5\u00b0N\u201335.6\u00b0N.  "
         "Analysis: @salamituns.",
         fontsize=8, color=MUTED, fontfamily='sans-serif')

plt.subplots_adjust(left=0.02, right=0.98, top=0.86, bottom=0.14)
plt.savefig(OUT, facecolor=PAPER, dpi=300, bbox_inches='tight')
print(f'\nwrote {OUT}')
