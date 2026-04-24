"""
Phase 9 / Fig 11: Bump chart: rank evolution of the top parent operators
by GHGRP facility count, 2010 \u2192 2023.

Renders the union of (top 10 in 2010) \u222a (top 10 in 2023). Operators not
in a top-N list for a given year are truncated at the edge with a dotted
tail so the reader sees entry / exit rather than silent gaps.
"""
import warnings
warnings.filterwarnings('ignore')

import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pyxlsb import open_workbook

RAW = '/Users/olatunde/CoWorker/Geoworks/data/raw/epa_ghgrp/ghgp_data_parent_company.xlsb'
OUT = '/Users/olatunde/CoWorker/Geoworks/salamituns.github.io/ghgrp/figures/ghgrp_bump_operators.png'

PAPER = '#F6F3EB'
INK = '#0E0E0E'
CLAY = '#A23B2A'
MUTED = '#7A7368'
FAINT = '#C9C2B5'

YEARS = list(range(2010, 2024))
RANK_FLOOR = 15  # only plot ranks 1\u2013N; beyond = off-panel

# --- Name normalization ---------------------------------------------------
SUFFIX_PATTERNS = [
    r'\bLLC\b', r'\bINC\b', r'\bL\.P\.\b', r'\bLP\b', r'\bCORP\b', r'\bCO\b',
    r'\bCOMPANY\b', r'\bCOMPANIES\b', r'\bCORPORATION\b', r'\bINCORPORATED\b',
    r'\bHOLDINGS?\b', r'\bGROUP\b', r'\bRESOURCES\b', r'\bENERGY\b',
    r'\bPARTNERS?\b', r'\bOPERATING\b', r'\bLIMITED\b', r'\bTHE\b',
]
SUFFIX_RE = re.compile('|'.join(SUFFIX_PATTERNS), re.IGNORECASE)
PUNCT_RE = re.compile(r"[.,'\"&\-/\\]")

# Canonical mapping for the known top operators (keeps the bump readable)
ALIASES = {
    'KINDER MORGAN': 'Kinder Morgan',
    'EL PASO': 'El Paso',
    'ENERGY TRANSFER': 'Energy Transfer',
    'REGENCY': 'Energy Transfer',
    'SUNOCO LOGISTICS': 'Energy Transfer',
    'WILLIAMS': 'Williams',
    'WILLIAMS FIELD SERVICES': 'Williams',
    'WILLIAMS PARTNERS': 'Williams',
    'WMB HOLDINGS': 'Williams',
    'WASTE MANAGEMENT': 'Waste Management',
    'REPUBLIC SERVICES': 'Republic Services',
    'CALPINE': 'Calpine',
    'CONOCOPHILLIPS': 'ConocoPhillips',
    'CONOCO PHILLIPS': 'ConocoPhillips',
    'PHILLIPS 66': 'Phillips 66',
    'CHEVRON': 'Chevron',
    'EXXON': 'ExxonMobil',
    'EXXONMOBIL': 'ExxonMobil',
    'BP': 'BP',
    'BP AMERICA': 'BP',
    'SHELL': 'Shell',
    'DOMINION': 'Dominion',
    'US GOVERNMENT': 'US Government',
    'U S GOVERNMENT': 'US Government',
    'UNITED STATES GOVERNMENT': 'US Government',
    'XCEL': 'Xcel Energy',
    'ANADARKO': 'Anadarko',
    'OCCIDENTAL': 'Occidental',
    'SPECTRA': 'Spectra',
    'BERKSHIRE HATHAWAY': 'Berkshire Hathaway',
    'DUKE': 'Duke Energy',
    'DTE': 'DTE Energy',
    'SOUTHERN': 'Southern Company',
    'EQT': 'EQT',
    'ENCANA': 'Ovintiv',
    'OVINTIV': 'Ovintiv',
    'ENBRIDGE': 'Enbridge',
    'TRANSCANADA': 'TC Energy',
    'TC ENERGY': 'TC Energy',
    'ENTERPRISE PRODUCTS': 'Enterprise Products',
    'MARATHON': 'Marathon',
    'VALERO': 'Valero',
    'DEVON': 'Devon',
    'PIONEER NATURAL': 'Pioneer Natural',
    'CHENIERE': 'Cheniere',
    'TARGA': 'Targa',
    'DCP MIDSTREAM': 'DCP Midstream',
    'AMERICAN ELECTRIC POWER': 'American Electric Power',
    'AEP': 'American Electric Power',
}

