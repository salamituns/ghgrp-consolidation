"""
Phase 9 / Fig 03: Comparative ribbon: 221M Americans within 10 km of a GHGRP
reporter, expressed as an equivalent-length stack of recognizable nations.

Top bar: the US-within-10km population (clay, single block).
Bottom bar: Germany + UK + Canada + Australia, total ~217M, segmented.
The two bars are drawn to identical length to carry the tactile claim.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

OUT = '/Users/olatunde/CoWorker/Geoworks/salamituns.github.io/ghgrp/figures/ghgrp_comparative_ribbon.png'

PAPER = '#F6F3EB'
INK = '#0E0E0E'
CLAY = '#A23B2A'
MUTED = '#7A7368'
FAINT = '#D9D2C4'

# --- Source populations (World Bank / UN DESA, 2023) ----------------------
US_WITHIN = 221.0  # millions, GHGRP-within-10km population (2023)
COUNTRIES = [
    ('Germany',   84),
    ('United Kingdom', 67),
    ('Canada',    40),
    ('Australia', 26),
]
NATION_TOTAL = sum(p for _, p in COUNTRIES)  # 217M
GAP = US_WITHIN - NATION_TOTAL  # ~4M

# --- Geometry -------------------------------------------------------------
BAR_LEN = US_WITHIN  # x-axis units = millions of people, so both bars span 0..221
BAR_HEIGHT = 1.0
BAR_GAP = 1.1  # vertical space between the two bars
Y_TOP = 2.6
Y_BOT = Y_TOP - BAR_GAP

fig, ax = plt.subplots(figsize=(12, 4.6), dpi=300, facecolor=PAPER)
ax.set_facecolor(PAPER)

# --- Top bar: US within 10 km ---------------------------------------------
ax.add_patch(mpatches.Rectangle((0, Y_TOP), BAR_LEN, BAR_HEIGHT,
                                 facecolor=CLAY, edgecolor=CLAY, lw=0))
ax.text(BAR_LEN / 2, Y_TOP + BAR_HEIGHT / 2,
        "221 million Americans within 10 km of a reporter",
        ha='center', va='center', color=PAPER, fontsize=12.5,
        fontfamily='sans-serif', fontweight='medium')

# Endpoint tick
ax.plot([0, 0], [Y_TOP - 0.08, Y_TOP + BAR_HEIGHT + 0.08], color=INK, lw=0.6)
ax.plot([BAR_LEN, BAR_LEN], [Y_TOP - 0.08, Y_TOP + BAR_HEIGHT + 0.08], color=INK, lw=0.6)

# --- Bottom bar: four-nation stack ----------------------------------------
NATION_SHADES = ['#2E3440', '#4C566A', '#7A7368', '#A89F91']  # four tonal steps

cursor = 0
for (label, pop), shade in zip(COUNTRIES, NATION_SHADES):
    ax.add_patch(mpatches.Rectangle((cursor, Y_BOT), pop, BAR_HEIGHT,
                                     facecolor=shade, edgecolor=PAPER, lw=1.2))
    # In-segment label (country + population, centred)
    ax.text(cursor + pop / 2, Y_BOT + BAR_HEIGHT / 2,
            f"{label}\n{pop}M",
            ha='center', va='center', color=PAPER, fontsize=10.2,
            fontfamily='sans-serif', fontweight='medium')
    cursor += pop

# Gap block (honest: 4M short of the US bar)
if GAP > 0:
    ax.add_patch(mpatches.Rectangle((cursor, Y_BOT), GAP, BAR_HEIGHT,
                                     facecolor=PAPER, edgecolor=INK, lw=0.55,
                                     hatch='///', alpha=0.55))
    ax.text(cursor + GAP / 2, Y_BOT - 0.22,
            f"+{GAP:.0f}M", ha='center', va='top', color=MUTED, fontsize=8.5,
            fontfamily='sans-serif')

ax.plot([0, 0], [Y_BOT - 0.08, Y_BOT + BAR_HEIGHT + 0.08], color=INK, lw=0.6)
ax.plot([BAR_LEN, BAR_LEN], [Y_BOT - 0.08, Y_BOT + BAR_HEIGHT + 0.08], color=INK, lw=0.6)

# --- Connector ticks at each nation boundary ------------------------------
cursor = 0
for _, pop in COUNTRIES:
    cursor += pop
    if cursor < BAR_LEN:
        ax.plot([cursor, cursor], [Y_BOT - 0.04, Y_BOT - 0.18],
                color=MUTED, lw=0.5)

# --- Title block ----------------------------------------------------------
ax.text(0, Y_TOP + BAR_HEIGHT + 1.05,
        "Put it somewhere you can feel it.",
        fontsize=19, fontweight='medium', color=INK, fontfamily='serif',
        va='bottom')
ax.text(0, Y_TOP + BAR_HEIGHT + 0.55,
        "The population within 10 km of an American emissions reporter is roughly the combined "
        "population of Germany, the United Kingdom, Canada, and Australia.",
        fontsize=11, color=MUTED, fontfamily='serif', fontstyle='italic',
        va='bottom', wrap=True)

# --- Footnote -------------------------------------------------------------
ax.text(0, Y_BOT - 0.65,
        "Sources: GHGRP exposure figure from EPA GHGRP 2023 facility panel + ACS 2019\u20132023 B01003, 10\u00a0km union buffers in EPSG:5070.  "
        "Country populations from UN DESA World Population Prospects 2024, mid-2023 estimates, rounded.  "
        "Analysis: @salamituns.",
        fontsize=8, color=MUTED, fontfamily='sans-serif', va='top')

ax.set_xlim(-2, BAR_LEN + 2)
ax.set_ylim(-0.1, Y_TOP + BAR_HEIGHT + 2.2)
ax.set_aspect('auto')
ax.axis('off')

plt.tight_layout()
plt.savefig(OUT, facecolor=PAPER, dpi=300, bbox_inches='tight')
print(f"wrote {OUT}")
