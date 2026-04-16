"""
GHGRP Hero Map - Phase 1
Renders all 2023 GHGRP facilities with Kinder Morgan + Energy Transfer highlighted.
"""
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from shapely.geometry import Point

# ---------- Paths ----------
GEOWORKS = '/sessions/wonderful-amazing-volta/mnt/CoWorker/Geoworks'
RAW_EPA  = f'{GEOWORKS}/data/raw/epa_ghgrp'
RAW_CB   = f'{GEOWORKS}/data/raw/census_boundaries'
PROC     = f'{GEOWORKS}/data/processed'
VIZ      = f'{GEOWORKS}/viz'

# ---------- Load data ----------
geo = pd.read_csv(f'{PROC}/ghgrp_2023_geo.csv')
ops = pd.read_csv(f'{PROC}/ghgrp_2023_primary_operator.csv')
ops['Facility Id'] = ops['GHGRP FACILITY ID'].astype(int)
geo['Facility Id'] = geo['Facility Id'].astype(int)

# Compute JV flag: facilities where BOTH KM and ET appear in the raw ownership table
from pyxlsb import open_workbook
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

# Merge
df = geo.merge(ops[['Facility Id','PRIMARY_OPERATOR']], on='Facility Id', how='left')
df = df[df['Latitude'].notna() & df['Longitude'].notna()].copy()

# Classify
def classify(fid):
    if fid in jv_set: return 'jv'
    if fid in km_only: return 'km'
    if fid in et_only: return 'et'
    return 'other'
df['class'] = df['Facility Id'].apply(classify)

# Filter to CONUS bbox (exclude AK, HI, territories for visual clarity)
conus = df[(df['Longitude'] >= -125) & (df['Longitude'] <= -66) &
           (df['Latitude'] >= 24) & (df['Latitude'] <= 50)].copy()

print(f"Total geocoded: {len(df)}")
print(f"CONUS subset: {len(conus)}")
print(f"  Other: {(conus['class']=='other').sum()}")
print(f"  KM only: {(conus['class']=='km').sum()}")
print(f"  ET only: {(conus['class']=='et').sum()}")
print(f"  KM+ET JV: {(conus['class']=='jv').sum()}")

# ---------- US states outline (Census 5m GeoJSON, dropped by Tee) ----------
states = gpd.read_file(f'{RAW_CB}/gz_2010_us_040_00_5m.json')

# ---------- Render ----------
fig, ax = plt.subplots(figsize=(16, 10), dpi=150)
fig.patch.set_facecolor('#fafafa')
ax.set_facecolor('#fafafa')

# Basemap: US states outlines, clipped to CONUS (exclude AK, HI, PR)
conus_states = states[~states['NAME'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]
conus_states.plot(ax=ax, color='#f0f0f0', edgecolor='#b0b0b0', linewidth=0.6, zorder=1)

# Plot layers in order: other (bottom) -> ET -> KM -> JV (top)
other = conus[conus['class'] == 'other']
km = conus[conus['class'] == 'km']
et = conus[conus['class'] == 'et']
jv = conus[conus['class'] == 'jv']

ax.scatter(other['Longitude'], other['Latitude'],
           s=4, c='#7a7a7a', alpha=0.35, linewidth=0, zorder=2)
ax.scatter(et['Longitude'], et['Latitude'],
           s=22, c='#e8822c', alpha=0.85, linewidth=0.3, edgecolor='#8a4a10', zorder=3)
ax.scatter(km['Longitude'], km['Latitude'],
           s=22, c='#c8292c', alpha=0.85, linewidth=0.3, edgecolor='#6a1214', zorder=4)
ax.scatter(jv['Longitude'], jv['Latitude'],
           s=35, c='#7b3fa0', alpha=0.95, linewidth=0.7, edgecolor='#2e1545', zorder=5,
           marker='D')

# Extent
ax.set_xlim(-126, -65)
ax.set_ylim(23.5, 50)
ax.set_aspect(1.3)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# Title block
fig.text(0.06, 0.93, 'This is what consolidation looks like on the ground',
         fontsize=22, fontweight='bold', color='#111', family='sans-serif')
fig.text(0.06, 0.89, 'Kinder Morgan + Energy Transfer grew from 43 facilities in 2010 to 415 in 2023. They bought, not built.',
         fontsize=12.5, color='#444', family='sans-serif')

# Legend (hand-built for precise typography)
legend_elems = [
    Line2D([0],[0], marker='o', color='w', markerfacecolor='#c8292c', markersize=10,
           label=f'Kinder Morgan  ({len(km_only)} wholly owned + 17 JV = 231 total)'),
    Line2D([0],[0], marker='o', color='w', markerfacecolor='#e8822c', markersize=10,
           label=f'Energy Transfer  ({len(et_only)} wholly owned + 17 JV = 184 total)'),
    Line2D([0],[0], marker='D', color='w', markerfacecolor='#7b3fa0', markersize=9,
           label=f'KM + ET joint venture  ({len(jv_set)} facilities, mostly Florida Gas Transmission)'),
    Line2D([0],[0], marker='o', color='w', markerfacecolor='#7a7a7a', markersize=6, alpha=0.6,
           label=f'All other 2023 GHGRP reporters  ({len(other):,} shown; 8,106 total)'),
]
leg = ax.legend(handles=legend_elems, loc='lower left', frameon=False,
                fontsize=10.5, labelcolor='#222', bbox_to_anchor=(0.01, 0.02))

# Footer
fig.text(0.06, 0.05,
         'Source: EPA Greenhouse Gas Reporting Program, 2023 Data Summary Spreadsheets + Parent Company Dataset.',
         fontsize=9, color='#666', family='sans-serif')
fig.text(0.06, 0.03,
         'CONUS only. Facilities without reported coordinates (7.0%, mostly small natural gas LDCs) are excluded from this view.',
         fontsize=9, color='#666', family='sans-serif')
fig.text(0.06, 0.01,
         'Analysis: @salamituns  |  Stratdevs (Tareony)',
         fontsize=9, color='#888', family='sans-serif', style='italic')

plt.subplots_adjust(left=0.02, right=0.98, top=0.86, bottom=0.08)

OUT = f'{VIZ}/ghgrp_hero_map_2023.png'
plt.savefig(OUT, dpi=200, bbox_inches='tight', facecolor='#fafafa')
print(f"\nSaved: {OUT}")
plt.close()
