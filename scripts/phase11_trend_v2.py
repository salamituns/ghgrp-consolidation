"""
Phase 11 / Fig 04 v2: 14-year top-10 concentration trend, editorial palette.

Reads the already-computed phase5_14yr_trend.csv, re-renders in paper/ink/clay
at 300 DPI with Fraunces serif titling and Inter sans labels. Keeps the 2015
parent-co reclassification callout: it's a real data-integrity flag worth
preserving in the visual.
"""
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import matplotlib.pyplot as plt

TREND = '/Users/olatunde/CoWorker/Geoworks/ghgrp-repo/data/processed/phase5_14yr_trend.csv'
OUT = '/Users/olatunde/CoWorker/Geoworks/salamituns.github.io/ghgrp/figures/ghgrp_14yr_trend_recomputed.png'

PAPER = '#F6F3EB'
INK = '#0E0E0E'
CLAY = '#A23B2A'
MUTED = '#7A7368'
FAINT = '#D9D2C4'

trend = pd.read_csv(TREND).sort_values('year').reset_index(drop=True)
xs = trend['year'].values
ys = trend['top10_share_pct'].values

y_2010 = float(trend[trend['year']==2010]['top10_share_pct'].iloc[0])
y_2023 = float(trend[trend['year']==2023]['top10_share_pct'].iloc[0])
delta_pp = y_2023 - y_2010
rel_growth = (y_2023 / y_2010 - 1) * 100

fig, ax = plt.subplots(figsize=(13, 6.6), dpi=300, facecolor=PAPER)
ax.set_facecolor(PAPER)

# 2015 reclassification shaded span: FAINT band, no arrow
ax.axvspan(2014.5, 2015.5, color=FAINT, alpha=0.8, zorder=1)
ax.text(2015, 10.0, '2015\nparent-co\nreclassification',
        fontsize=8.5, color=MUTED, ha='center', va='bottom',
        fontfamily='sans-serif', zorder=2)

# Trend line
ax.plot(xs, ys, color=CLAY, linewidth=2.4, zorder=3, solid_capstyle='round')
ax.scatter(xs, ys, s=42, color=CLAY, edgecolor=PAPER, linewidth=1.2, zorder=4)

# Endpoint labels
ax.annotate(f'{y_2010:.1f}%', xy=(2010, y_2010), xytext=(2010-0.15, y_2010+0.6),
            fontsize=12, color=INK, fontfamily='serif', fontweight='medium', ha='left')
ax.annotate(f'{y_2023:.1f}%', xy=(2023, y_2023), xytext=(2023-0.35, y_2023+0.6),
            fontsize=12, color=CLAY, fontfamily='serif', fontweight='medium', ha='right')

# Axes
ax.set_xlim(2009.5, 2023.8)
ax.set_ylim(9.5, 18.5)
ax.set_xticks(xs)
ax.tick_params(axis='both', labelsize=9, colors=MUTED, length=0, pad=6)
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontfamily('sans-serif')
ax.set_yticks([10, 12, 14, 16, 18])
ax.set_yticklabels(['10%', '12%', '14%', '16%', '18%'])
ax.grid(axis='y', linestyle='-', alpha=0.4, color=FAINT, zorder=0)
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color(FAINT); ax.spines['left'].set_linewidth(0.6)
ax.spines['bottom'].set_color(FAINT); ax.spines['bottom'].set_linewidth(0.6)

# Title block
fig.text(0.035, 0.955,
         "Ownership, compounding.",
         fontsize=20, color=INK, fontfamily='serif', fontweight='medium')
fig.text(0.035, 0.905,
         f"Top 10 parent companies rose from {y_2010:.1f}% of GHGRP-reporting facilities in 2010 to "
         f"{y_2023:.1f}% in 2023. A {delta_pp:.1f} percentage-point absolute gain, {rel_growth:.0f}% relative.",
         fontsize=10.5, color=MUTED, fontfamily='sans-serif')

fig.text(0.035, 0.04,
         "Source: EPA GHGRP Parent Company dataset, annual sheets 2010\u20132023.  "
         "Methodology: top-10 parents selected per year by unique facility count; share = unique facilities with any top-10 stake (any-stake union).  "
         "Analysis: @salamituns.",
         fontsize=8, color=MUTED, fontfamily='sans-serif')

plt.subplots_adjust(left=0.06, right=0.97, top=0.86, bottom=0.10)
plt.savefig(OUT, facecolor=PAPER, dpi=300, bbox_inches='tight')
print(f"wrote {OUT}")
