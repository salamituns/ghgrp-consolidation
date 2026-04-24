"""
Phase 9 / Fig 10 — Waffle grid: 221M Americans within 10 km of a GHGRP reporter
as a 1000-square tactile grid, versus the full US population.

Each square = 1/1000 of the 2023 US population (Census ACS).
Shaded clay = within 10 km of a GHGRP reporter; ink outline = not.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

PROC = '/Users/olatunde/CoWorker/Geoworks/ghgrp-repo/data/processed'
OUT = '/Users/olatunde/CoWorker/Geoworks/salamituns.github.io/ghgrp/figures/ghgrp_waffle_scale.png'

PAPER = '#F6F3EB'
INK = '#0E0E0E'
CLAY = '#A23B2A'
MUTED = '#7A7368'
FAINT = '#E4DFD3'

df = pd.read_csv(f'{PROC}/phase8_timeseries_exposure.csv')
row = df[df['year'] == 2023].iloc[0]
pct_2023 = float(row['pct_us_pop_10km'])  # 65.8526…
pop_within = float(row['pop_10km'])        # 220,976,…

# --- Waffle geometry ---
COLS, ROWS = 50, 20                       # 1000 squares
n_shaded = int(round(pct_2023 * 10))       # 65.8 → 658 squares
n_total = COLS * ROWS
square = 0.82                              # side of each square (cell=1)

fig, ax = plt.subplots(figsize=(11, 7.4), dpi=300, facecolor=PAPER)
ax.set_facecolor(PAPER)

# Fill row by row from bottom-left; left-to-right within each row.
# Bottom rows shaded first so the "within 10 km" mass feels like a floor
# rising, matching the editorial reading of 2/3rds of the country.
for idx in range(n_total):
    r = idx // COLS                  # 0 at bottom
    c = idx % COLS
    x = c
    y = r
    if idx < n_shaded:
        face = CLAY
        edge = CLAY
        lw = 0.0
    else:
        face = PAPER
        edge = INK
        lw = 0.55
    ax.add_patch(mpatches.Rectangle(
        (x + (1 - square) / 2, y + (1 - square) / 2),
        square, square,
        facecolor=face, edgecolor=edge, linewidth=lw, alpha=1.0 if idx < n_shaded else 0.55
    ))

ax.set_xlim(-1.5, COLS + 1.5)
ax.set_ylim(-8.5, ROWS + 5.2)
ax.set_aspect('equal')
ax.axis('off')

# --- Title block (top-left) ---
ax.text(0, ROWS + 4.4,
        "Two thirds of America lives within 10 km",
        fontsize=20, fontweight='medium', color=INK, fontfamily='serif', va='top')
ax.text(0, ROWS + 2.9,
        "of a facility that reports greenhouse gases to the EPA.",
        fontsize=14, color=MUTED, fontfamily='serif', fontstyle='italic', va='top')

# --- Legend blocks under the grid ---
legend_y = -2.8
# Shaded square
ax.add_patch(mpatches.Rectangle((0, legend_y - 0.55), 1.1, 1.1,
                                 facecolor=CLAY, edgecolor=CLAY, lw=0))
ax.text(1.7, legend_y, f"{pct_2023:.1f}%  \u2014  {pop_within/1e6:.1f} million residents within 10 km of a reporter",
        fontsize=11, color=INK, fontfamily='sans-serif', va='center')

# Outline square
ax.add_patch(mpatches.Rectangle((0, legend_y - 2.35), 1.1, 1.1,
                                 facecolor=PAPER, edgecolor=INK, lw=0.55, alpha=0.55))
ax.text(1.7, legend_y - 1.8, f"{100 - pct_2023:.1f}%  \u2014  everyone else",
        fontsize=11, color=MUTED, fontfamily='sans-serif', va='center')

# --- Footnote ---
ax.text(0, -7.5,
        "1 square = 1/1000 of the US population (2023). Proximity does not mean emissions exposure; see method note.\n"
        "Source: EPA GHGRP 2023 facility panel + Census ACS 2019\u20132023 B01003.",
        fontsize=8, color=MUTED, fontfamily='sans-serif', va='top')

plt.tight_layout()
plt.savefig(OUT, facecolor=PAPER, dpi=300, bbox_inches='tight')
print(f"wrote {OUT} ({n_shaded}/{n_total} shaded = {pct_2023:.2f}%)")
