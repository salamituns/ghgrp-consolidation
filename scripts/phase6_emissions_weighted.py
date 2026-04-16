"""
Phase 6 (Spin-off A) — Emissions-Weighted Concentration

Recomputes top-10 parent concentration for each sector using CO2e emissions
instead of facility counts. Shows where emissions are more or less concentrated
than facility ownership would suggest.
"""
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import openpyxl
from pyxlsb import open_workbook
import json

GEOWORKS = '/sessions/wonderful-amazing-volta/mnt/CoWorker/Geoworks'
RAW_EPA  = f'{GEOWORKS}/data/raw/epa_ghgrp'
PROC     = f'{GEOWORKS}/data/processed'
VIZ      = f'{GEOWORKS}/viz'

PATH = f'{RAW_EPA}/2023_data_summary_spreadsheets/ghgp_data_2023.xlsx'

# ---------- 1. Pull facility-level emissions from each sheet ----------
def load_sheet(wb, name):
    ws = wb[name]
    rows = list(ws.iter_rows(values_only=True))
    headers = list(rows[3])
    data = [r for r in rows[4:] if r[0] is not None]
    df = pd.DataFrame(data, columns=headers)
    # normalize emissions column name
    em_col = next((c for c in df.columns if c and str(c).startswith('Total reported')), None)
    if em_col and em_col != 'emissions':
        df = df.rename(columns={em_col: 'emissions'})
    df['emissions'] = pd.to_numeric(df['emissions'], errors='coerce').fillna(0)
    df['Facility Id'] = pd.to_numeric(df['Facility Id'], errors='coerce').astype('Int64')
    df = df[df['Facility Id'].notna()].copy()
    df['Facility Id'] = df['Facility Id'].astype(int)
    return df

wb = openpyxl.load_workbook(PATH, read_only=True, data_only=True)
dpe = load_sheet(wb, 'Direct Point Emitters')                     # 6470 rows
ws_ong = load_sheet(wb, 'Onshore Oil & Gas Prod.')
ws_gb  = load_sheet(wb, 'Gathering & Boosting')
ws_trn = load_sheet(wb, 'Transmission Pipelines')
ws_ldc = load_sheet(wb, 'LDC - Direct Emissions')
wb.close()

# Sector membership labels (same as Phase 4b)
def has_sector(s, sector):
    return sector in str(s or '').split(',')
dpe['is_power']    = dpe['Industry Type (sectors)'].apply(lambda s: has_sector(s, 'Power Plants'))
dpe['is_refinery'] = dpe['Industry Type (sectors)'].apply(lambda s: has_sector(s, 'Refineries'))
dpe['is_chem']     = dpe['Industry Type (sectors)'].apply(lambda s: has_sector(s, 'Chemicals'))

# Sector emissions aggregated to facility level
power_em     = dpe[dpe['is_power']][['Facility Id','emissions']].groupby('Facility Id', as_index=False).sum()
refinery_em  = dpe[dpe['is_refinery']][['Facility Id','emissions']].groupby('Facility Id', as_index=False).sum()
chem_em      = dpe[dpe['is_chem']][['Facility Id','emissions']].groupby('Facility Id', as_index=False).sum()

# Oil & Gas (Subpart W): combine all 5 sheets + W-PROC subset from DPE
og_parts = [ws_ong, ws_gb, ws_trn, ws_ldc]
og_ids_all = set()
og_em_frames = []
for part in og_parts:
    og_ids_all |= set(part['Facility Id'])
    og_em_frames.append(part[['Facility Id','emissions']])
# W-PROC from DPE
wproc_mask = dpe['Industry Type (subparts)'].astype(str).str.contains('W-PROC', na=False)
og_ids_all |= set(dpe[wproc_mask]['Facility Id'])
og_em_frames.append(dpe[wproc_mask][['Facility Id','emissions']])

og_em = pd.concat(og_em_frames, ignore_index=True)
# Each facility may appear in multiple subpart sheets (e.g., gas processing + transmission);
# sum reported emissions across those sheets for that facility.
og_em = og_em.groupby('Facility Id', as_index=False).sum()

print(f"Power facilities with emissions: {len(power_em)}, total emissions {power_em['emissions'].sum()/1e6:.1f} MMT CO2e")
print(f"Refineries facilities with emissions: {len(refinery_em)}, total {refinery_em['emissions'].sum()/1e6:.1f} MMT")
print(f"Chemicals facilities with emissions: {len(chem_em)}, total {chem_em['emissions'].sum()/1e6:.1f} MMT")
print(f"Oil & Gas facilities with emissions: {len(og_em)}, total {og_em['emissions'].sum()/1e6:.1f} MMT")

