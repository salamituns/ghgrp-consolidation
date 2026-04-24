"""
Phase 10 / Fig 13 prep + render \u2014 state-level net change in GHGRP reporter
facility count, 2010 \u2192 2023.

Reads the XLSB parent-company panel, extracts distinct facility-state pairs
per reporting year (to avoid JV double-counting), computes 2023 \u2212 2010 per
state, and renders a diverging choropleth in the editorial palette.

Diverging palette rationale: facility *count* can move either direction
(states gain or lose reporters as categories open/close, or as facilities
shut down). Clay = gain, ink/muted = loss, near-white = no change.
"""
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pyxlsb import open_workbook

RAW_XLSB = '/Users/olatunde/CoWorker/Geoworks/data/raw/epa_ghgrp/ghgp_data_parent_company.xlsb'
STATES_GEOJSON = '/Users/olatunde/CoWorker/Geoworks/data/raw/census_boundaries/gz_2010_us_040_00_5m.json'
OUT = '/Users/olatunde/CoWorker/Geoworks/salamituns.github.io/ghgrp/figures/ghgrp_state_delta_choropleth.png'

PAPER = '#F6F3EB'
INK = '#0E0E0E'
CLAY = '#A23B2A'
MUTED = '#7A7368'
FAINT = '#E4DFD3'

EXCLUDE_STATES = {'Alaska', 'Hawaii', 'Puerto Rico'}

# ---- Load 2010 and 2023 from XLSB ----------------------------------------
def read_year(year: int) -> pd.DataFrame:
    with open_workbook(RAW_XLSB) as wb:
        with wb.get_sheet(str(year)) as sheet:
            rows = list(sheet.rows())
            headers = [c.v for c in rows[0]]
            data = [[c.v for c in r] for r in rows[1:]]
    df = pd.DataFrame(data, columns=headers)
    df = df.dropna(subset=['GHGRP FACILITY ID', 'FACILITY STATE']).copy()
    df['GHGRP FACILITY ID'] = df['GHGRP FACILITY ID'].astype(int)
    df['FACILITY STATE'] = df['FACILITY STATE'].astype(str).str.strip().str.upper()
    return df[['GHGRP FACILITY ID', 'FACILITY STATE']].drop_duplicates()

print('Reading 2010...')
y10 = read_year(2010)
print(f'  facilities: {y10["GHGRP FACILITY ID"].nunique()}')
print('Reading 2023...')
y23 = read_year(2023)
print(f'  facilities: {y23["GHGRP FACILITY ID"].nunique()}')

# Per-state unique-facility counts
c10 = y10.drop_duplicates().groupby('FACILITY STATE')['GHGRP FACILITY ID'].nunique().rename('n2010')
c23 = y23.drop_duplicates().groupby('FACILITY STATE')['GHGRP FACILITY ID'].nunique().rename('n2023')
states_df = pd.concat([c10, c23], axis=1).fillna(0).astype(int)
states_df['delta'] = states_df['n2023'] - states_df['n2010']
states_df['pct'] = (states_df['delta'] / states_df['n2010'].replace(0, pd.NA)) * 100

# ---- Merge with state polygons -------------------------------------------
# Census uses two-letter state codes sometimes, full names others. Canonicalise
# to USPS code via a lookup.
USPS = {
    'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA',
    'Colorado':'CO','Connecticut':'CT','Delaware':'DE','District of Columbia':'DC',
    'Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL',
    'Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA',
    'Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN',
    'Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV',
    'New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY',
    'North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR',
    'Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD',
    'Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA',
    'Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY',
    'Puerto Rico':'PR'
}

states = gpd.read_file(STATES_GEOJSON)
states = states[~states['NAME'].isin(EXCLUDE_STATES)].copy()
states['USPS'] = states['NAME'].map(USPS)
states = states.merge(states_df, how='left', left_on='USPS', right_index=True)
states['delta'] = states['delta'].fillna(0)

# Print top gainers / losers
print('\nTop 6 gainers:')
print(states_df.sort_values('delta', ascending=False).head(6))
print('\nTop 6 losers:')
print(states_df.sort_values('delta').head(6))

