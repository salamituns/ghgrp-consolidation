"""
Phase 5 — 14-Year Concentration Trend Recomputation
Recomputes the top-10 parent-company concentration share for every year 2010-2023
using the any-stake union method. Supersedes the hardcoded 11.7% / 18.0% numbers
from the initial published analysis.
"""
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import matplotlib.pyplot as plt
from pyxlsb import open_workbook
import json

GEOWORKS = '/sessions/wonderful-amazing-volta/mnt/CoWorker/Geoworks'
RAW_EPA  = f'{GEOWORKS}/data/raw/epa_ghgrp'
PROC     = f'{GEOWORKS}/data/processed'
VIZ      = f'{GEOWORKS}/viz'

# ---------- 1. Iterate over every year sheet in the parent company xlsb ----------
rows_all = []
YEARS = list(range(2010, 2024))

with open_workbook(f'{RAW_EPA}/ghgp_data_parent_company.xlsb') as wb:
    for year in YEARS:
        with wb.get_sheet(str(year)) as sheet:
            srows = list(sheet.rows())
            headers = [c.v for c in srows[0]]
            data = [[c.v for c in r] for r in srows[1:]]
        df = pd.DataFrame(data, columns=headers)
        df = df.dropna(subset=['GHGRP FACILITY ID', 'PARENT COMPANY NAME']).copy()
        df['GHGRP FACILITY ID'] = df['GHGRP FACILITY ID'].astype(int)
        total_facilities = df['GHGRP FACILITY ID'].nunique()
        total_parents = df['PARENT COMPANY NAME'].nunique()
        by_parent = df.groupby('PARENT COMPANY NAME')['GHGRP FACILITY ID'].nunique().sort_values(ascending=False)
        top10 = by_parent.head(10)
        top10_names = list(top10.index)
        top10_facility_set = set(df[df['PARENT COMPANY NAME'].isin(top10_names)]['GHGRP FACILITY ID'])
        top10_share = 100 * len(top10_facility_set) / total_facilities
        rows_all.append({
            'year': year,
            'total_facilities': int(total_facilities),
            'total_parents': int(total_parents),
            'top10_share_pct': float(top10_share),
            'top10_facilities_sum': int(top10.sum()),  # sum-of-counts (double-count JVs)
            'top10_names': top10_names,
            'top10_counts': [int(x) for x in top10.values],
        })
        print(f"{year}: {total_facilities} facilities, {total_parents} parents, top-10 share = {top10_share:.2f}%")

trend = pd.DataFrame(rows_all)
trend.to_csv(f'{PROC}/phase5_14yr_trend.csv', index=False)

# Save the full structured output
with open(f'{PROC}/phase5_14yr_trend.json', 'w') as f:
    json.dump(rows_all, f, indent=2)

# ---------- 2. Derived stats for narrative ----------
pub_2010 = 11.7  # from published Substack/LinkedIn
pub_2023 = 18.0  # from published Substack/LinkedIn

my_2010 = trend[trend['year']==2010]['top10_share_pct'].iloc[0]
my_2023 = trend[trend['year']==2023]['top10_share_pct'].iloc[0]
delta_recomputed = my_2023 - my_2010
relative_growth_recomputed = (my_2023 / my_2010 - 1) * 100

print(f"\n14-year change (recomputed, any-stake union):")
print(f"  2010: {my_2010:.1f}%")
print(f"  2023: {my_2023:.1f}%")
print(f"  Absolute delta: +{delta_recomputed:.1f} pp")
print(f"  Relative growth: +{relative_growth_recomputed:.0f}%")

print(f"\nPublished (from prior Substack / LinkedIn):")
print(f"  2010: {pub_2010}%  (diff: {my_2010-pub_2010:+.1f} pp)")
print(f"  2023: {pub_2023}%  (diff: {my_2023-pub_2023:+.1f} pp)")
print(f"  Published absolute delta: +{pub_2023-pub_2010:.1f} pp")
print(f"  Published relative growth: +{(pub_2023/pub_2010-1)*100:.0f}%")

# Top-10 turnover: how often do names appear across 14 years?
name_years = {}
for r in rows_all:
    for n in r['top10_names']:
        name_years.setdefault(n, []).append(r['year'])

persistent = sorted([(n, len(ys)) for n, ys in name_years.items()], key=lambda x: -x[1])
print(f"\nTop-10 persistence (how many years a parent was in the top 10):")
for name, years_in in persistent[:20]:
    print(f"  {years_in:>2d} yrs — {name}")

persistent_14 = [n for n, ys in name_years.items() if len(ys) == 14]
print(f"\n{len(persistent_14)} parents appeared in top 10 every year 2010-2023: {persistent_14}")