# ---------- 2. Load parent ownership ----------
with open_workbook(f'{RAW_EPA}/ghgp_data_parent_company.xlsb') as pwb:
    with pwb.get_sheet('2023') as sheet:
        rows = list(sheet.rows())
        headers = [c.v for c in rows[0]]
        data = [[c.v for c in r] for r in rows[1:]]
parent = pd.DataFrame(data, columns=headers)
parent = parent.dropna(subset=['GHGRP FACILITY ID','PARENT COMPANY NAME']).copy()
parent['GHGRP FACILITY ID'] = parent['GHGRP FACILITY ID'].astype(int)

# For each facility, split emissions across parents by ownership percentage
# (missing percentage → equal share across that facility's parents)
parent['pct'] = pd.to_numeric(parent['PARENT CO. PERCENT OWNERSHIP'], errors='coerce')

def split_emissions(parent_df, facility_em_df, label):
    """
    Allocate facility-level emissions to parents using ownership percentage.
    Facilities without percentage data get equal allocation across their parents.
    Returns per-parent total attributed emissions and top-10 share.
    """
    df = parent_df.merge(facility_em_df.rename(columns={'Facility Id':'GHGRP FACILITY ID'}),
                         on='GHGRP FACILITY ID', how='inner')
    # Normalize ownership pct per facility so they sum to 100
    total_pct = df.groupby('GHGRP FACILITY ID')['pct'].transform('sum')
    # If no owner has pct data, divide equally among rows
    n_rows = df.groupby('GHGRP FACILITY ID')['pct'].transform('size')
    df['share'] = df['pct'] / total_pct.replace(0, pd.NA)
    # Fallback: equal split when no pct data
    df['share'] = df['share'].fillna(1.0 / n_rows)
    df['attributed'] = df['emissions'] * df['share']

    by_parent = df.groupby('PARENT COMPANY NAME')['attributed'].sum().sort_values(ascending=False)
    total = facility_em_df['emissions'].sum()
    top10_em = by_parent.head(10).sum()
    top10_share = 100 * top10_em / total if total else 0.0
    top10 = by_parent.head(10)
    print(f"\n{label}: total {total/1e6:.1f} MMT CO2e")
    print(f"  Top-10 share (emissions-weighted): {top10_share:.1f}%")
    for n, e in top10.items():
        pct_of_total = 100 * e / total
        print(f"    {n}: {e/1e6:,.2f} MMT ({pct_of_total:.1f}%)")
    return {'label': label, 'total_emissions_MMT': total/1e6,
            'top10_share_pct': float(top10_share),
            'top10_emissions': {n: float(e) for n, e in top10.items()}}

sector_results = {}
sector_results['refineries'] = split_emissions(parent, refinery_em, 'Refineries')
sector_results['power']      = split_emissions(parent, power_em,    'Power Plants')
sector_results['petrochem']  = split_emissions(parent, chem_em,     'Petrochemicals')
sector_results['oil_gas']    = split_emissions(parent, og_em,       'Oil & Gas (Subpart W)')

# GHGRP-wide: use DPE + the subpart W sheets (unique facilities), summed across all ownership rows
all_em = pd.concat([
    dpe[['Facility Id','emissions']],
    ws_ong[['Facility Id','emissions']],
    ws_gb [['Facility Id','emissions']],
    ws_trn[['Facility Id','emissions']],
    ws_ldc[['Facility Id','emissions']],
], ignore_index=True)
all_em = all_em.groupby('Facility Id', as_index=False).sum()
sector_results['ghgrp_wide'] = split_emissions(parent, all_em, 'GHGRP-wide')

# ---------- 3. Compare to Phase 4b (facility-count share) ----------
with open(f'{PROC}/phase4b_sector_results.json') as f:
    count_based = json.load(f)

COMPARE = [
    ('refineries',  count_based['refineries']['top10_share_pct'],    sector_results['refineries']['top10_share_pct'],    'Refineries'),
    ('oil_gas',     count_based['oil_gas']['top10_share_pct'],       sector_results['oil_gas']['top10_share_pct'],       'Oil & Gas'),
    ('petrochem',   count_based['petrochem']['top10_share_pct'],     sector_results['petrochem']['top10_share_pct'],     'Petrochemicals'),
    ('power',       count_based['power']['top10_share_pct'],         sector_results['power']['top10_share_pct'],         'Power Plants'),
    ('ghgrp_wide',  count_based['ghgrp_wide']['top10_share_pct'],    sector_results['ghgrp_wide']['top10_share_pct'],    'GHGRP-wide'),
]

