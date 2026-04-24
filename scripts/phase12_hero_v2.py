"""
Phase 12 / Fig 01 v2: Hero map, editorial rebuild.

Strips the original hero's self-competing layers: 7,401 gray dots PLUS the
KM/ET/JV dots meant neither read. This version makes the hero about the
thesis (the two parents) and lets scope live in the dek.

Facility classification matches Figs 07 and 14 (KM, ET, JV, other).
Other-GHGRP dots are kept at very low alpha as a ghost density wash so the
map doesn't feel empty, but the KM/ET/JV dots dominate the read.
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
OUT = '/Users/olatunde/CoWorker/Geoworks/salamituns.github.io/ghgrp/figures/ghgrp_hero_map_publication.png'

PAPER = '#F6F3EB'
INK = '#0E0E0E'
CLAY = '#A23B2A'
AMBER = '#C57B35'
VIOLET = '#6B4E8A'
MUTED = '#7A7368'
FAINT = '#D9D2C4'
GHOST = '#C9C0AE'

# ---- Facility geo + 2023 parent classification --------------------------
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

# CONUS bbox filter (exclude AK, HI, PR, territories for visual clarity)
conus = geo[(geo['Longitude'] >= -125) & (geo['Longitude'] <= -66) &
            (geo['Latitude'] >= 24) & (geo['Latitude'] <= 50)].copy()

n_total = len(conus)
n_km = (conus['class'] == 'km').sum()
n_et = (conus['class'] == 'et').sum()
n_jv = (conus['class'] == 'jv').sum()
n_other = (conus['class'] == 'other').sum()
n_affiliated = n_km + n_et + n_jv
print(f"CONUS total: {n_total}")
print(f"  KM-only: {n_km}")
print(f"  ET-only: {n_et}")
print(f"  KM+ET JV: {n_jv}")
print(f"  Other: {n_other}")
print(f"  KM/ET-affiliated (unique): {n_affiliated}")

# ---- States geometry ----------------------------------------------------
states_gdf = gpd.read_file(STATES)
conus_states = states_gdf[~states_gdf['NAME'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]

# ---- Render -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(15, 8.6), dpi=300, facecolor=PAPER)
ax.set_facecolor(PAPER)

# State basemap: faint fill + ink hairline
conus_states.plot(ax=ax, color=FAINT, edgecolor=INK, linewidth=0.4,
                  zorder=1, alpha=0.75)

# Ghost density wash for context: deliberately under-emphasized
others = conus[conus['class'] == 'other']
ax.scatter(others['Longitude'], others['Latitude'],
           s=2.4, c=GHOST, alpha=0.20, linewidth=0, zorder=2, marker='o')

# The thesis layers
et = conus[conus['class'] == 'et']
km = conus[conus['class'] == 'km']
jv = conus[conus['class'] == 'jv']

ax.scatter(et['Longitude'], et['Latitude'],
           s=34, facecolor=AMBER, edgecolor=PAPER, linewidth=0.6,
           alpha=0.92, zorder=4, marker='o')
ax.scatter(km['Longitude'], km['Latitude'],
           s=34, facecolor=CLAY, edgecolor=PAPER, linewidth=0.6,
           alpha=0.95, zorder=5, marker='o')
ax.scatter(jv['Longitude'], jv['Latitude'],
           s=68, facecolor=VIOLET, edgecolor=PAPER, linewidth=0.9,
           alpha=0.98, zorder=6, marker='D')

# Extent + frame
ax.set_xlim(-126, -65)
ax.set_ylim(23.5, 50)
ax.set_aspect(1.3)
ax.set_xticks([]); ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# ---- Title block --------------------------------------------------------
fig.text(0.04, 0.955,
         f"Two parents. {n_affiliated} facilities.",
         fontsize=28, color=INK, fontfamily='serif', fontweight='medium')
fig.text(0.04, 0.905,
         f"Kinder Morgan owns {n_km + n_jv}. Energy Transfer owns {n_et + n_jv}. "
         f"Seventeen are 50/50 joint ventures between them. Together: "
         f"{n_affiliated / 8106 * 100:.1f}% of the {8106:,} facilities "
         f"that reported to the EPA Greenhouse Gas Reporting Program in 2023, up from under 1% in 2010.",
         fontsize=11, color=MUTED, fontfamily='sans-serif')

# ---- Legend -------------------------------------------------------------
legend_handles = [
    Line2D([0],[0], marker='o', color='w', markerfacecolor=CLAY,
           markeredgecolor=PAPER, markersize=10,
           label=f"Kinder Morgan  ({n_km + n_jv} facilities)"),
    Line2D([0],[0], marker='o', color='w', markerfacecolor=AMBER,
           markeredgecolor=PAPER, markersize=10,
           label=f"Energy Transfer  ({n_et + n_jv} facilities)"),
    Line2D([0],[0], marker='D', color='w', markerfacecolor=VIOLET,
           markeredgecolor=PAPER, markersize=9,
           label=f"KM + ET joint venture  ({n_jv} facilities)"),
    Line2D([0],[0], marker='o', color='w', markerfacecolor=GHOST,
           markeredgecolor='none', markersize=5, alpha=0.6,
           label=f"All other 2023 GHGRP reporters  ({n_other:,} shown)"),
]
leg = fig.legend(handles=legend_handles, loc='lower center', frameon=False,
                 fontsize=10, labelcolor=INK, bbox_to_anchor=(0.5, 0.055),
                 ncol=4, columnspacing=2.2, handletextpad=0.7)
for t in leg.get_texts():
    t.set_fontfamily('sans-serif')

# ---- Footer -------------------------------------------------------------
fig.text(0.04, 0.025,
         "Source: EPA GHGRP 2023 Data Summary Spreadsheets + Parent Company dataset (any-stake union per facility).  "
         "State outlines: Census 2010 5m cartographic.  "
         "CONUS facilities with reported coordinates; ~7% of reporters without coordinates excluded from view.  "
         "Analysis: @salamituns.",
         fontsize=8.5, color=MUTED, fontfamily='sans-serif')

plt.subplots_adjust(left=0.02, right=0.98, top=0.86, bottom=0.11)
plt.savefig(OUT, facecolor=PAPER, dpi=300, bbox_inches='tight')
print(f"\nwrote {OUT}")
