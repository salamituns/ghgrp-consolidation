"""
Render phase 8 time-series as a publication PNG to match the existing
editorial figures (paper bg, ink text, clay accent).
"""
import pandas as pd
import matplotlib.pyplot as plt

PROC = '/Users/olatunde/CoWorker/Geoworks/ghgrp-repo/data/processed'
OUT = '/Users/olatunde/CoWorker/Geoworks/salamituns.github.io/ghgrp/figures/ghgrp_exposure_timeseries.png'

PAPER = '#F6F3EB'
INK = '#0E0E0E'
CLAY = '#A23B2A'
MUTED = '#7A7368'

df = pd.read_csv(f'{PROC}/phase8_timeseries_exposure.csv')
df['pop_10km_m'] = df['pop_10km'] / 1e6

fig, ax = plt.subplots(figsize=(10, 5.2), dpi=300, facecolor=PAPER)
ax.set_facecolor(PAPER)

# Main series: 10 km exposure, in millions
ax.plot(df['year'], df['pop_10km_m'], color=CLAY, lw=2.4, zorder=3)
ax.scatter(df['year'], df['pop_10km_m'], color=CLAY, s=22, zorder=4, edgecolor=PAPER, lw=1.2)

# Annotate endpoints
y0 = df.iloc[0]
y1 = df.iloc[-1]
ax.annotate(f"{y0['pop_10km_m']:.1f}M  ({y0['pct_us_pop_10km']:.1f}% of US pop)",
            xy=(y0['year'], y0['pop_10km_m']),
            xytext=(6, -14), textcoords='offset points',
            color=INK, fontsize=10, fontfamily='serif')
ax.annotate(f"{y1['pop_10km_m']:.1f}M  ({y1['pct_us_pop_10km']:.1f}% of US pop)",
            xy=(y1['year'], y1['pop_10km_m']),
            xytext=(-6, 10), textcoords='offset points',
            color=INK, fontsize=10, fontfamily='serif', ha='right')

# Title & subtitle
ax.set_title("Americans within 10 km of a GHGRP reporter, 2010\u20132023",
             loc='left', pad=18, color=INK, fontsize=14, fontfamily='serif',
             fontweight='medium')
ax.text(0.0, 1.02,
        "Population layer frozen at ACS 2019\u20132023 to isolate facility entry / exit signal.",
        transform=ax.transAxes, fontsize=9, color=MUTED, fontfamily='sans-serif')

# Axes cosmetics
ax.set_xlim(2009.5, 2023.5)
ax.set_ylim(195, 225)
ax.set_xticks(range(2010, 2024, 2))
ax.set_yticks([200, 205, 210, 215, 220, 225])
ax.tick_params(colors=INK, labelsize=10)
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['left', 'bottom']:
    ax.spines[spine].set_color(INK)
    ax.spines[spine].set_linewidth(0.6)

ax.grid(axis='y', color=INK, alpha=0.08, lw=0.5)
ax.set_ylabel('Millions of residents', color=INK, fontsize=10)
ax.set_xlabel('Reporting year', color=INK, fontsize=10)

# Footnote
ax.text(0.0, -0.18,
        "Source: EPA GHGRP facility panel + Census ACS 5-year B01003 (tract-level), "
        "10 km union buffers in EPSG:5070, area-weighted tract population.",
        transform=ax.transAxes, fontsize=8, color=MUTED, fontfamily='sans-serif')

plt.tight_layout()
plt.savefig(OUT, facecolor=PAPER, dpi=300, bbox_inches='tight')
print(f"wrote {OUT}")