print("\n\nCOMPARISON — facility-count share vs emissions-weighted share:")
print(f"{'Sector':<18}  {'Count':>8}  {'Emissions':>10}  {'Delta':>8}")
for key, count_share, em_share, label in COMPARE:
    delta = em_share - count_share
    print(f"  {label:<16}  {count_share:>7.1f}%  {em_share:>9.1f}%  {delta:>+7.1f} pp")

with open(f'{PROC}/phase6_emissions_weighted_results.json', 'w') as f:
    json.dump({
        'sectors': sector_results,
        'comparison': [
            {'sector': k, 'label': l,
             'count_share_pct': cs, 'emissions_share_pct': es,
             'delta_pp': es-cs}
            for k, cs, es, l in COMPARE
        ],
    }, f, indent=2)
print(f"\nSaved: {PROC}/phase6_emissions_weighted_results.json")

# ---------- 4. Render: grouped bar comparison ----------
labels = [l for k,cs,es,l in COMPARE]
count_shares = [cs for k,cs,es,l in COMPARE]
em_shares    = [es for k,cs,es,l in COMPARE]
deltas       = [es-cs for k,cs,es,l in COMPARE]

import numpy as np
y = np.arange(len(labels))

fig, ax = plt.subplots(figsize=(14, 8), dpi=150)
fig.patch.set_facecolor('#fafafa')
ax.set_facecolor('#fafafa')

h = 0.35
bars_count = ax.barh(y - h/2, count_shares, h, color='#7a7a7a', edgecolor='white',
                    linewidth=1.2, label='By facility count (Phase 4b)')
bars_em = ax.barh(y + h/2, em_shares, h, color='#c8292c', edgecolor='white',
                 linewidth=1.2, label='By CO2e emissions weight (this phase)')

# value labels
for bar, v in zip(bars_count, count_shares):
    ax.text(v+0.5, bar.get_y()+bar.get_height()/2, f'{v:.1f}%',
            va='center', fontsize=10, color='#333')
for bar, v in zip(bars_em, em_shares):
    ax.text(v+0.5, bar.get_y()+bar.get_height()/2, f'{v:.1f}%',
            va='center', fontsize=10, color='#7a0e10', fontweight='bold')

# Delta callouts at the right side
for i, (cs, es, d) in enumerate(zip(count_shares, em_shares, deltas)):
    arrow_x = max(cs, es) + 12
    sign = '+' if d > 0 else ''
    color = '#0a6b2a' if d > 0 else '#b02020'
    ax.text(arrow_x, i, f'{sign}{d:.1f} pp',
            va='center', fontsize=11, fontweight='bold', color=color)

ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=12, color='#222')
ax.invert_yaxis()
ax.set_xlim(0, 105)
ax.set_xlabel('Top-10 parent share of sector (%)', fontsize=11, color='#333', labelpad=10)
ax.tick_params(axis='x', labelsize=10, colors='#555')
for spine in ['top','right']: ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#bbb'); ax.spines['bottom'].set_color('#bbb')

# Title
fig.text(0.05, 0.955, 'When you weight by emissions, the story shifts',
         fontsize=22, fontweight='bold', color='#111')
fig.text(0.05, 0.915,
         'Refineries: already extreme by count, even more extreme by emissions. Oil & gas: count concentration hides emissions concentration.',
         fontsize=11, color='#444')

# Legend below
fig.legend(loc='lower center', frameon=False, fontsize=10.5,
           bbox_to_anchor=(0.5, 0.12), ncol=2, columnspacing=3.0, handletextpad=0.6)

# Footer
fig.text(0.05, 0.07,
         'Source: EPA GHGRP 2023 Data Summary Spreadsheets + Parent Company Dataset. Emissions = Total reported direct emissions (CO2e, metric tons).',
         fontsize=8.5, color='#666')
fig.text(0.05, 0.05,
         'Method: facility emissions are allocated across parents by reported ownership percentage (equal-split fallback when percentages are null). Top-10 parents per sector then summed.',
         fontsize=8.5, color='#666')
fig.text(0.05, 0.03,
         'Companion to Phase 4b. Facility-count shares are the Phase 4b any-stake-union numbers; emissions-weighted shares use ownership-weighted allocation.',
         fontsize=8.5, color='#666')
fig.text(0.05, 0.01,
         'Analysis: @salamituns  |  Stratdevs (Tareony)',
         fontsize=9, color='#888', style='italic')

plt.subplots_adjust(left=0.12, right=0.97, top=0.87, bottom=0.18)
OUT = f'{VIZ}/ghgrp_emissions_weighted_2023.png'
plt.savefig(OUT, dpi=200, bbox_inches='tight', facecolor='#fafafa')
print(f"\nSaved: {OUT}")
plt.close()
