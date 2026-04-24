"""
Phase 7 / Fig 09 v3 — Basin ownership personality, concentration-decay overlay.

Replaces the small-multiples top-5 bars (which muffled the story because
small basins tie across ranks) with a single-panel decay chart: one
curve per basin, share-of-basin-facilities vs parent rank, ranks 1 to 20.

The *shape* of each curve is the personality:
  - Steep left → one or two dominant parents (Appalachia, Arkla at the top)
  - Flat low  → long-tail fragmentation (Permian — 130+ parents all small)

Each curve is labeled at rank 1 with the dominant parent and its share,
so the "who" survives alongside the "shape".

Editorial palette throughout; savefig lands at 300 DPI in the site
figures directory.
"""
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import openpyxl
from pyxlsb import open_workbook
import json

GEOWORKS = '/Users/olatunde/CoWorker/Geoworks'
RAW_EPA  = f'{GEOWORKS}/data/raw/epa_ghgrp'
PROC     = f'{GEOWORKS}/ghgrp-repo/data/processed'
OUT      = f'{GEOWORKS}/salamituns.github.io/ghgrp/figures/ghgrp_basin_ownership_2023.png'

PAPER = '#F6F3EB'
INK = '#0E0E0E'
CLAY = '#A23B2A'
MUTED = '#7A7368'
FAINT = '#D9D2C4'
GHOST = '#C9C0AE'

# ---------- 1. Load upstream + midstream basin assignment ----------
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

basin_df = pd.concat([
    w_onsh[['Facility Id','Basin']],
    w_gb[['Facility Id','Basin']],
], ignore_index=True)
basin_df = basin_df.dropna(subset=['Basin']).drop_duplicates(subset=['Facility Id','Basin'])

basin_counts = basin_df.groupby('Basin')['Facility Id'].nunique().sort_values(ascending=False)
TOP_BASINS = basin_counts.head(6).index.tolist()

def pretty_basin(name):
    s = str(name)
    if ' - ' in s:
        s = s.split(' - ', 1)[1]
    s = s.replace(' Basin', '').replace(' (LA, TX)', '')
    s = s.replace('Eastern Overthrust Area', 'Eastern Overthrust')
    s = s.replace(' (Eastern)', '')
    return s.strip()

# ---------- 2. Ownership per basin ----------
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
    for s in [' INC', ' CORP', ' CORPORATION', ' LP', ' LLC', ' LTD',
              ' CO', ' PARTNERS', ' HOLDINGS', ' COMPANY']:
        n = n.replace(s, '')
    n = n.title().strip()
    fixes = {
        'Kinder Morgan': 'Kinder Morgan',
        'Enbridge (Us)': 'Enbridge',
        'Exxonmobil': 'ExxonMobil',
        'Exxon Mobil': 'ExxonMobil',
        'Eog Resources': 'EOG Resources',
        'Mplx': 'MPLX',
        'Targa Resources': 'Targa',
        'Bp Exploration': 'BP',
        'Conocophillips': 'ConocoPhillips',
        'Eqt Production': 'EQT',
        'Eqt': 'EQT',
    }
    for k, v in fixes.items():
        n = n.replace(k, v)
    # trim trailing ampersand bits
    n = n.strip(' &,.')
    # ultimate length cap
    if len(n) > 30:
        n = n[:28].rstrip() + '…'
    return n

N_RANKS = 20

results = {}
for basin in TOP_BASINS:
    basin_facility_ids = set(basin_df[basin_df['Basin']==basin]['Facility Id'])
    sp = parent[parent['GHGRP FACILITY ID'].isin(basin_facility_ids)]
    by_parent = sp.groupby('PARENT COMPANY NAME')['GHGRP FACILITY ID'].nunique().sort_values(ascending=False)
    total = len(basin_facility_ids)
    shares_series = (100 * by_parent / total).head(N_RANKS)
    # Pad to N_RANKS with NaN so shorter lists don't crash the plotter
    shares = shares_series.tolist() + [np.nan] * (N_RANKS - len(shares_series))
    results[basin] = {
        'pretty': pretty_basin(basin),
        'facility_count': total,
        'unique_parents': int(sp['PARENT COMPANY NAME'].nunique()),
        'top1_name': shorten(by_parent.index[0]),
        'top1_share_pct': float(100 * by_parent.iloc[0] / total),
        'top5_share_pct': float(100 * sp[sp['PARENT COMPANY NAME'].isin(by_parent.head(5).index)]
                                ['GHGRP FACILITY ID'].nunique() / total),
        'decay_shares': shares,
        'top5': [(shorten(n), int(c), 100*c/total)
                 for n, c in by_parent.head(5).items()],
    }

# Sort basins by top-1 share descending — concentrated first
ordered = sorted(TOP_BASINS, key=lambda b: -results[b]['top1_share_pct'])

# ---------- 3. Render: single-panel concentration-decay overlay ----------
BASIN_COLORS = {
    0: CLAY,          # most concentrated
    1: '#6B4E8A',     # VIOLET
    2: '#C57B35',     # AMBER
    3: '#3E6B5C',     # TEAL
    4: '#7A6F2B',     # OCHRE-MOSS
    5: '#5E574C',     # DEEP MUTED (most fragmented)
}

fig = plt.figure(figsize=(15, 8.6), dpi=300, facecolor=PAPER)
# Chart on the left, basin identity list on the right
ax = fig.add_axes([0.058, 0.15, 0.55, 0.68])
ax_list = fig.add_axes([0.64, 0.15, 0.34, 0.68])
ax.set_facecolor(PAPER)
ax_list.set_facecolor(PAPER)

