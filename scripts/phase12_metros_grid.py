"""
Phase 12 / Fig 14: Four metros, four consolidation stories.

2x2 grid of GHGRP 2023 facilities in the four regions where consolidation
is most load-bearing:

  Houston          : corporate control node; dense KM/ET footprint
  Permian Basin    : shale frontier; thousands of Subpart W reporters added
  Cancer Alley     : petrochemical corridor between Baton Rouge and New Orleans
  Appalachia       : Marcellus gas shale build-out (PA, WV, OH, NY southern tier)

Same facility classification as Fig 07 (KM, ET, JV, other) so the national
corridor story extends into four zoomed lenses in the same visual language.
"""
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec
from pyxlsb import open_workbook

GEO = '/Users/olatunde/CoWorker/Geoworks/ghgrp-repo/data/processed/ghgrp_2023_geo.csv'
RAW_XLSB = '/Users/olatunde/CoWorker/Geoworks/data/raw/epa_ghgrp/ghgp_data_parent_company.xlsb'
STATES = '/Users/olatunde/CoWorker/Geoworks/data/raw/census_boundaries/gz_2010_us_040_00_5m.json'
OUT = '/Users/olatunde/CoWorker/Geoworks/salamituns.github.io/ghgrp/figures/ghgrp_four_metros_grid.png'

PAPER = '#F6F3EB'
INK = '#0E0E0E'
CLAY = '#A23B2A'
AMBER = '#C57B35'
VIOLET = '#6B4E8A'
MUTED = '#7A7368'
FAINT = '#D9D2C4'
GHOST = '#9E9689'

# ---- Load facility geo + classify by 2023 parent -------------------------
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

# ---- States geometry -----------------------------------------------------
states_gdf = gpd.read_file(STATES)
states_gdf = states_gdf[~states_gdf['NAME'].isin(['Alaska', 'Hawaii', 'Puerto Rico'])]

# ---- Metro definitions ---------------------------------------------------
# (title, thesis, (west, east, south, north), fontsize-tweak)
METROS = [
    {
        'key': 'houston',
        'title': 'Houston',
        'thesis': 'The control node.',
        'bbox': (-96.2, -94.4, 29.1, 30.4),
        'aspect': 1.15,
    },
    {
        'key': 'permian',
        'title': 'Permian Basin',
        'thesis': 'The shale frontier.',
        'bbox': (-104.2, -100.5, 30.8, 33.6),
        'aspect': 1.2,
    },
    {
        'key': 'cancer_alley',
        'title': 'Cancer Alley',
        'thesis': 'The petrochemical corridor.',
        'bbox': (-91.8, -89.6, 29.7, 30.8),
        'aspect': 1.15,
    },
    {
        'key': 'appalachia',
        'title': 'Marcellus',
        'thesis': 'The gas-shale build-out.',
        'bbox': (-82.5, -75.5, 38.0, 42.8),
        'aspect': 1.35,
    },
]

for m in METROS:
    w, e, s, n = m['bbox']
    sub = geo[(geo['Longitude'] >= w) & (geo['Longitude'] <= e) &
             (geo['Latitude'] >= s) & (geo['Latitude'] <= n)].copy()
    m['facilities'] = sub
    m['n_total'] = len(sub)
    m['n_km'] = (sub['class'] == 'km').sum()
    m['n_et'] = (sub['class'] == 'et').sum()
    m['n_jv'] = (sub['class'] == 'jv').sum()
    print(f"{m['title']:15s} : total {m['n_total']}, KM {m['n_km']}, ET {m['n_et']}, JV {m['n_jv']}")

# ---- Render --------------------------------------------------------------
fig = plt.figure(figsize=(14, 9.2), dpi=300, facecolor=PAPER)
gs = GridSpec(2, 2, figure=fig, left=0.03, right=0.97, top=0.80, bottom=0.10,
              wspace=0.08, hspace=0.20)

