"""
Regenerate all three GHGRP charts with consistent attribution (@salamituns).

Historical-record correction (Apr 15 2026, Phase 5):
  Prior versions reported the 2023 top-10 share as 18.0%. That number came from
  summing per-parent facility counts, which double-counts joint-venture facilities
  (a JV where two top-10 parents both hold stakes is counted twice in the sum).
  The correct any-stake-union figure — share of unique facilities in which any
  top-10 parent holds a stake — is 16.7%. This script now uses the union figure.
  See methodology/Trend14yr_Methodology_and_SelfAudit.md for the full write-up.
"""
import json
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.cm import ScalarMappable
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

# ============================================================
# Shared palette & attribution
# ============================================================
TEAL = '#2FAAAA'
SLATE = '#2E3A4A'
GRAY = '#B8BFC7'
ANNOT = '#C2410C'
HANDLE = '@salamituns'
SRC_PREFIX = 'Source: EPA Greenhouse Gas Reporting Program, Parent Company Dataset (2010 to 2023).'

VIZ_DIR = '/sessions/wonderful-amazing-volta/mnt/CoWorker/Geoworks/viz'


# ============================================================
# 1. TOP 10 BAR CHART - share = 16.7% (Phase 5 any-stake union)
# ============================================================
def build_top10_barchart():
    # Consolidated Top 10 (from "Top 10 Trend" sheet in xlsb)
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
    # Sort descending by 2023
    data = sorted(data, key=lambda x: x[1], reverse=True)
    names = [d[0] for d in data]
    v2023 = [d[1] for d in data]
    v2010 = [d[2] for d in data]
    deltas = [a - b for a, b in zip(v2023, v2010)]

    # Any-stake union share (Phase 5 recomputed value). Loaded from processed summary for
    # reproducibility — the sum-of-counts method overstates by ~1.3 pp due to JV double-counting.
    import os
    summary_path = os.path.join(os.path.dirname(__file__),
                                '..', 'data', 'processed', 'phase5_comparison_summary.json')
    with open(os.path.abspath(summary_path)) as f:
        top10_share = json.load(f)['recomputed_2023_pct']  # 16.74%

    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=150)
    fig.patch.set_facecolor('white')

    y = np.arange(len(names))
    ax.barh(y, v2010, color=GRAY, alpha=0.85, height=0.72, zorder=2, label='2010')
    ax.barh(y, v2023, color=TEAL, height=0.55, zorder=3, label='2023')

    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlim(0, max(v2023 + v2010) * 1.45)
    ax.set_xlabel('GHGRP reporting facilities', fontsize=10, color='#555')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', length=0)
    ax.grid(axis='x', linestyle='--', alpha=0.3, zorder=0)

    # Value labels
    for i, (v, d) in enumerate(zip(v2023, deltas)):
        ax.text(v + 6, i, f'{v}', va='center', ha='left',
                fontsize=10, fontweight='bold', color=SLATE)
        sign = f'+{d}' if d > 0 else f'{d}'
        ax.text(v + 60, i, f'({sign} vs 2010)', va='center', ha='left',
                fontsize=9, color=TEAL, style='italic')

    # Title block
    fig.text(0.045, 0.955,
             f'The Top 10 Now Control {top10_share:.1f}% of Reporting Facilities',
             fontsize=17, fontweight='bold', color=SLATE, ha='left')
    fig.text(0.045, 0.915,
             'Facility counts by parent company, 2010 vs 2023',
             fontsize=10.5, color='#555', ha='left')

    # Legend (mini, right side)
    legend_teal = mpatches.Patch(color=TEAL, label='2023')
    legend_gray = mpatches.Patch(color=GRAY, label='2010')
    ax.legend(handles=[legend_teal, legend_gray],
              loc='lower right', frameon=False, fontsize=9)

    # Source
    fig.text(0.045, 0.02,
             f'{SRC_PREFIX}   Analysis: {HANDLE}',
             fontsize=8, color='#777', ha='left')

    plt.subplots_adjust(top=0.86, bottom=0.10, left=0.22, right=0.97)
    out = f'{VIZ_DIR}/ghgrp_top10_barchart.png'
    plt.savefig(out, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'✓ Saved: {out}  (title: {top10_share:.1f}%)')


