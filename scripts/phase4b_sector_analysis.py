"""
Phase 4b — Power, Refineries, Petrochemicals
Concentration comparison across sectors + companion refineries map.
"""
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
import json
import openpyxl
from pyxlsb import open_workbook
from shapely.geometry import shape

GEOWORKS = '/sessions/wonderful-amazing-volta/mnt/CoWorker/Geoworks'
RAW_EPA  = f'{GEOWORKS}/data/raw/epa_ghgrp'
RAW_CB   = f'{GEOWORKS}/data/raw/census_boundaries'
PROC     = f'{GEOWORKS}/data/processed'
VIZ      = f'{GEOWORKS}/viz'

# ---------- 1. Load Direct Point Emitters, identify sector sets ----------
PATH = f'{RAW_EPA}/2023_data_summary_spreadsheets/ghgp_data_2023.xlsx'
wb = openpyxl.load_workbook(PATH, read_only=True, data_only=True)
ws = wb['Direct Point Emitters']
rows = list(ws.iter_rows(values_only=True))
headers = list(rows[3])
data = [r for r in rows[4:] if r[0] is not None]
wb.close()
dpe = pd.DataFrame(data, columns=headers)
dpe['Facility Id'] = dpe['Facility Id'].astype(int)

def has_sector(s, sector):
    return sector in str(s or '').split(',')
dpe['is_power']   = dpe['Industry Type (sectors)'].apply(lambda s: has_sector(s, 'Power Plants'))
dpe['is_refinery']= dpe['Industry Type (sectors)'].apply(lambda s: has_sector(s, 'Refineries'))
dpe['is_chem']    = dpe['Industry Type (sectors)'].apply(lambda s: has_sector(s, 'Chemicals'))

power_ids    = set(dpe[dpe['is_power']]['Facility Id'])
refinery_ids = set(dpe[dpe['is_refinery']]['Facility Id'])
chem_ids     = set(dpe[dpe['is_chem']]['Facility Id'])

# ---------- 2. Ownership analysis ----------
with open_workbook(f'{RAW_EPA}/ghgp_data_parent_company.xlsb') as pwb:
    with pwb.get_sheet('2023') as sheet:
        rows = list(sheet.rows())
        headers = [c.v for c in rows[0]]
        data = [[c.v for c in r] for r in rows[1:]]
parent = pd.DataFrame(data, columns=headers)
parent['GHGRP FACILITY ID'] = parent['GHGRP FACILITY ID'].astype(int)

def sector_metrics(ids, label):
    sp = parent[parent['GHGRP FACILITY ID'].isin(ids)]
    total = sp['GHGRP FACILITY ID'].nunique()
    by_parent = sp.groupby('PARENT COMPANY NAME')['GHGRP FACILITY ID'].nunique().sort_values(ascending=False)
    top10 = by_parent.head(10)
    top10_share = sp[sp['PARENT COMPANY NAME'].isin(top10.index)]['GHGRP FACILITY ID'].nunique() / total * 100
    return {
        'label': label,
        'total_facilities': int(total),
        'unique_parents': int(sp['PARENT COMPANY NAME'].nunique()),
        'top10_share_pct': float(top10_share),
        'top10': {n: int(c) for n, c in top10.items()},
    }

results = {}
results['power']      = sector_metrics(power_ids,    'Power Plants')
results['refineries'] = sector_metrics(refinery_ids, 'Refineries')
results['petrochem']  = sector_metrics(chem_ids,     'Petrochemicals')

# Load Phase 4a O&G result from processed
with open(f'{PROC}/phase4_og_results.json') as f:
    og_results = json.load(f)
results['oil_gas'] = {
    'label': 'Oil & Gas',
    'total_facilities': og_results['og_total_facilities'],
    'unique_parents': og_results['og_unique_parents'],
    'top10_share_pct': og_results['og_top10_share_pct'],
    'top10': og_results['top10_og'],
}

# GHGRP-wide
total_ghgrp = parent['GHGRP FACILITY ID'].nunique()
ghgrp_by_parent = parent.groupby('PARENT COMPANY NAME')['GHGRP FACILITY ID'].nunique().sort_values(ascending=False)
ghgrp_top10 = ghgrp_by_parent.head(10)
ghgrp_top10_share = parent[parent['PARENT COMPANY NAME'].isin(ghgrp_top10.index)]['GHGRP FACILITY ID'].nunique() / total_ghgrp * 100
results['ghgrp_wide'] = {
    'label': 'GHGRP-wide',
    'total_facilities': int(total_ghgrp),
    'unique_parents': int(parent['PARENT COMPANY NAME'].nunique()),
    'top10_share_pct': float(ghgrp_top10_share),
    'top10': {n: int(c) for n, c in ghgrp_top10.items()},
}

