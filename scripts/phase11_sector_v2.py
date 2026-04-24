"""
Phase 11 / Fig 08 v2: Sector concentration, editorial palette.

Reads phase4b_sector_results.json. Refineries anchor the narrative (54.1%
vs 16.7% GHGRP-wide), so Refineries gets the CLAY accent; other sectors
sit in a shaded ink hierarchy.
"""
import warnings
warnings.filterwarnings('ignore')

import json
import numpy as np
import matplotlib.pyplot as plt

SRC = '/Users/olatunde/CoWorker/Geoworks/ghgrp-repo/data/processed/phase4b_sector_results.json'
OUT = '/Users/olatunde/CoWorker/Geoworks/salamituns.github.io/ghgrp/figures/ghgrp_sector_concentration_2023.png'

PAPER = '#F6F3EB'
INK = '#0E0E0E'
CLAY = '#A23B2A'
MUTED = '#7A7368'
FAINT = '#D9D2C4'
SLATE = '#3C5069'

with open(SRC) as f:
    sectors = json.load(f)

# Ordered: Refineries first (clay anchor), then other extractives, then ghgrp baseline
order = ['refineries', 'oil_gas', 'petrochem', 'power', 'ghgrp_wide']
rows = [(sectors[k]['label'], sectors[k]['top10_share_pct'], sectors[k]['total_facilities']) for k in order]

fig, ax = plt.subplots(figsize=(13, 5.8), dpi=300, facecolor=PAPER)
ax.set_facecolor(PAPER)

labels = [r[0] for r in rows]
values = [r[1] for r in rows]
counts = [r[2] for r in rows]
colors = [CLAY, SLATE, SLATE, SLATE, MUTED]
alphas = [1.0, 0.78, 0.66, 0.54, 0.9]

y = np.arange(len(rows))
for i, (v, c, a) in enumerate(zip(values, colors, alphas)):
    ax.barh(y[i], v, height=0.66, color=c, alpha=a, zorder=3)

# Baseline rule at 16.7% (GHGRP-wide): vertical FAINT line for reference
baseline = sectors['ghgrp_wide']['top10_share_pct']
ax.axvline(baseline, color=MUTED, linestyle='--', linewidth=0.8, alpha=0.6, zorder=2)
ax.text(baseline, -0.68, f'GHGRP-wide\n{baseline:.1f}%', fontsize=8, color=MUTED,
        ha='center', va='top', fontfamily='sans-serif', fontstyle='italic')

# Direct value + count labels
for i, (v, cnt) in enumerate(zip(values, counts)):
    ax.text(v + 0.8, i, f'{v:.1f}%', va='center', ha='left',
            fontsize=12, color=INK, fontfamily='serif', fontweight='medium')
    ax.text(v + 7.5, i, f'({cnt:,} facilities)', va='center', ha='left',
            fontsize=9, color=MUTED, fontfamily='sans-serif')

ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=11, color=INK)
for label in ax.get_yticklabels():
    label.set_fontfamily('sans-serif')
ax.invert_yaxis()
ax.set_xlim(0, 70)
ax.set_xticks([0, 10, 20, 30, 40, 50, 60])
ax.set_xticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%'])
ax.tick_params(axis='x', labelsize=9, colors=MUTED, length=0, pad=6)
for label in ax.get_xticklabels():
    label.set_fontfamily('sans-serif')
ax.tick_params(axis='y', length=0)
for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color(FAINT); ax.spines['bottom'].set_linewidth(0.6)
ax.set_xlabel('Share of sector facilities held by top 10 parents', fontsize=9.5, color=MUTED,
              fontfamily='sans-serif', labelpad=8)
ax.grid(axis='x', linestyle='-', alpha=0.4, color=FAINT, zorder=0)

# Title block
fig.text(0.035, 0.955,
         "Not every sector consolidates the same way.",
         fontsize=20, color=INK, fontfamily='serif', fontweight='medium')
fig.text(0.035, 0.905,
         "US petroleum refineries are 3.2× more concentrated than the full GHGRP. "
         "Power plants (the most facility-count-heavy sector) are the least consolidated.",
         fontsize=10.5, color=MUTED, fontfamily='sans-serif')

fig.text(0.035, 0.025,
         "Source: EPA GHGRP 2023 Parent Company dataset + Data Summary Spreadsheets.  "
         "Sector classification: Refineries = Subpart Y; Petrochemicals = Subpart X; "
         "Oil & Gas = Subpart W; Power Plants = Subpart D (Power).  "
         "Analysis: @salamituns.",
         fontsize=8, color=MUTED, fontfamily='sans-serif')

plt.subplots_adjust(left=0.14, right=0.97, top=0.85, bottom=0.17)
plt.savefig(OUT, facecolor=PAPER, dpi=300, bbox_inches='tight')
print(f"wrote {OUT}")