# ---- Build diverging colormap --------------------------------------------
vmax = float(states['delta'].abs().quantile(0.95))
vmin = -vmax

LOSS = '#3C5069'      # cool slate
ZERO = '#EFE8D6'      # near-paper
GAIN = CLAY
cmap = mcolors.LinearSegmentedColormap.from_list(
    'editorial_div', [(0.0, LOSS), (0.5, ZERO), (1.0, GAIN)], N=256
)
norm = mcolors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

# ---- Render ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 7.4), dpi=300, facecolor=PAPER)
ax.set_facecolor(PAPER)

states.plot(
    ax=ax,
    column='delta',
    cmap=cmap, norm=norm,
    edgecolor=PAPER, linewidth=0.6,
    missing_kwds={'color': FAINT, 'edgecolor': PAPER, 'linewidth': 0.6},
)

# Extent \u2014 CONUS
ax.set_xlim(-126, -66)
ax.set_ylim(23.5, 50)
ax.set_aspect(1.3)
ax.set_xticks([]); ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# Annotate the four most interesting states (top 2 gainers + top 2 losers)
gainers = states_df.sort_values('delta', ascending=False).head(2)
losers = states_df.sort_values('delta').head(2)
annots = []
for code, row in gainers.iterrows():
    annots.append((code, int(row['delta']), 'gain'))
for code, row in losers.iterrows():
    annots.append((code, int(row['delta']), 'loss'))

# Centroids for labels
states['centroid'] = states.geometry.representative_point()
for code, delta, _ in annots:
    r = states[states['USPS'] == code]
    if r.empty: continue
    pt = r.iloc[0]['centroid']
    sign = '+' if delta > 0 else ''
    ax.annotate(f"{code}  {sign}{delta}",
                xy=(pt.x, pt.y), xytext=(0, 0), textcoords='offset points',
                ha='center', va='center',
                fontsize=10, color=INK, fontfamily='sans-serif', fontweight='medium',
                bbox=dict(boxstyle='round,pad=0.25', facecolor=PAPER, edgecolor=INK,
                          linewidth=0.4, alpha=0.9))

# ---- Title block ---------------------------------------------------------
fig.text(0.035, 0.95,
         "Who gained reporters, and who lost them.",
         fontsize=18, color=INK, fontfamily='serif', fontweight='medium')
fig.text(0.035, 0.915,
         "Net change in GHGRP reporter facility count by state, 2010\u20132023. "
         "A gain means the state has more reporters subject to federal emissions disclosure; "
         "a loss means fewer.",
         fontsize=10.5, color=MUTED, fontfamily='sans-serif')

# ---- Legend / color bar --------------------------------------------------
cax = fig.add_axes([0.035, 0.08, 0.23, 0.018])
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm); sm.set_array([])
cb = fig.colorbar(sm, cax=cax, orientation='horizontal')
cb.outline.set_visible(False)
cb.ax.tick_params(colors=INK, labelsize=9, length=0, pad=3)
cb.set_ticks([int(vmin), 0, int(vmax)])
cb.set_ticklabels([f"{int(vmin):+d}", "0", f"{int(vmax):+d}"])
fig.text(0.035, 0.115, 'Facility count change, 2010 \u2192 2023',
         fontsize=9, color=MUTED, fontfamily='sans-serif')

# ---- Footnote ------------------------------------------------------------
fig.text(0.035, 0.02,
         "Source: EPA GHGRP Parent Company dataset, 2010 and 2023 reporting years.  "
         "Per-state counts are unique GHGRP Facility IDs; JV double-counts collapsed.  "
         "Color scale is clipped at the 95th percentile of |\u0394| to keep the range legible.  "
         "Analysis: @salamituns.",
         fontsize=8, color=MUTED, fontfamily='sans-serif')

plt.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.05)
plt.savefig(OUT, facecolor=PAPER, dpi=300, bbox_inches='tight')
print(f"\nwrote {OUT}")
