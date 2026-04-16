"""
Phase 7 (Spin-off B) — Basin-Level Oil & Gas Operator Concentration

For each of the top 6 US basins, compute who dominates ownership at the
facility level. Shows that different basins have distinctly different
ownership structures — Permian is multi-operator, Appalachia is narrower,
Anadarko leans midstream.
"""
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import openpyxl
from pyxlsb import open_workbook
import json

GEOWORKS = '/sessions/wonderful-amazing-volta/mnt/CoWorker/Geoworks'
RAW_EPA  = f'{GEOWORKS}/data/raw/epa_ghgrp'
PROC     = f'{GEOWORKS}/data/processed'
VIZ      = f'{GEOWORKS}/viz'

# ---------- 1. Load upstream + midstream + shortlist of basins ----------
PATH = f'{RAW_EPA}/2023_data_summary_spreadsheets/ghgp_data_2023.xlsx'
wb = openpyxl.load_workbook(PATH, read_only=True, data_only=True)

def load_sheet(name):
    ws = wb[name]
    rows = list(ws.iter_rows(values_only=True))
    headers = list(rows[3])
    data = [r for r in rows[4:] if r[0] is not None]
    df = pd.DataFrame(data, columns=headers)
    df['Facility Id'] = pd.to_numeric(df['Facility Id'], errors='coerce').astype('Int64')
    df = df[df['Facility Id'].notna()].copy()
    df['Facility Id'] = df['Facility Id'].astype(int)
    return df

w_onsh = load_sheet('Onshore Oil & Gas Prod.')
w_gb   = load_sheet('Gathering & Boosting')
wb.close()

w_onsh['segment'] = 'Upstream (onshore production)'
w_gb['segment']   = 'Midstream (gathering & boosting)'
basin_df = pd.concat([
    w_onsh[['Facility Id','Basin','segment']],
    w_gb[['Facility Id','Basin','segment']],
], ignore_index=True)
basin_df = basin_df.dropna(subset=['Basin']).drop_duplicates(subset=['Facility Id','Basin'])

# ---------- 2. Select top N basins by combined facility count ----------
basin_counts = basin_df.groupby('Basin')['Facility Id'].nunique().sort_values(ascending=False)
print("Top 10 basins by facility count (upstream + midstream combined):")
print(basin_counts.head(10).to_string())

TOP_BASINS = basin_counts.head(6).index.tolist()
# Clean up names for display
def pretty_basin(name):
    # 430 - Permian Basin -> Permian
    s = str(name)
    if ' - ' in s:
        s = s.split(' - ', 1)[1]
    s = s.replace(' Basin', '').replace(' (LA, TX)', '').replace('Eastern Overthrust Area', 'Eastern').replace(' (Eastern)', '')
    return s.strip()

basin_pretty = {b: pretty_basin(b) for b in TOP_BASINS}
print(f"\nFocus basins (pretty names): {list(basin_pretty.values())}")

# ---------- 3. Ownership analysis per basin ----------
with open_workbook(f'{RAW_EPA}/ghgp_data_parent_company.xlsb') as pwb:
    with pwb.get_sheet('2023') as sheet:
        rows = list(sheet.rows())
        headers = [c.v for c in rows[0]]
        data = [[c.v for c in r] for r in rows[1:]]
parent = pd.DataFrame(data, columns=headers)
parent = parent.dropna(subset=['GHGRP FACILITY ID','PARENT COMPANY NAME']).copy()
parent['GHGRP FACILITY ID'] = parent['GHGRP FACILITY ID'].astype(int)

def shorten(name):
    n = str(name)
    n = n.replace(' INC','').replace(' CORP','').replace(' CORPORATION','')
    n = n.replace(' LP','').replace(' LLC','').replace(' LTD','').replace(' CO','')
    n = n.replace('PARTNERS','').replace(' HOLDINGS','')
    n = n.title().strip()
    # Special cases
    n = n.replace('Kinder Morgan', 'Kinder Morgan').replace('Enbridge (Us)', 'Enbridge')
    n = n.replace('Exxonmobil', 'ExxonMobil').replace('Exxon Mobil', 'ExxonMobil')
    n = n.replace('Eog Resources', 'EOG Resources')
    n = n.replace('Mplx', 'MPLX')
    n = n.replace('Targa Resources', 'Targa')
    n = n.replace('Bp Exploration', 'BP')
    n = n.replace('Conocophillips', 'ConocoPhillips')
    return n