with open(f'{PROC}/phase4b_sector_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("Saved phase4b_sector_results.json")

for key in ['refineries', 'oil_gas', 'petrochem', 'power', 'ghgrp_wide']:
    r = results[key]
    print(f"  {r['label']}: {r['total_facilities']} facilities, top-10 share {r['top10_share_pct']:.1f}%")

# ---------- 3. Render: Hero bar chart ----------
order = ['refineries', 'oil_gas', 'petrochem', 'power', 'ghgrp_wide']
labels = [results[k]['label'] for k in order]
shares = [results[k]['top10_share_pct'] for k in order]
totals = [results[k]['total_facilities'] for k in order]

fig, ax = plt.subplots(figsize=(14, 8), dpi=150)
fig.patch.set_facecolor('#fafafa')
ax.set_facecolor('#fafafa')

colors = ['#a81e1e', '#e12828', '#d13d80', '#2a6cd4', '#7a7a7a']
bars = ax.barh(labels, shares, color=colors, edgecolor='white', linewidth=1.5, height=0.68)

# Data labels on bars
for i, (bar, share, total) in enumerate(zip(bars, shares, totals)):
    x = share + 1.0
    ax.text(x, bar.get_y() + bar.get_height()/2,
            f'{share:.1f}%  ',
            va='center', fontsize=14, fontweight='bold', color='#111')
    ax.text(x + 6.5, bar.get_y() + bar.get_height()/2,
            f'({total:,} facilities)',
            va='center', fontsize=10.5, color='#555')

# Reference line at GHGRP-wide baseline
baseline = results['ghgrp_wide']['top10_share_pct']
ax.axvline(baseline, color='#555', linestyle=':', linewidth=1.2, alpha=0.7, zorder=0)
ax.text(baseline+0.3, 4.55, f'  GHGRP baseline', fontsize=9, color='#555', ha='left')

ax.set_xlim(0, 68)
ax.invert_yaxis()
ax.tick_params(axis='y', labelsize=13, colors='#222')
ax.tick_params(axis='x', labelsize=10, colors='#555')
ax.set_xlabel('Share of sector facilities controlled by top 10 parent companies (%)',
              fontsize=11, color='#333', labelpad=10)
for spine in ['top','right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#bbb')
ax.spines['bottom'].set_color('#bbb')

# Title
fig.text(0.05, 0.96, 'Not all sectors are equally consolidated',
         fontsize=22, fontweight='bold', color='#111')
fig.text(0.05, 0.925,
         'US petroleum refineries are 3.2x more concentrated than the full GHGRP. Power plants are the least concentrated major sector.',
         fontsize=12, color='#444')

# Footer
fig.text(0.05, 0.06,
         'Source: EPA GHGRP 2023 — Parent Company Dataset + Data Summary Spreadsheets. Sector membership from "Industry Type (sectors)" column. Top-10 share = share of unique facilities where any top-10 parent holds an ownership stake (any-stake union rule).',
         fontsize=8.5, color='#666')
fig.text(0.05, 0.04,
         'Oil & Gas defined as Subpart W (petroleum and natural gas systems) per Phase 4a. Refineries = Subpart Y. Petrochemicals = "Chemicals" sector label. Power Plants = "Power Plants" sector label.',
         fontsize=8.5, color='#666')
fig.text(0.05, 0.02,
         'Analysis: @salamituns  |  Stratdevs (Tareony)',
         fontsize=9, color='#888', style='italic')

plt.subplots_adjust(left=0.12, right=0.97, top=0.87, bottom=0.15)

OUT = f'{VIZ}/ghgrp_sector_concentration_2023.png'
plt.savefig(OUT, dpi=200, bbox_inches='tight', facecolor='#fafafa')
print(f"\nSaved hero chart: {OUT}")
plt.close()

# ---------- 4. Companion: Refineries operator map ----------
print("\nBuilding refineries map...")
geo = pd.read_csv(f'{PROC}/ghgrp_2023_geo.csv')
geo['Facility Id'] = geo['Facility Id'].astype(int)
refinery_geo = geo[geo['Facility Id'].isin(refinery_ids)].copy()

# Assign top operator
top10_ref_names = list(results['refineries']['top10'].keys())
priority = {n: i for i, n in enumerate(top10_ref_names)}
def top_owner(gid):
    owners = set(parent[parent['GHGRP FACILITY ID']==gid]['PARENT COMPANY NAME'])
    top10_owners = [n for n in owners if n in priority]
    return sorted(top10_owners, key=lambda n: priority[n])[0] if top10_owners else 'other'
refinery_geo['owner'] = refinery_geo['Facility Id'].apply(top_owner)
refinery_geo.to_csv(f'{PROC}/ghgrp_2023_refineries.csv', index=False)

# States basemap
with open(f'{RAW_CB}/gz_2010_us_040_00_5m.json', encoding='latin-1') as f:
    sj = json.load(f)
srows=[]
for feat in sj['features']:
    p = feat['properties']
    p['geometry'] = shape(feat['geometry'])
    srows.append(p)
states = gpd.GeoDataFrame(srows, crs='EPSG:4326')
conus_states = states[~states['NAME'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]

# CONUS filter
rgeo = refinery_geo[
    (refinery_geo['Longitude'] >= -125) & (refinery_geo['Longitude'] <= -66) &
    (refinery_geo['Latitude'] >= 24) & (refinery_geo['Latitude'] <= 50)
].copy()
print(f"Refineries in CONUS: {len(rgeo)}")

REF_PALETTE = [
    '#a81e1e', '#e36414', '#11998e', '#2a6cd4', '#8f3fbd',
    '#c5a300', '#046b49', '#d13d80', '#9b1d20', '#3e4d6b',
]
ref_colors = dict(zip(top10_ref_names, REF_PALETTE))
ref_colors['other'] = '#9a9a9a'

fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
fig.patch.set_facecolor('#fafafa')
ax.set_facecolor('#fafafa')
conus_states.plot(ax=ax, color='#f0f0f0', edgecolor='#9a9a9a', linewidth=0.6, zorder=1)

for owner in ['other'] + list(reversed(top10_ref_names)):
    subset = rgeo[rgeo['owner'] == owner]
    if len(subset)==0: continue
    if owner == 'other':
        ax.scatter(subset['Longitude'], subset['Latitude'],
                   s=45, c=ref_colors[owner], alpha=0.7, zorder=2, edgecolor='white', linewidth=0.6)
    else:
        ax.scatter(subset['Longitude'], subset['Latitude'],
                   s=95, c=ref_colors[owner], alpha=0.95, zorder=3, edgecolor='white', linewidth=0.9)

ax.set_xlim(-126, -65); ax.set_ylim(23.5, 50); ax.set_aspect(1.3)
ax.set_xticks([]); ax.set_yticks([])
for spine in ax.spines.values(): spine.set_visible(False)

fig.text(0.05, 0.94, 'Where the refineries actually are',
         fontsize=22, fontweight='bold', color='#111')
fig.text(0.05, 0.905,
         f'133 US petroleum refineries, colored by parent company. Top 10 control {results["refineries"]["top10_share_pct"]:.0f}% of facilities.',
         fontsize=12.5, color='#444')

# Legend
legend_elems = []
for n in top10_ref_names:
    display = n.replace(' INC','').replace(' CORP','').replace(' LLC','').replace(' LP','').replace(' CO','').title()
    count = results['refineries']['top10'][n]
    legend_elems.append(Line2D([0],[0], marker='o', color='w',
                               markerfacecolor=ref_colors[n], markersize=11, label=f'{display}  ({count})'))
legend_elems.append(Line2D([0],[0], marker='o', color='w',
                           markerfacecolor='#9a9a9a', markersize=8, label='Other operators'))
# Legend placed BELOW the map axes so it never covers dots
leg = fig.legend(handles=legend_elems, loc='lower center', frameon=False,
                 fontsize=9.5, bbox_to_anchor=(0.5, 0.14),
                 ncol=6, columnspacing=1.2, handletextpad=0.4)

# Footer (pushed lower to clear legend)
fig.text(0.05, 0.06,
         'Source: EPA GHGRP 2023 Data Summary Spreadsheets + Parent Company Dataset. Sector: Refineries (Subpart Y).',
         fontsize=8.5, color='#666')
fig.text(0.05, 0.04,
         'Companion to phase 4b sector concentration chart.',
         fontsize=8.5, color='#666')
fig.text(0.05, 0.02,
         'Analysis: @salamituns  |  Stratdevs (Tareony)',
         fontsize=9, color='#888', style='italic')

plt.subplots_adjust(left=0.02, right=0.98, top=0.83, bottom=0.20)
OUT = f'{VIZ}/ghgrp_refineries_map_2023.png'
plt.savefig(OUT, dpi=200, bbox_inches='tight', facecolor='#fafafa')
print(f"Saved refineries map: {OUT}")
plt.close()