X = np.arange(1, N_RANKS + 1)
max_y = max(results[b]['top1_share_pct'] for b in ordered)
Y_MAX = max(8.0, max_y + 1.2)

# ---- Chart curves --------------------------------------------------------
for rank_idx, basin in enumerate(ordered):
    r = results[basin]
    color = BASIN_COLORS[rank_idx]
    shares = r['decay_shares']

    ax.plot(X, shares, color=color, lw=2.4, zorder=3 + rank_idx,
            solid_capstyle='round')
    ax.scatter([1], [shares[0]], s=60, color=color,
               edgecolor=PAPER, lw=1.3, zorder=4 + rank_idx)

# ---- Axes ----------------------------------------------------------------
ax.set_xlim(0.6, N_RANKS + 0.5)
ax.set_ylim(0, Y_MAX)
ax.set_xticks([1, 5, 10, 15, 20])
ax.set_xticklabels(['Rank 1', '5', '10', '15', '20'])
ax.set_yticks([0, 2, 4, 6, 8])
ax.set_yticklabels(['0%', '2%', '4%', '6%', '8%'])
ax.tick_params(colors=INK, labelsize=10)
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['left', 'bottom']:
    ax.spines[spine].set_color(INK)
    ax.spines[spine].set_linewidth(0.6)
ax.grid(axis='y', color=INK, alpha=0.06, lw=0.5, zorder=1)
ax.set_ylabel('Share of basin facilities', color=INK, fontsize=10,
              fontfamily='sans-serif', labelpad=8)
ax.set_xlabel('Parent-company rank within basin', color=INK, fontsize=10,
              fontfamily='sans-serif', labelpad=8)

# ---- Personality callouts on the chart itself ----------------------------
r_top = results[ordered[0]]
ax.annotate(
    "Top parent owns\n1-in-16 facilities.",
    xy=(1, r_top['top1_share_pct']),
    xytext=(2.5, r_top['top1_share_pct'] + 0.9),
    color=MUTED, fontsize=9, fontfamily='sans-serif',
    arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6, alpha=0.55),
    ha='left', va='bottom',
)
r_bot = results[ordered[-1]]
ax.annotate(
    f"{r_bot['unique_parents']} parents in one basin;\nno one tops "
    f"{r_bot['top1_share_pct']:.1f}%.",
    xy=(3, r_bot['decay_shares'][2] if not np.isnan(r_bot['decay_shares'][2]) else 2.0),
    xytext=(6.5, 0.7),
    color=MUTED, fontsize=9, fontfamily='sans-serif',
    arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6, alpha=0.55),
    ha='left', va='bottom',
)

# ---- Right-side basin identity panel -------------------------------------
ax_list.set_xlim(0, 1)
ax_list.set_ylim(0, 1)
ax_list.axis('off')

n = len(ordered)
row_h = 1.0 / n
for rank_idx, basin in enumerate(ordered):
    r = results[basin]
    color = BASIN_COLORS[rank_idx]
    y_top = 1 - rank_idx * row_h
    y_cen = y_top - row_h * 0.55

    # Color swatch (thick vertical bar)
    ax_list.plot([0.01, 0.01], [y_top - row_h * 0.15, y_top - row_h * 0.85],
                 color=color, lw=4, solid_capstyle='butt', zorder=5)

    # Basin name (serif, medium)
    ax_list.text(0.06, y_top - row_h * 0.2, r['pretty'],
                 color=INK, fontsize=12.5, fontfamily='serif',
                 fontweight='medium', va='top', ha='left')
    # Top parent + share
    ax_list.text(0.06, y_top - row_h * 0.48,
                 f"Top: {r['top1_name']}  ·  {r['top1_share_pct']:.1f}%",
                 color=color, fontsize=10, fontfamily='sans-serif',
                 fontweight='medium', va='top', ha='left')
    # Meta
    ax_list.text(0.06, y_top - row_h * 0.74,
                 f"{r['facility_count']:,} facilities  ·  {r['unique_parents']} parents",
                 color=MUTED, fontsize=9, fontfamily='sans-serif',
                 va='top', ha='left')

# ---- Title & subtitle ----------------------------------------------------
fig.text(0.058, 0.935, "Every basin has its own ownership personality",
         fontsize=22, color=INK, fontfamily='serif', fontweight='medium')
fig.text(0.058, 0.887,
         "Share of 2023 basin facilities, by parent rank, top 20 parents. "
         "Steep curve = one or two parents dominate. Flat curve = long-tail fragmentation.",
         fontsize=11, color=MUTED, fontfamily='sans-serif')

# ---------- 4. Footer ----------
fig.text(0.058, 0.065,
         "Source: EPA GHGRP 2023 — Onshore Oil & Gas Production and Gathering & Boosting sheets, "
         "joined to the Parent Company dataset (any-stake rule).",
         fontsize=8.5, color=MUTED, fontfamily='sans-serif')
fig.text(0.058, 0.035,
         "Counter to sector-level concentration: at the basin level, ownership is long-tailed. "
         "Even the most concentrated basin's top parent owns under 7% of its facilities.",
         fontsize=8.5, color=MUTED, fontfamily='sans-serif')

plt.savefig(OUT, facecolor=PAPER, dpi=300)
print(f"wrote {OUT}")

# Persist the numeric summary as JSON alongside processed data
with open(f'{PROC}/phase7_basin_results.json', 'w') as f:
    json.dump({b: {**results[b], 'top5': [list(t) for t in results[b]['top5']]}
               for b in TOP_BASINS}, f, indent=2)