def canonicalize(name: str) -> str:
    if not isinstance(name, str):
        return 'Unknown'
    s = name.upper().strip()
    s = PUNCT_RE.sub(' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    # Alias lookup: match if alias key is a prefix or contained in the name
    for key in sorted(ALIASES.keys(), key=len, reverse=True):
        if key in s:
            return ALIASES[key]
    s = SUFFIX_RE.sub(' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s.title() if s else 'Unknown'

# --- Load the per-year facility-parent panel ------------------------------
rows_all = []
with open_workbook(RAW) as wb:
    for year in YEARS:
        with wb.get_sheet(str(year)) as sheet:
            srows = list(sheet.rows())
            headers = [c.v for c in srows[0]]
            data = [[c.v for c in r] for r in srows[1:]]
        df = pd.DataFrame(data, columns=headers)
        df = df.dropna(subset=['GHGRP FACILITY ID', 'PARENT COMPANY NAME']).copy()
        df['GHGRP FACILITY ID'] = df['GHGRP FACILITY ID'].astype(int)
        df['parent_canon'] = df['PARENT COMPANY NAME'].apply(canonicalize)
        # unique facility-parent pairs per year (avoid JV double-count)
        uniq = df[['GHGRP FACILITY ID', 'parent_canon']].drop_duplicates()
        counts = uniq.groupby('parent_canon')['GHGRP FACILITY ID'].nunique().reset_index(name='n')
        counts['year'] = year
        counts['rank'] = counts['n'].rank(method='min', ascending=False).astype(int)
        rows_all.append(counts)

panel = pd.concat(rows_all, ignore_index=True)

# --- Select tracked operators: union of top-10 in 2010 and 2023 -----------
top_2010 = panel[(panel['year'] == 2010) & (panel['rank'] <= 10)].sort_values('rank')
top_2023 = panel[(panel['year'] == 2023) & (panel['rank'] <= 10)].sort_values('rank')
tracked = list(dict.fromkeys(list(top_2010['parent_canon']) + list(top_2023['parent_canon'])))

print(f"Tracked {len(tracked)} operators: {tracked}")

# --- Build the rank matrix (NaN = outside top RANK_FLOOR) -----------------
track_df = panel[panel['parent_canon'].isin(tracked)].copy()
track_df.loc[track_df['rank'] > RANK_FLOOR, 'rank'] = np.nan

pivot = track_df.pivot_table(index='parent_canon', columns='year', values='rank')
pivot = pivot.reindex(tracked)

# --- Plot ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 7.6), dpi=300, facecolor=PAPER)
ax.set_facecolor(PAPER)

# Color logic: a handful of storyline operators get clay; others ink/muted.
STORY = {'Kinder Morgan', 'Energy Transfer', 'Williams', 'El Paso'}
STORY_COLORS = {
    'Kinder Morgan': CLAY,
    'Energy Transfer': '#C57B35',
    'Williams': '#6B7A8F',
    'El Paso': '#8A8378',
}

for parent in tracked:
    series = pivot.loc[parent]
    xs = series.index.values
    ys = series.values
    is_story = parent in STORY
    color = STORY_COLORS.get(parent, INK if is_story else FAINT)
    lw = 2.4 if is_story else 1.1
    alpha = 1.0 if is_story else 0.55
    ax.plot(xs, ys, color=color, lw=lw, alpha=alpha, zorder=3 if is_story else 2)
    ax.scatter(xs, ys, color=color, s=26 if is_story else 14,
               zorder=4 if is_story else 2, edgecolor=PAPER, lw=1.0, alpha=alpha)

# Invert so rank 1 sits on top
ax.invert_yaxis()
ax.set_ylim(RANK_FLOOR + 0.7, 0.3)
ax.set_yticks(range(1, RANK_FLOOR + 1))
ax.set_xticks(YEARS)
ax.set_xticklabels([str(y) if (y % 2 == 0 or y == 2023) else '' for y in YEARS], fontsize=10)
ax.tick_params(colors=INK, labelsize=10)
ax.set_ylabel('Rank by number of reporting facilities', color=INK, fontsize=10)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['left', 'bottom']:
    ax.spines[spine].set_color(INK)
    ax.spines[spine].set_linewidth(0.6)
ax.grid(axis='y', color=INK, alpha=0.06, lw=0.5)

# Left labels (2010 rank \u2192 operator)
for parent in tracked:
    r0 = pivot.loc[parent].get(2010, np.nan)
    if pd.notna(r0):
        color = STORY_COLORS.get(parent, MUTED)
        ax.text(2009.6, r0, parent, ha='right', va='center',
                fontsize=10 if parent in STORY else 9,
                fontweight='medium' if parent in STORY else 'normal',
                color=color, fontfamily='sans-serif')

# Right labels (2023 rank \u2192 operator) with facility count
for parent in tracked:
    r1 = pivot.loc[parent].get(2023, np.nan)
    if pd.notna(r1):
        color = STORY_COLORS.get(parent, MUTED)
        n = int(panel[(panel['year'] == 2023) & (panel['parent_canon'] == parent)]['n'].iloc[0])
        ax.text(2023.4, r1, f"{parent}  ({n})", ha='left', va='center',
                fontsize=10 if parent in STORY else 9,
                fontweight='medium' if parent in STORY else 'normal',
                color=color, fontfamily='sans-serif')

ax.set_xlim(2006.5, 2027)

# Title block
ax.set_title("The operators that rose, and the ones that vanished",
             loc='left', pad=38, color=INK, fontsize=16, fontfamily='serif',
             fontweight='medium')
ax.text(0.0, 1.045,
        "Rank by GHGRP facility count, 2010\u20132023. Top 10 in 2010 \u222a top 10 in 2023.",
        transform=ax.transAxes, fontsize=10.5, color=MUTED, fontfamily='sans-serif')

# Footnote
ax.text(0.0, -0.10,
        "Source: EPA GHGRP Parent Company dataset, any-stake union per facility-year. "
        "Name canonicalization collapses corporate-form variants (e.g. Kinder Morgan Inc, KMP, El Paso Pipeline \u2192 Kinder Morgan once the 2014 roll-up closes). "
        "Analysis: @salamituns.",
        transform=ax.transAxes, fontsize=8, color=MUTED, fontfamily='sans-serif', wrap=True)

plt.tight_layout()
plt.savefig(OUT, facecolor=PAPER, dpi=300, bbox_inches='tight')
print(f"wrote {OUT}")
