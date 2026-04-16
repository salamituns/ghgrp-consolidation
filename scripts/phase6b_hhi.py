"""
Phase 6b — Herfindahl-Hirschman Index (HHI) supplement
Bulletproofs the Phase 6 claim that US refining is "highly concentrated" by computing
the actual DOJ-standard HHI for each sector, using both facility count and CO2e weights.

DOJ Horizontal Merger Guidelines (2010) thresholds:
  HHI < 1,500  → unconcentrated
  1,500 ≤ HHI < 2,500  → moderately concentrated
  HHI ≥ 2,500  → highly concentrated
"""
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import openpyxl
from pyxlsb import open_workbook
import json

GEOWORKS = '/sessions/wonderful-amazing-volta/mnt/CoWorker/Geoworks'
RAW_EPA  = f'{GEOWORKS}/data/raw/epa_ghgrp'
PROC     = f'{GEOWORKS}/data/processed'

PATH = f'{RAW_EPA}/2023_data_summary_spreadsheets/ghgp_data_2023.xlsx'

# ---------- 1. Load sheets ----------
def load_sheet(wb, name):
    ws = wb[name]
    rows = list(ws.iter_rows(values_only=True))
    headers = list(rows[3])
    data = [r for r in rows[4:] if r[0] is not None]
    df = pd.DataFrame(data, columns=headers)
    em_col = next((c for c in df.columns if c and str(c).startswith('Total reported')), None)
    if em_col:
        df = df.rename(columns={em_col:'emissions'})
        df['emissions'] = pd.to_numeric(df['emissions'], errors='coerce').fillna(0)
    df['Facility Id'] = pd.to_numeric(df['Facility Id'], errors='coerce').astype('Int64')
    df = df[df['Facility Id'].notna()].copy()
    df['Facility Id'] = df['Facility Id'].astype(int)
    return df

wb = openpyxl.load_workbook(PATH, read_only=True, data_only=True)
dpe = load_sheet(wb, 'Direct Point Emitters')
w_ong = load_sheet(wb, 'Onshore Oil & Gas Prod.')
w_gb  = load_sheet(wb, 'Gathering & Boosting')
w_trn = load_sheet(wb, 'Transmission Pipelines')
w_ldc = load_sheet(wb, 'LDC - Direct Emissions')
wb.close()

def has_sector(s, sector):
    return sector in str(s or '').split(',')
dpe['is_power']   = dpe['Industry Type (sectors)'].apply(lambda s: has_sector(s, 'Power Plants'))
dpe['is_refinery']= dpe['Industry Type (sectors)'].apply(lambda s: has_sector(s, 'Refineries'))
dpe['is_chem']    = dpe['Industry Type (sectors)'].apply(lambda s: has_sector(s, 'Chemicals'))

def og_facility_set():
    """Build unique O&G (Subpart W) facility → emissions map."""
    og_em_frames = [
        w_ong[['Facility Id','emissions']],
        w_gb [['Facility Id','emissions']],
        w_trn[['Facility Id','emissions']],
        w_ldc[['Facility Id','emissions']],
    ]
    wproc_mask = dpe['Industry Type (subparts)'].astype(str).str.contains('W-PROC', na=False)
    og_em_frames.append(dpe[wproc_mask][['Facility Id','emissions']])
    og = pd.concat(og_em_frames, ignore_index=True)
    return og.groupby('Facility Id', as_index=False).sum()

power_em    = dpe[dpe['is_power']   ][['Facility Id','emissions']].groupby('Facility Id',as_index=False).sum()
refinery_em = dpe[dpe['is_refinery']][['Facility Id','emissions']].groupby('Facility Id',as_index=False).sum()
chem_em     = dpe[dpe['is_chem']    ][['Facility Id','emissions']].groupby('Facility Id',as_index=False).sum()
og_em       = og_facility_set()
all_em      = pd.concat([
    dpe[['Facility Id','emissions']],
    w_ong[['Facility Id','emissions']], w_gb[['Facility Id','emissions']],
    w_trn[['Facility Id','emissions']], w_ldc[['Facility Id','emissions']],
], ignore_index=True).groupby('Facility Id', as_index=False).sum()