basin_top_operators = {}
for basin in TOP_BASINS:
    basin_facility_ids = set(basin_df[basin_df['Basin']==basin]['Facility Id'])
    sp = parent[parent['GHGRP FACILITY ID'].isin(basin_facility_ids)]
    # count unique facilities per parent (any-stake rule)
    by_parent = sp.groupby('PARENT COMPANY NAME')['GHGRP FACILITY ID'].nunique().sort_values(ascending=False)
    basin_top_operators[basin] = {
        'pretty': pretty_basin(basin),
        'facility_count': len(basin_facility_ids),
        'unique_parents': sp['PARENT COMPANY NAME'].nunique(),
        'top5': {shorten(n): int(c) for n,c in by_parent.head(5).items()},
        'top1_share_pct': float(100 * by_parent.iloc[0] / len(basin_facility_ids)),
        'top5_share_pct': float(100 * sp[sp['PARENT COMPANY NAME'].isin(by_parent.head(5).index)]
                                ['GHGRP FACILITY ID'].nunique() / len(basin_facility_ids)),
    }

# Print summary
print("\n" + "="*90)
print(f"{'Basin':<22} {'Facilities':>10} {'Parents':>8} {'Top-1 share':>12} {'Top-5 share':>12}")
print("="*90)
for basin in TOP_BASINS:
    r = basin_top_operators[basin]
    print(f"{r['pretty']:<22} {r['facility_count']:>10} {r['unique_parents']:>8}  {r['top1_share_pct']:>10.1f}%  {r['top5_share_pct']:>10.1f}%")

# Save
with open(f'{PROC}/phase7_basin_results.json', 'w') as f:
    json.dump({b: basin_top_operators[b] for b in TOP_BASINS}, f, indent=2)
print(f"\nSaved: {PROC}/phase7_basin_results.json")

# ---------- 4. Render: stacked 100% bars per basin, top 5 + other ----------
# Collect all top-5 operator names across basins for a consistent palette (with color cycling)
all_names = set()
for b in TOP_BASINS:
    all_names.update(basin_top_operators[b]['top5'].keys())
all_names = sorted(all_names)
print(f"\nUnique top-5 operators across focus basins: {len(all_names)}")
print(all_names)

# Assign a color per operator
import matplotlib.cm as cm
palette = [
    '#c8292c','#ff8b2a','#11998e','#2a6cd4','#8f3fbd',
    '#c5a300','#046b49','#d13d80','#9b1d20','#3e4d6b',
    '#0a6b2a','#b02020','#5e72a0','#a84d06','#2a4d22',
    '#7a2066','#135c91','#b96c2e','#4a1a6e','#8c9c46',
]
op_color = {}
for i, n in enumerate(all_names):
    op_color[n] = palette[i % len(palette)]
op_color['Other'] = '#bbbbbb'

# Build stacked bar data — each basin gets TWO rows: the bar on the top row and
# the top-5 operator list in small text on the bottom row.
fig, ax = plt.subplots(figsize=(15, 10), dpi=150)
fig.patch.set_facecolor('#fafafa')
ax.set_facecolor('#fafafa')

basin_labels = [basin_top_operators[b]['pretty'] for b in TOP_BASINS]
# Vertical positions: each basin gets a slot of 1.0 unit; bar at y and annotation at y+0.38
y = np.arange(len(TOP_BASINS)) * 1.0