# ============================================================
# 2. 2015 VANISHING ACT DUAL-AXIS CHART
# ============================================================
def build_cliff_chart():
    data = pd.DataFrame({
        'year':       list(range(2010, 2024)),
        'facilities': [6668, 7989, 8398, 8496, 8731, 8587, 8216, 8142, 8268, 8282, 8248, 8212, 8175, 8106],
        'parents':    [3851, 4118, 4396, 4454, 4505, 3495, 3383, 3360, 3527, 3402, 3415, 3317, 3339, 3327],
    })

    fig, ax1 = plt.subplots(figsize=(11, 6.2), dpi=150)
    fig.patch.set_facecolor('white')

    ax1.plot(data['year'], data['parents'], marker='o', linewidth=2.5,
             color=SLATE, label='Unique parent companies', zorder=3,
             markersize=6, markerfacecolor=SLATE, markeredgecolor='white', markeredgewidth=1.2)
    ax1.set_ylabel('Unique parent companies', color=SLATE, fontsize=11, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=SLATE)
    ax1.set_ylim(3000, 4800)
    ax1.set_xlim(2009.5, 2023.5)
    ax1.set_xticks(data['year'])
    ax1.tick_params(axis='x', labelsize=10)
    ax1.grid(axis='y', linestyle='--', alpha=0.35, zorder=0)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    ax2 = ax1.twinx()
    ax2.plot(data['year'], data['facilities'], marker='s', linewidth=2.5,
             color=TEAL, label='Unique facilities', zorder=3,
             markersize=6, markerfacecolor=TEAL, markeredgecolor='white', markeredgewidth=1.2)
    ax2.set_ylabel('Unique facilities', color=TEAL, fontsize=11, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=TEAL)
    ax2.set_ylim(6200, 9200)
    ax2.spines['top'].set_visible(False)

    ax1.axvspan(2014, 2015, alpha=0.10, color=ANNOT, zorder=1)
    arrow = FancyArrowPatch((2014, 4505), (2015, 3495),
                            arrowstyle='->', mutation_scale=18,
                            color=ANNOT, linewidth=2, zorder=4)
    ax1.add_patch(arrow)

    ax1.annotate(
        '−1,010 parent companies\nin a single year\n(−22.4%)',
        xy=(2014.5, 4000), xytext=(2017.3, 4550),
        fontsize=10, color=ANNOT, fontweight='bold',
        ha='left', va='center',
        arrowprops=dict(arrowstyle='-', color=ANNOT, linewidth=1, linestyle=':'),
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                  edgecolor=ANNOT, linewidth=1.2)
    )

    ax2.annotate(
        'Facilities barely moved\n(8,731 → 8,587)',
        xy=(2015, 8587), xytext=(2011.2, 7100),
        fontsize=9.5, color=TEAL, fontweight='bold',
        ha='left', va='center',
        arrowprops=dict(arrowstyle='-', color=TEAL, linewidth=1, linestyle=':')
    )

    fig.text(0.045, 0.955, 'The 2015 Vanishing Act',
             fontsize=17, fontweight='bold', color=SLATE, ha='left')
    fig.text(0.045, 0.915,
             'Over 1,000 parent companies disappeared between 2014 and 2015, '
             'while facility counts barely moved',
             fontsize=10.5, color='#555', ha='left', style='italic')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2,
               loc='lower right', frameon=False, fontsize=10)

    fig.text(0.045, 0.02,
             f'{SRC_PREFIX}   Analysis: {HANDLE}',
             fontsize=8, color='#777', ha='left')

    plt.subplots_adjust(top=0.86, bottom=0.10, left=0.08, right=0.92)
    out = f'{VIZ_DIR}/ghgrp_2015_vanishing_act.png'
    plt.savefig(out, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'✓ Saved: {out}')


