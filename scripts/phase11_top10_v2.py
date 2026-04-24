"""
Phase 11 / Fig 05 v2: Top 10 parent companies, 2010 vs 2023.

Editorial palette repaint. Same horizontal-bar structure (2010 ghost + 2023
primary) but in CLAY/MUTED, direct value labels, Fraunces serif title.
"""
import warnings
warnings.filterwarnings('ignore')

import json
import numpy as np
import matplotlib.pyplot as plt

SUMMARY = '/Users/olatunde/CoWorker/Geoworks/ghgrp-repo/data/processed/phase5_comparison_summary.json'
OUT = '/Users/olatunde/CoWorker/Geoworks/salamituns.github.io/ghgrp/figures/ghgrp_top10_barchart.png'

PAPER = '#F6F3EB'
INK = '#0E0E0E'
CLAY = '#A23B2A'
MUTED = '#7A7368'
FAINT = '#D9D2C4'
GHOST = '#C9C0AE'

with open(SUMMARY) as f:
    summary = json.load(f)
top10_share = summary['recomputed_2023_pct']  # 16.74

# Top 10 facility counts (from Phase 5 "Top 10 Trend")
data = [
    ('Waste Management',   265, 277),
    ('Kinder Morgan',      231,  24),
    ('Energy Transfer',    184,  19),
    ('Republic Services',  177, 194),
    ('Berkshire Hathaway', 131,  36),
    ('TC Energy',          116,  36),
    ('Enbridge',           110,  26),
    ('US Government',       85,  61),
    ('Williams Cos',        82,  72),
    ('Enterprise Products', 75,  35),
]
data = sorted(data, key=lambda x: x[1], reverse=True)
names = [d[0] for d in data]
v2023 = [d[1] for d in data]
v2010 = [d[2] for d in data]
deltas = [a - b for a, b in zip(v2023, v2010)]

fig, ax = plt.subplots(figsize=(13, 6.4), dpi=300, facecolor=PAPER)
ax.set_facecolor(PAPER)

y = np.arange(len(names))
ax.barh(y, v2010, color=GHOST, alpha=0.85, height=0.62, zorder=2, label='2010')
ax.barh(y, v2023, color=CLAY, height=0.42, zorder=3, label='2023')

ax.set_yticks(y)
ax.set_yticklabels(names, fontsize=10.5, color=INK)
for label in ax.get_yticklabels():
    label.set_fontfamily('sans-serif')
ax.invert_yaxis()
ax.set_xlim(0, max(v2023 + v2010) * 1.42)
ax.set_xlabel('GHGRP reporting facilities (2023)', fontsize=9.5, color=MUTED,
              fontfamily='sans-serif', labelpad=8)
ax.tick_params(axis='x', labelsize=9, colors=MUTED, length=0, pad=4)
for label in ax.get_xticklabels():
    label.set_fontfamily('sans-serif')
for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color(FAINT); ax.spines['bottom'].set_linewidth(0.6)
ax.tick_params(axis='y', length=0)
ax.grid(axis='x', linestyle='-', alpha=0.4, color=FAINT, zorder=0)

# Direct labels: 2023 value + delta vs 2010
for i, (v, d) in enumerate(zip(v2023, deltas)):
    ax.text(v + 5, i, f'{v}', va='center', ha='left',
            fontsize=10.5, color=INK, fontfamily='serif', fontweight='medium')
    sign = f'+{d}' if d > 0 else f'{d}'
    col = CLAY if d > 0 else MUTED
    ax.text(v + 46, i, f'{sign} vs 2010', va='center', ha='left',
            fontsize=9, color=col, fontfamily='sans-serif', fontstyle='italic')

# Title block
fig.text(0.035, 0.955,
         f"The top ten now hold {top10_share:.1f}% of reporters.",
         fontsize=20, color=INK, fontfamily='serif', fontweight='medium')
fig.text(0.035, 0.915,
         "Facility counts by parent company, 2010 vs 2023. Pipeline operators (Kinder Morgan, Energy Transfer, TC Energy, Enbridge, Williams, Enterprise) dominate the new entrants.",
         fontsize=10.5, color=MUTED, fontfamily='sans-serif')

# Minimal legend
from matplotlib.patches import Patch
leg = ax.legend(
    handles=[
        Patch(facecolor=CLAY, label='2023'),
        Patch(facecolor=GHOST, label='2010'),
    ],
    loc='lower right', frameon=False, fontsize=9.5, labelcolor=INK,
)
for t in leg.get_texts():
    t.set_fontfamily('sans-serif')

fig.text(0.035, 0.04,
         "Source: EPA GHGRP Parent Company dataset, 2010 and 2023 reporting years. "
         "Top-10 share computed using any-stake union (see methodology). "
         "Analysis: @salamituns.",
         fontsize=8, color=MUTED, fontfamily='sans-serif')

plt.subplots_adjust(left=0.20, right=0.97, top=0.86, bottom=0.12)
plt.savefig(OUT, facecolor=PAPER, dpi=300, bbox_inches='tight')
print(f"wrote {OUT}")