# ---------- 2. Parent ownership ----------
with open_workbook(f'{RAW_EPA}/ghgp_data_parent_company.xlsb') as pwb:
    with pwb.get_sheet('2023') as sheet:
        rows = list(sheet.rows())
        headers = [c.v for c in rows[0]]
        data = [[c.v for c in r] for r in rows[1:]]
parent = pd.DataFrame(data, columns=headers)
parent = parent.dropna(subset=['GHGRP FACILITY ID','PARENT COMPANY NAME']).copy()
parent['GHGRP FACILITY ID'] = parent['GHGRP FACILITY ID'].astype(int)
parent['pct'] = pd.to_numeric(parent['PARENT CO. PERCENT OWNERSHIP'], errors='coerce')

def allocate(parent_df, facility_df, weight_col):
    """
    Ownership-weighted allocation of a per-facility weight (count=1 or emissions tons)
    to each parent. Returns per-parent weighted share and the shares vector.
    """
    df = parent_df.merge(facility_df.rename(columns={'Facility Id':'GHGRP FACILITY ID'}),
                         on='GHGRP FACILITY ID', how='inner')
    # Ownership-percentage split (normalized per facility)
    total_pct = df.groupby('GHGRP FACILITY ID')['pct'].transform('sum')
    n_rows    = df.groupby('GHGRP FACILITY ID')['pct'].transform('size')
    share     = df['pct'] / total_pct.replace(0, pd.NA)
    share     = share.fillna(1.0 / n_rows)
    df['attributed'] = df[weight_col] * share
    by_parent = df.groupby('PARENT COMPANY NAME')['attributed'].sum()
    total = df.drop_duplicates('GHGRP FACILITY ID')[weight_col].sum()
    pct_shares = (100.0 * by_parent / total).sort_values(ascending=False)
    return pct_shares, total

def hhi(share_series_pct):
    """HHI = sum of (percentage share)^2. Returns unitless integer-range value."""
    return float((share_series_pct ** 2).sum())

def categorize(h):
    if h < 1500: return 'Unconcentrated'
    if h < 2500: return 'Moderately concentrated'
    return 'Highly concentrated'

# Build facility-count "weight column" = 1 per facility
power_cnt    = power_em.assign(count=1)[['Facility Id','count']]
refinery_cnt = refinery_em.assign(count=1)[['Facility Id','count']]
chem_cnt     = chem_em.assign(count=1)[['Facility Id','count']]
og_cnt       = og_em.assign(count=1)[['Facility Id','count']]
all_cnt      = all_em.assign(count=1)[['Facility Id','count']]

results = {}
for label, fac_em, fac_cnt in [
    ('Refineries',     refinery_em, refinery_cnt),
    ('Oil & Gas',      og_em,       og_cnt),
    ('Petrochemicals', chem_em,     chem_cnt),
    ('Power Plants',   power_em,    power_cnt),
    ('GHGRP-wide',     all_em,      all_cnt),
]:
    # facility-count HHI (ownership-weighted share of facilities)
    cnt_shares, _ = allocate(parent, fac_cnt, 'count')
    cnt_hhi = hhi(cnt_shares)

    # emissions-weighted HHI
    em_shares, _ = allocate(parent, fac_em, 'emissions')
    em_hhi = hhi(em_shares)

    print(f"\n{label}:")
    print(f"  Facility-count HHI:     {cnt_hhi:>7,.0f}  ({categorize(cnt_hhi)})")
    print(f"  Emissions-weighted HHI: {em_hhi:>7,.0f}  ({categorize(em_hhi)})")
    print(f"  Top 3 by emissions: {', '.join(f'{n} ({v:.1f}%)' for n,v in em_shares.head(3).items())}")

    results[label] = {
        'count_hhi': cnt_hhi,
        'count_hhi_category': categorize(cnt_hhi),
        'emissions_hhi': em_hhi,
        'emissions_hhi_category': categorize(em_hhi),
        'top3_by_emissions': {n: float(v) for n, v in em_shares.head(3).items()},
    }

with open(f'{PROC}/phase6b_hhi_results.json', 'w') as f:
    json.dump({
        'doj_thresholds': {
            'unconcentrated_below': 1500,
            'moderately_concentrated_range': [1500, 2500],
            'highly_concentrated_above': 2500,
            'source': 'DOJ Horizontal Merger Guidelines (2010)',
        },
        'sectors': results,
    }, f, indent=2)
print(f"\nSaved: {PROC}/phase6b_hhi_results.json")