# ============================================================
# 3. TILE-GRID CARTOGRAM
# ============================================================
# Canonical tile-grid layout (row, col) per state
TILE_LAYOUT = {
    'AK': (0, 0),
    'ME': (0, 10),
    'VT': (1, 9), 'NH': (1, 10),
    'WA': (1, 1), 'ID': (1, 2), 'MT': (1, 3), 'ND': (1, 4), 'MN': (1, 5),
    'WI': (1, 6), 'IL': (1, 7), 'MI': (1, 8), 'NY': (2, 9), 'MA': (2, 10),
    'OR': (2, 1), 'NV': (2, 2), 'WY': (2, 3), 'SD': (2, 4), 'IA': (2, 5),
    'IN': (2, 6), 'OH': (2, 7), 'PA': (2, 8),
    'NJ': (3, 9), 'CT': (3, 10), 'RI': (3, 11),
    'CA': (3, 1), 'UT': (3, 2), 'CO': (3, 3), 'NE': (3, 4), 'MO': (3, 5),
    'KY': (3, 6), 'WV': (3, 7), 'VA': (3, 8),
    'MD': (4, 9), 'DE': (4, 10),
    'AZ': (4, 2), 'NM': (4, 3), 'KS': (4, 4), 'AR': (4, 5), 'TN': (4, 6),
    'NC': (4, 7), 'SC': (4, 8),
    'HI': (5, 0),
    'OK': (5, 4), 'LA': (5, 5), 'MS': (5, 6), 'AL': (5, 7), 'GA': (5, 8),
    'DC': (5, 9),
    'TX': (6, 4),
    'FL': (6, 8),
}

def build_tilegrid():
    with open(f'{VIZ_DIR}/state_counts_2023.json') as f:
        counts = json.load(f)

    # Remove territories from tile chart (GU, PR, VI); they're not in TILE_LAYOUT
    total = 8106  # consistent with the post

    layout = dict(TILE_LAYOUT)

    fig, ax = plt.subplots(figsize=(11, 6.8), dpi=150)
    fig.patch.set_facecolor('white')

    vals = [counts.get(s, 0) for s in layout.keys() if counts.get(s, 0) > 0]
    vmin, vmax = max(1, min(vals)), max(vals)
    norm = LogNorm(vmin=vmin, vmax=vmax)
    cmap = plt.cm.get_cmap('BuGn')

    for state, (row, col) in layout.items():
        count = counts.get(state, 0)
        if count == 0:
            continue
        color = cmap(norm(count))
        # Text color based on tile intensity
        text_color = 'white' if norm(count) > 0.45 else SLATE
        rect = FancyBboxPatch(
            (col, -row), 0.88, 0.88,
            boxstyle="round,pad=0.02,rounding_size=0.1",
            facecolor=color, edgecolor='white', linewidth=2, zorder=2
        )
        ax.add_patch(rect)
        # State abbrev
        ax.text(col + 0.44, -row + 0.62, state,
                ha='center', va='center', fontsize=10,
                fontweight='bold', color=text_color, zorder=3)
        # Facility count
        ax.text(col + 0.44, -row + 0.28, f'{count:,}',
                ha='center', va='center', fontsize=8.5,
                color=text_color, zorder=3)

    ax.set_xlim(-0.3, 12)
    ax.set_ylim(-7.2, 0.9)
    ax.set_aspect('equal')
    ax.axis('off')

    # Title block
    fig.text(0.045, 0.955, 'Emissions Infrastructure Clusters in the South',
             fontsize=17, fontweight='bold', color=SLATE, ha='left')
    fig.text(0.045, 0.918,
             'GHGRP reporting facilities by state · 2023 · 8,106 facilities',
             fontsize=10.5, color='#555', ha='left')

    # Colorbar (small, bottom right)
    cax = fig.add_axes([0.65, 0.09, 0.25, 0.015])
    sm = ScalarMappable(cmap=cmap, norm=norm)
    cb = fig.colorbar(sm, cax=cax, orientation='horizontal')
    cb.set_label('Facilities per state (log scale)', fontsize=8, color='#555')
    cb.ax.tick_params(labelsize=7)

    # Summary text (bottom left)
    fig.text(0.045, 0.115,
             'Texas alone hosts 1,438 facilities (17.7% of the national total).\n'
             'Three states (TX, CA, LA) account for 28.2% of reporting facilities.',
             fontsize=9, color='#555', ha='left', style='italic')

    # Source
    fig.text(0.045, 0.02,
             f'{SRC_PREFIX}   Analysis: {HANDLE}   ·   '
             'Tile-grid cartogram for equal-weight state comparison',
             fontsize=8, color='#777', ha='left')

    out = f'{VIZ_DIR}/ghgrp_facility_tilegrid_2023.png'
    plt.savefig(out, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'✓ Saved: {out}')


# ============================================================
if __name__ == '__main__':
    build_top10_barchart()
    build_cliff_chart()
    build_tilegrid()
    print('\nAll three charts regenerated with @salamituns attribution.')
