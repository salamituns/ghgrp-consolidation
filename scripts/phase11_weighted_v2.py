"""
Phase 11 / Fig 10 v2: Count-weighted vs emissions-weighted concentration.

Structure preserved (paired bars: facility-count share vs CO2e-weighted share
per sector): only palette/typography swap. Emissions-weighted bars in CLAY,
count-weighted reference bars in MUTED/GHOST. Delta annotations shift from
"green +pp" noise to CLAY italic, matching the editorial stack.
"""
import warnings
warnings.filterwarnings('ignore')

import json
import numpy as np
import matplotlib.pyplot as plt

WEIGHTED = '/Users/olatunde/CoWorker/Geoworks/ghgrp-repo/data/processed/phase6_emissions_weighted_results.json'
SECTOR   = '/Users/olatunde/CoWorker/Geoworks/ghgrp-repo/data/processed/phase4b_sector_results.json'
OUT = '/Users/olatunde/CoWorker/Geoworks/salamituns.github.io/ghgrp/figures/ghgrp_emissions_weighted_2023.png'

PAPER = '#F6F3EB'
INK = '#0E0E0E'
CLAY = '#A23B2A'
MUTED = '#7A7368'
FAINT = '#D9D2C4'
GHOST = '#C9C0AE'

with open(WEIGHTED) as f:
    w = json.load(f)['sectors']
with open(SECTOR) as f:
    c = json.load(f)

order = ['refineries', 'oil_gas', 'petrochem', 'power', 'ghgrp_wide']
labels = [c[k]['label'] for k in order]
count_share = [c[k]['top10_share_pct'] for k in order]
# oil_gas label mismatch between files; fall back to w's value
emis_share  = [w[k]['top10_share_pct'] for k in order]
deltas = [e - c_ for e, c_ in zip(emis_share, count_share)]

fig, ax = plt.subplots(figsize=(13, 6.4), dpi=300, facecolor=PAPER)
ax.set_facecolor(PAPER)

y = np.arange(len(labels))
bar_h = 0.35
ax.barh(y - bar_h/2, count_share, height=bar_h, color=GHOST, zorder=3,
        label='By facility count (Fig 08)')
ax.barh(y + bar_h/2, emis_share, height=bar_h, color=CLAY, zorder=3,
        label='By CO₂e emissions (weighted)')

# Value labels on each bar
for i, (ec, ee, d) in enumerate(zip(count_share, emis_share, deltas)):
    ax.text(ec + 0.8, i - bar_h/2, f'{ec:.1f}%', va='center', ha='left',
            fontsize=9.5, color=MUTED, fontfamily='sans-serif')
    ax.text(ee + 0.8, i + bar_h/2, f'{ee:.1f}%', va='center', ha='left',
            fontsize=10.5, color=INK, fontfamily='serif', fontweight='medium')
    # Shift delta
    sign = '+' if d > 0 else ''
    ax.text(max(ec, ee) + 11, i, f'{sign}{d:.1f} pp',
            va='center', ha='left', fontsize=10, color=CLAY,
            fontfamily='sans-serif', fontstyle='italic', fontweight='medium')

ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=11, color=INK)
for label in ax.get_yticklabels():
    label.set_fontfamily('sans-serif')
ax.invert_yaxis()
ax.set_xlim(0, 100)
ax.set_xticks([0, 20, 40, 60, 80, 100])
ax.set_xticklabels(['0%', '20%', '40%', '60%', '80%', '100%'])
ax.tick_params(axis='x', labelsize=9, colors=MUTED, length=0, pad=4)
for label in ax.get_xticklabels():
    label.set_fontfamily('sans-serif')
ax.tick_params(axis='y', length=0)
for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color(FAINT); ax.spines['bottom'].set_linewidth(0.6)
ax.set_xlabel('Top 10 parent share of sector', fontsize=9.5, color=MUTED,
              fontfamily='sans-serif', labelpad=8)
ax.grid(axis='x', linestyle='-', alpha=0.4, color=FAINT, zorder=0)

# Legend
from matplotlib.patches import Patch
leg = ax.legend(
    handles=[
        Patch(facecolor=CLAY, label='By CO₂e emissions (weighted)'),
        Patch(facecolor=GHOST, label='By facility count'),
    ],
    loc='lower right', frameon=False, fontsize=9.5, labelcolor=INK,
)
for t in leg.get_texts():
    t.set_fontfamily('sans-serif')

# Title
fig.text(0.035, 0.955,
         "Weight by emissions, and the story shifts.",
         fontsize=20, color=INK, fontfamily='serif', fontweight='medium')
fig.text(0.035, 0.915,
         "Refineries were already extreme by count (54%); by CO₂e they're near-monopolistic (80%). "
         "Petrochemicals double. Power plants gain 12pp. In every sector, the top 10 emit more than they count.",
         fontsize=10.5, color=MUTED, fontfamily='sans-serif')

fig.text(0.035, 0.025,
         "Source: EPA GHGRP 2023 Parent Company dataset + Data Summary Spreadsheets.  "
         "Emissions = Total reported direct emissions (CO₂e, metric tons), allocated across parents "
         "by reported ownership percentage (equal-split fallback where null).  "
         "Analysis: @salamituns.",
         fontsize=8, color=MUTED, fontfamily='sans-serif')

plt.subplots_adjust(left=0.13, right=0.97, top=0.85, bottom=0.12)
plt.savefig(OUT, facecolor=PAPER, dpi=300, bbox_inches='tight')
print(f"wrote {OUT}")