for i, m in enumerate(METROS):
    row, col = divmod(i, 2)
    ax = fig.add_subplot(gs[row, col])
    ax.set_facecolor(PAPER)

    w, e, s, n = m['bbox']

    # State outlines, clipped to bbox by setting xlim/ylim
    states_gdf.plot(ax=ax, color=FAINT, edgecolor=INK, linewidth=0.4,
                    zorder=1, alpha=0.80)

    sub = m['facilities']
    others = sub[sub['class'] == 'other']
    et = sub[sub['class'] == 'et']
    km = sub[sub['class'] == 'km']
    jv = sub[sub['class'] == 'jv']

    ax.scatter(others['Longitude'], others['Latitude'],
               s=5, c=GHOST, alpha=0.32, linewidth=0, zorder=2, marker='o')
    ax.scatter(et['Longitude'], et['Latitude'],
               s=22, facecolor=AMBER, edgecolor=PAPER, linewidth=0.5,
               alpha=0.92, zorder=4, marker='o')
    ax.scatter(km['Longitude'], km['Latitude'],
               s=22, facecolor=CLAY, edgecolor=PAPER, linewidth=0.5,
               alpha=0.95, zorder=5, marker='o')
    ax.scatter(jv['Longitude'], jv['Latitude'],
               s=50, facecolor=VIOLET, edgecolor=PAPER, linewidth=0.8,
               alpha=0.98, zorder=6, marker='D')

    ax.set_xlim(w, e)
    ax.set_ylim(s, n)
    ax.set_aspect(m['aspect'])
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color(FAINT); sp.set_linewidth(0.6)

    # Panel title block (inside axes, top-left)
    ax.text(0.025, 0.955, m['title'],
            transform=ax.transAxes, fontsize=15, color=INK,
            fontfamily='serif', fontweight='medium', va='top')
    ax.text(0.025, 0.885, m['thesis'],
            transform=ax.transAxes, fontsize=10.5, color=MUTED,
            fontfamily='sans-serif', fontstyle='italic', va='top')

    # Stat callout (inside axes, bottom-right)
    stat_lines = [
        f"{m['n_total']:,} total reporters",
    ]
    owned_bits = []
    if m['n_km']: owned_bits.append(f"{m['n_km']} KM")
    if m['n_et']: owned_bits.append(f"{m['n_et']} ET")
    if m['n_jv']: owned_bits.append(f"{m['n_jv']} JV")
    if owned_bits:
        stat_lines.append(' · '.join(owned_bits))
    ax.text(0.975, 0.04, '\n'.join(stat_lines),
            transform=ax.transAxes, fontsize=9, color=INK,
            fontfamily='sans-serif', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.35', facecolor=PAPER,
                      edgecolor=FAINT, linewidth=0.6, alpha=0.92))

# ---- Title block ---------------------------------------------------------
fig.text(0.03, 0.955,
         "Four metros, four versions of the same consolidation.",
         fontsize=19, color=INK, fontfamily='serif', fontweight='medium')
fig.text(0.03, 0.915,
         "The national aggregate is one number. On the ground it is four different stories: "
         "a control node, a shale frontier, a petrochemical corridor, and a gas-shale build-out.",
         fontsize=10.5, color=MUTED, fontfamily='sans-serif')

# ---- Shared legend -------------------------------------------------------
legend_handles = [
    Line2D([0],[0], marker='o', color='w', markerfacecolor=CLAY,
           markeredgecolor=PAPER, markersize=8, label='Kinder Morgan'),
    Line2D([0],[0], marker='o', color='w', markerfacecolor=AMBER,
           markeredgecolor=PAPER, markersize=8, label='Energy Transfer'),
    Line2D([0],[0], marker='D', color='w', markerfacecolor=VIOLET,
           markeredgecolor=PAPER, markersize=8, label='KM + ET joint venture'),
    Line2D([0],[0], marker='o', color='w', markerfacecolor=GHOST,
           markeredgecolor='none', markersize=6, alpha=0.6,
           label='Other GHGRP reporters'),
]
leg = fig.legend(handles=legend_handles, loc='lower center', frameon=False,
                 fontsize=9.5, labelcolor=INK, bbox_to_anchor=(0.5, 0.055),
                 ncol=4, columnspacing=2.0, handletextpad=0.6)
for t in leg.get_texts():
    t.set_fontfamily('sans-serif')

# ---- Footer --------------------------------------------------------------
fig.text(0.03, 0.025,
         "Source: EPA GHGRP 2023 facility panel + Parent Company dataset (any-stake union per facility).  "
         "State outlines: Census 2010 5m cartographic.  "
         "Classification matches Figure 07.  "
         "Analysis: @salamituns.",
         fontsize=8, color=MUTED, fontfamily='sans-serif')

plt.savefig(OUT, facecolor=PAPER, dpi=300, bbox_inches='tight')
print(f'\nwrote {OUT}')