# ---------- 3. Render the trend chart ----------
fig, ax = plt.subplots(figsize=(14, 8), dpi=150)
fig.patch.set_facecolor('#fafafa')
ax.set_facecolor('#fafafa')

xs = trend['year'].values
ys_recomp = trend['top10_share_pct'].values

# Trend line — clean, no correction comparison
ax.plot(xs, ys_recomp, color='#c8292c', linewidth=3.0, zorder=3)
ax.scatter(xs, ys_recomp, s=70, color='#c8292c', edgecolor='white',
           linewidth=1.5, zorder=4)

# Endpoint labels
ax.annotate(f'{my_2010:.1f}%', xy=(2010, my_2010), xytext=(2010-0.3, my_2010+0.7),
            fontsize=12, fontweight='bold', color='#111')
ax.annotate(f'{my_2023:.1f}%', xy=(2023, my_2023), xytext=(2023-0.8, my_2023+0.7),
            fontsize=12, fontweight='bold', color='#111')

# 2015 annotation (the "vanishing act" year from published analysis)
ax.axvspan(2014.5, 2015.5, color='#f0c040', alpha=0.15, zorder=1)
ax.annotate('2015:\nparent-co\nreclassification',
            xy=(2015, trend[trend['year']==2015]['top10_share_pct'].iloc[0]),
            xytext=(2015.3, 13.2), fontsize=9, color='#7a5a00',
            arrowprops=dict(arrowstyle='->', color='#aa8030', lw=0.8),
            ha='left')

# Axes
ax.set_xlim(2009.5, 2023.8)
ax.set_ylim(9.5, 19.0)
ax.set_xlabel('Reporting year', fontsize=11, color='#333', labelpad=10)
ax.set_ylabel('Top-10 parent share of GHGRP facilities (%)',
              fontsize=11, color='#333', labelpad=10)
ax.set_xticks(xs)
ax.tick_params(axis='both', labelsize=10, colors='#444')
ax.grid(True, axis='y', linestyle='-', alpha=0.25, color='#aaa')
for spine in ['top','right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#bbb')
ax.spines['bottom'].set_color('#bbb')

# Title
fig.text(0.05, 0.95, 'Industrial emissions ownership concentrated over 14 years',
         fontsize=20, fontweight='bold', color='#111')
fig.text(0.05, 0.915,
         f'Top 10 parent companies went from {my_2010:.1f}% of GHGRP-reporting facilities in 2010 to {my_2023:.1f}% in 2023. A {delta_recomputed:.1f} percentage-point absolute gain, {relative_growth_recomputed:.0f}% relative.',
         fontsize=11.5, color='#444')

# Footer
fig.text(0.05, 0.055,
         'Source: EPA GHGRP Parent Company Dataset, annual sheets 2010-2023.',
         fontsize=8.5, color='#666')
fig.text(0.05, 0.035,
         'Methodology: for each year, top-10 parents selected by unique facility count. Top-10 share = share of unique facilities in which any top-10 parent holds an ownership stake (any-stake union rule).',
         fontsize=8.5, color='#666')
fig.text(0.05, 0.015,
         'Analysis: @salamituns  |  Stratdevs (Tareony)',
         fontsize=9, color='#888', style='italic')

plt.subplots_adjust(left=0.08, right=0.97, top=0.86, bottom=0.14)

OUT = f'{VIZ}/ghgrp_14yr_trend_recomputed.png'
plt.savefig(OUT, dpi=200, bbox_inches='tight', facecolor='#fafafa')
print(f"\nSaved: {OUT}")
plt.close()

# Save comparison summary
with open(f'{PROC}/phase5_comparison_summary.json', 'w') as f:
    json.dump({
        'methodology': 'any-stake union: facility counts toward a parent if parent appears in any ownership row',
        'recomputed_2010_pct': float(my_2010),
        'recomputed_2023_pct': float(my_2023),
        'recomputed_absolute_delta_pp': float(delta_recomputed),
        'recomputed_relative_growth_pct': float(relative_growth_recomputed),
        'published_2010_pct': pub_2010,
        'published_2023_pct': pub_2023,
        'published_absolute_delta_pp': pub_2023 - pub_2010,
        'published_relative_growth_pct': (pub_2023/pub_2010-1)*100,
        'diff_2010_pp': float(my_2010 - pub_2010),
        'diff_2023_pp': float(my_2023 - pub_2023),
        'year_by_year': [{'year': r['year'], 'top10_share_pct': r['top10_share_pct']} for r in rows_all],
        'top10_persistence': {n: len(ys) for n, ys in name_years.items()},
    }, f, indent=2)
print(f"Saved comparison summary.")