for i, basin in enumerate(TOP_BASINS):
    r = basin_top_operators[basin]
    total = r['facility_count']
    cumulative = 0
    # Plot each top-5 operator as a colored segment
    for name, count in r['top5'].items():
        pct = 100 * count / total
        ax.barh(y[i], pct, left=cumulative, color=op_color[name], edgecolor='white',
                linewidth=1.3, height=0.48)
        cumulative += pct
    # "Other" grey segment
    other_pct = 100 - r['top5_share_pct']
    if other_pct > 0:
        ax.barh(y[i], other_pct, left=cumulative, color=op_color['Other'],
                edgecolor='white', linewidth=1.3, height=0.48)
        # Label the "other" segment with parent count
        if other_pct >= 15:
            ax.text(cumulative + other_pct/2, y[i],
                    f'Remaining {r["unique_parents"]-5} parents share this',
                    ha='center', va='center', fontsize=9, color='#555', style='italic')
    # Right-side metadata
    ax.text(102, y[i], f'Top 5 = {r["top5_share_pct"]:.0f}%  •  {r["facility_count"]} facilities  •  {r["unique_parents"]} total parents',
            va='center', fontsize=10, color='#333')
    # BELOW each bar: the top-5 operator names with exact shares
    # Build a colored-swatch inline text. Since matplotlib can't inline colored swatches in one
    # text call cleanly, we place small colored rectangles + text next to each other.
    x_cursor = 0.0
    for idx, (name, count) in enumerate(r['top5'].items()):
        pct = 100 * count / total
        # Small colored dot (drawn as a scatter point at the text baseline)
        ax.scatter(x_cursor + 1.5, y[i] + 0.42, s=45, marker='s',
                   color=op_color[name], edgecolor='white', linewidth=0.6, zorder=5)
        label = f'  {name} ({pct:.1f}%)'
        txt = ax.text(x_cursor + 2.8, y[i] + 0.42, label,
                      va='center', fontsize=9, color='#222')
        # Advance cursor by approximate text width
        x_cursor += 4.0 + len(label) * 0.9

ax.set_yticks(y)
ax.set_yticklabels(basin_labels, fontsize=14, color='#222', fontweight='bold')
ax.invert_yaxis()
ax.set_xlim(0, 100)
ax.set_ylim(y[-1] + 0.8, y[0] - 0.6)  # extra headroom for annotation text below each bar
ax.set_xlabel('Share of basin facilities, by parent company', fontsize=11, color='#333', labelpad=10)
ax.tick_params(axis='x', labelsize=10, colors='#555')
for spine in ['top','right','left','bottom']:
    ax.spines[spine].set_visible(False)
ax.tick_params(axis='y', length=0)
# percent ticks only 0, 25, 50, 75, 100
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(['0%','25%','50%','75%','100%'])

# Title
fig.text(0.05, 0.945, 'Each basin has its own ownership personality',
         fontsize=22, fontweight='bold', color='#111')
fig.text(0.05, 0.910,
         'Top 5 parent companies per basin. Upstream production + gathering & boosting combined.',
         fontsize=11, color='#444')

# Footer
fig.text(0.05, 0.07,
         'Source: EPA GHGRP 2023 — Onshore Oil & Gas Prod. + Gathering & Boosting sheets; Parent Company Dataset. Basin boundaries use EPA\'s reporting-basin classification.',
         fontsize=8.5, color='#666')
fig.text(0.05, 0.05,
         'Concentration metric: share of unique facilities in basin owned (any stake) by top-5 parent companies for that basin. Each basin\'s bar sums to 100%.',
         fontsize=8.5, color='#666')
fig.text(0.05, 0.03,
         'Counter-finding to Phase 4a: at the basin level, ownership is much more fragmented than at the sector level. Permian has 130 parents, top-1 controls only 3.2%. Every focus basin shows long tail of small operators.',
         fontsize=8.5, color='#666')
fig.text(0.05, 0.01,
         'Analysis: @salamituns  |  Stratdevs (Tareony)',
         fontsize=9, color='#888', style='italic')

# Right margin extended for metadata; top/bottom for title + footer
plt.subplots_adjust(left=0.13, right=0.76, top=0.90, bottom=0.12)

OUT = f'{VIZ}/ghgrp_basin_ownership_2023.png'
plt.savefig(OUT, dpi=200, bbox_inches='tight', facecolor='#fafafa')
print(f"\nSaved: {OUT}")
plt.close()
