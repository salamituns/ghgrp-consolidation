"""
Phase 9 / Fig 09 v2 \u2014 14-year exposure time-series with milestone annotations.

Pins four factual markers on the curve so the reader sees the shape as a
chronology, not just a trend:
  \u2022 2011 \u2014 Subpart W active; petroleum & natural gas systems begin reporting.
  \u2022 2014 \u2014 Kinder Morgan rolls up El Paso / KMP / KMR into a single C-corp.
  \u2022 2018 \u2014 Energy Transfer completes Regency (2015) + Sunoco Logistics (2017) consolidation.
  \u2022 2022 \u2014 Inflation Reduction Act signed; methane Waste Emissions Charge enacted.

Overwrites the existing Fig 09 PNG in place so the site picks it up automatically.
"""
import pandas as pd
import matplotlib.pyplot as plt

PROC = '/Users/olatunde/CoWorker/Geoworks/ghgrp-repo/data/processed'
OUT = '/Users/olatunde/CoWorker/Geoworks/salamituns.github.io/ghgrp/figures/ghgrp_exposure_timeseries.png'

PAPER = '#F6F3EB'
INK = '#0E0E0E'
CLAY = '#A23B2A'
MUTED = '#7A7368'
FAINT = '#D9D2C4'

df = pd.read_csv(f'{PROC}/phase8_timeseries_exposure.csv')
df['pop_10km_m'] = df['pop_10km'] / 1e6

fig, ax = plt.subplots(figsize=(11.2, 6.3), dpi=300, facecolor=PAPER)
ax.set_facecolor(PAPER)

# --- Main series ---
ax.plot(df['year'], df['pop_10km_m'], color=CLAY, lw=2.6, zorder=5)
ax.scatter(df['year'], df['pop_10km_m'], color=CLAY, s=26, zorder=6,
           edgecolor=PAPER, lw=1.3)

y0 = df.iloc[0]
y1 = df.iloc[-1]

# Endpoint labels
ax.annotate(f"{y0['pop_10km_m']:.1f}M  ({y0['pct_us_pop_10km']:.1f}%)",
            xy=(y0['year'], y0['pop_10km_m']),
            xytext=(10, -6), textcoords='offset points',
            color=INK, fontsize=11, fontfamily='serif', fontweight='medium')
ax.annotate(f"{y1['pop_10km_m']:.1f}M  ({y1['pct_us_pop_10km']:.1f}%)",
            xy=(y1['year'], y1['pop_10km_m']),
            xytext=(-10, 18), textcoords='offset points',
            color=INK, fontsize=11, fontfamily='serif', fontweight='medium', ha='right')

# --- Milestones ---
# Place labels using axis coordinates, with long leader lines to data points.
# Top-row labels for later years (2018, 2022) and bottom-row for early years
# (2011, 2014) \u2014 early curve is low so labels sit ABOVE with downward leaders;
# late curve is near the top so labels sit ABOVE too but offset further up.
milestones = [
    {
        'year': 2011,
        'label': 'Subpart W active',
        'sub': 'Petroleum & natural gas\nsystems begin reporting.',
        'label_xy': (2010.3, 217.5),
        'ha': 'left',
    },
    {
        'year': 2014,
        'label': 'Kinder Morgan roll-up',
        'sub': 'KMI consolidates El Paso,\nKMP, KMR into one C-corp.',
        'label_xy': (2013.6, 207.8),
        'ha': 'left',
    },
    {
        'year': 2018,
        'label': 'Energy Transfer consolidates',
        'sub': 'Regency (2015) + Sunoco\nLogistics (2017) roll-up.',
        'label_xy': (2017.2, 213.4),
        'ha': 'left',
    },
    {
        'year': 2022,
        'label': 'Methane fee enacted',
        'sub': 'IRA signs Waste Emissions\nCharge into law.',
        'label_xy': (2017.2, 226.3),
        'ha': 'left',
    },
]

for m in milestones:
    y_val = df[df['year'] == m['year']]['pop_10km_m'].iloc[0]
    # Marker ring at the data point
    ax.scatter([m['year']], [y_val], s=85, facecolor=PAPER,
               edgecolor=INK, lw=1.1, zorder=7)
    ax.scatter([m['year']], [y_val], s=14, color=INK, zorder=8)
    # Leader line from marker to label
    lx, ly = m['label_xy']
    ax.annotate(
        '',
        xy=(m['year'], y_val), xytext=(lx, ly),
        arrowprops=dict(arrowstyle='-', color=INK, lw=0.6, alpha=0.32),
        zorder=3,
    )
    # Label headline
    ax.text(lx, ly, m['label'],
            color=INK, fontsize=10.5, fontfamily='sans-serif', fontweight='medium',
            ha=m['ha'], va='bottom')
    # Sub
    ax.text(lx, ly - 0.35, m['sub'],
            color=MUTED, fontsize=9, fontfamily='sans-serif',
            ha=m['ha'], va='top')

# --- Title & subtitle ---
ax.set_title("From 200 to 221 million, 2010\u20132023",
             loc='left', pad=28, color=INK, fontsize=17, fontfamily='serif',
             fontweight='medium')
ax.text(0.0, 1.035,
        "Americans within 10 km of a GHGRP reporter. Population layer frozen at "
        "ACS 2019\u20132023 to isolate facility entry / exit signal.",
        transform=ax.transAxes, fontsize=10.5, color=MUTED, fontfamily='sans-serif')

# --- Axes ---
ax.set_xlim(2009.4, 2023.6)
ax.set_ylim(198, 230)
ax.set_xticks(range(2010, 2024, 2))
ax.set_yticks([200, 205, 210, 215, 220, 225])
ax.tick_params(colors=INK, labelsize=10)
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['left', 'bottom']:
    ax.spines[spine].set_color(INK)
    ax.spines[spine].set_linewidth(0.6)

ax.grid(axis='y', color=INK, alpha=0.07, lw=0.5)
ax.set_ylabel('Millions of residents', color=INK, fontsize=10)
ax.set_xlabel('Reporting year', color=INK, fontsize=10)

# --- Footnote (two-line wrap so the bbox stays tight to the axes width) ---
ax.text(0.0, -0.14,
        "Source: EPA GHGRP facility panel + Census ACS 5-year B01003 (tract-level), "
        "10 km union buffers in EPSG:5070, area-weighted tract population.",
        transform=ax.transAxes, fontsize=8, color=MUTED, fontfamily='sans-serif')
ax.text(0.0, -0.175,
        "Milestone dates from EPA GHGRP rule history; Kinder Morgan 8-K (Nov 2014); "
        "Energy Transfer 10-K (2018); IRA \u00a7 60113 (Aug 2022).",
        transform=ax.transAxes, fontsize=8, color=MUTED, fontfamily='sans-serif')

plt.tight_layout()
plt.savefig(OUT, facecolor=PAPER, dpi=300, bbox_inches='tight')
print(f"wrote {OUT}")
