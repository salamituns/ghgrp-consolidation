"""
Phase 9 / OG — Open Graph share card for the GHGRP publication.

Output: 1200x630 PNG, paper/ink/clay palette, one headline + one stat.
Reads at full-res and at LinkedIn/Twitter thumbnail scale.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

OUT = '/Users/olatunde/CoWorker/Geoworks/salamituns.github.io/ghgrp/og-card.png'

PAPER = '#F6F3EB'
INK = '#0E0E0E'
CLAY = '#A23B2A'
MUTED = '#7A7368'

# 1200x630 at 100 dpi = 12x6.3 inches
fig, ax = plt.subplots(figsize=(12, 6.3), dpi=100, facecolor=PAPER)
ax.set_facecolor(PAPER)

# Normalise coordinate space to 0..1200 x 0..630
ax.set_xlim(0, 1200)
ax.set_ylim(0, 630)
ax.set_aspect('equal')
ax.axis('off')

# --- Right-edge clay bar (visual spine) -----------------------------------
ax.add_patch(mpatches.Rectangle((1150, 0), 8, 630, facecolor=CLAY, lw=0))

# --- Eyebrow --------------------------------------------------------------
ax.text(70, 555, "GHGRP  \u00b7  2026 ANALYSIS  \u00b7  OLATUNDE SALAMI",
        fontsize=13, color=MUTED, fontfamily='sans-serif', fontweight='medium',
        va='top')

# --- Headline (two lines, serif) ------------------------------------------
ax.text(70, 490, "Who owns America\u2019s",
        fontsize=58, color=INK, fontfamily='serif', fontweight='medium',
        va='top')
ax.text(70, 415, "industrial emissions.",
        fontsize=58, color=CLAY, fontfamily='serif', fontweight='medium',
        fontstyle='italic', va='top')

# --- Horizontal rule ------------------------------------------------------
ax.plot([70, 1100], [325, 325], color=INK, lw=1.0, alpha=0.25)

# --- Three-stat row -------------------------------------------------------
stats = [
    ("221M", "Americans within 10 km of a reporter"),
    ("8,106", "Facilities. 3,327 parents."),
    ("14 yrs", "2010\u20132023. One consolidation pattern."),
]
x_positions = [70, 460, 830]
for (big, label), x in zip(stats, x_positions):
    ax.text(x, 260, big, fontsize=44, color=INK, fontfamily='serif',
            fontweight='medium', va='top')
    ax.text(x, 180, label, fontsize=13, color=MUTED, fontfamily='sans-serif',
            va='top')

# --- URL footer -----------------------------------------------------------
ax.text(70, 85, "salamituns.github.io/ghgrp",
        fontsize=14, color=INK, fontfamily='sans-serif', fontweight='medium',
        va='top')
ax.text(70, 55, "Fourteen years of EPA GHGRP data, reconciled at the parent-company level.",
        fontsize=12, color=MUTED, fontfamily='sans-serif', fontstyle='italic',
        va='top')

# Tight save — bbox_inches=None so the exact 1200x630 is preserved
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.savefig(OUT, facecolor=PAPER, dpi=100, bbox_inches=None, pad_inches=0)
print(f"wrote {OUT}")
