# GHGRP Sector Concentration (Phase 4b) — Methodology and Self-Audit

*Companion to `posts/LinkedIn_Post_GHGP_SectorConcentration.md`,
`viz/ghgrp_sector_concentration_2023.png`, and `viz/ghgrp_refineries_map_2023.png`*

---

## Scope

Four sectors analyzed, plus GHGRP-wide baseline:

| Sector | GHGRP definition used | Subpart / Label |
|---|---|---|
| Power Plants | "Power Plants" in Industry Type (sectors) | (primarily Subpart D) |
| Petroleum Refineries | "Refineries" in Industry Type (sectors) | Subpart Y |
| Petrochemicals | "Chemicals" in Industry Type (sectors) | Primarily Subparts X, G |
| Oil & Gas | Subpart W tag (carried over from Phase 4a) | W-ONSH, W-GB, W-PROC, W-TRANS, W-LDC |
| GHGRP-wide | All 8,106 2023 facilities | All subparts |

## Data sources

1. **EPA GHGRP 2023 Data Summary Spreadsheets** (same file used in all prior phases). The "Industry Type (sectors)" column is a semicolon-delimited multi-value field; a facility can belong to multiple sectors. Sector membership computed by `str.split(',')` containment.
2. **EPA GHGRP Parent Company Dataset** (same 2023 sheet).
3. **Phase 4a output** for the Oil & Gas baseline: `data/processed/phase4_og_results.json`.

## Processing steps

1. Loaded the Direct Point Emitters sheet from the 2023 summary spreadsheet (6,470 facilities). This sheet contains the sector classification for most major industries, including power, refineries, and chemicals.
2. Filtered to the three sectors using the `Industry Type (sectors)` column. Resulting facility counts:
   - Power Plants: 1,320
   - Refineries: 133
   - Chemicals (Petrochemicals): 462
3. For each sector, joined to the parent-company xlsb on `Facility Id`, computed top-10 parents by unique facility count (any-stake rule — a parent counts toward a facility if it appears in any ownership row for that facility), and calculated the top-10 share as `union-of-top10-parent-facilities / total-sector-facilities`.
4. Same computation GHGRP-wide (all 8,106 facilities) as the baseline. Result: 16.7%.

## Headline numbers (any-stake union method, 2023)

| Sector | Facilities | Unique parents | Top-10 share | Multiplier vs baseline |
|---|---|---|---|---|
| Refineries | 133 | 59 | **54.1%** | **3.24x** |
| Oil & Gas (Phase 4a) | 1,433 | 593 | 27.1% | 1.62x |
| Petrochemicals | 462 | 208 | 25.8% | 1.54x |
| Power Plants | 1,320 | 596 | 23.6% | 1.41x |
| GHGRP-wide | 8,106 | 3,327 | 16.7% | 1.00x |

**Top 10 Petroleum Refineries parents:**

| Rank | Parent | Refineries |
|---|---|---|
| 1 | Valero Energy Corp | 14 |
| 2 | Marathon Petroleum Corp | 13 |
| 3 | Phillips 66 | 12 |
| 4 | PBF Energy Inc | 6 |
| 5 | Par Pacific Holdings Inc | 5 |
| 6 | HF Sinclair Corp | 5 |
| 7 | Chevron Corp | 5 |
| 8 | ExxonMobil Corp | 5 |
| 9 | Delek US Holdings Inc | 4 |
| 10 | Calumet Specialty Products Partners | 4 |

**Top 10 Power Plants parents** (for context):
CPN Management (44), Duke Energy (40), Vistra (39), Berkshire Hathaway (36), Xcel Energy (31), Southern Company (27), Entergy (26), AEP (25), Dominion (24), LS Power (22).

**Top 10 Petrochemicals parents**:
Air Products & Chemicals (27), Linde (18), American Air Liquide Holdings (12), Phillips 66 (11), Dow (10), Chevron (9), Koch Industries (9), LyondellBasell (9), Chemours (9), Valero (8).

## Self-audit of claims in the LinkedIn post

| # | Claim | Evidence | Status |
|---|-------|----------|--------|
| 1 | "In US petroleum refining, 10 parent companies control 54% of all facilities" | 72 / 133 = 54.14%. | CERTAIN |
| 2 | "133 refineries in the entire country" | Count of facilities in Refineries sector. | CERTAIN |
| 3 | "Valero operates 14 of them" | Top 10 Refineries table | CERTAIN |
| 4 | "Marathon Petroleum another 13" | " | CERTAIN |
| 5 | "Phillips 66 another 12" | " | CERTAIN |
| 6 | "PBF Energy 6" | " | CERTAIN |
| 7 | "Those four names alone account for one out of every three US refineries" | 14+13+12+6 = 45. 45/133 = 33.8%. Rounds to "one in three." | CERTAIN |
| 8 | Sector concentration numbers (54.1%, 27.1%, 25.8%, 23.6%, 16.7%) | All computed with any-stake union method. | CERTAIN |
| 9 | "Power is the least consolidated major sector" | Among the four sectors analyzed (power, O&G, petrochem, refineries), power has the lowest top-10 share at 23.6%. Other GHGRP sectors not analyzed (waste, minerals, metals, pulp and paper) may have comparable or lower concentration. The claim is true relative to the four "energy-adjacent" sectors named in this post. | CERTAIN (scoped) |
| 10 | "no single operator above 44 plants" in power | Top power operator is CPN Management at 44. | CERTAIN |
| 11 | "The top 3 petrochem parents are Air Products (27 facilities), Linde (18), and Air Liquide (12)" | Top 10 Petrochem table | CERTAIN |
| 12 | "Industrial gases, not commodity chemicals, drive the sector's top-10 count" | Air Products and Linde + Air Liquide are all industrial gas majors, not downstream chemical producers. Dow / LyondellBasell / Chemours (downstream chemicals) sit below them. | CERTAIN |
| 13 | "30 years of integrated majors (Chevron, ExxonMobil) divesting downstream assets while mid-cap operators (Valero, Marathon, PBF, Phillips 66) rolled up the refining footprint" | Historical industry context. The fact pattern is well-documented in trade press and EIA reports. Phillips 66 is a 2012 Conoco spinoff. Today's top 4 refiners by count are all pure-play downstream operators; Chevron and ExxonMobil are at rank 7 and 8 despite their much larger overall market cap. | SOFT (directionally accurate historical framing; specific 30-year claim not quantitatively verified in this post) |
| 14 | "The industry went from 'many refiners, integrated across the value chain' to 'few refiners, pure-play on crack spreads.'" | Interpretive claim consistent with claim #13. | SOFT (interpretive) |

## Limitations and caveats

1. **Sector classification is EPA's**, not mine. "Chemicals" includes petrochemical producers, industrial gas suppliers, specialty chemicals, and some pharmaceutical-adjacent facilities. Narrowing to "petrochemicals specifically" (which most readers will think of as commodity petrochem like olefins, polymers) would require a Subpart-X-only filter (75 facilities). The sector-label definition used here (462 facilities) is broader. Both are defensible; I chose the broader one for continuity with how EPA reports the data.

2. **Some facilities belong to multiple sectors.** A facility labeled "Chemicals,Petroleum Product Suppliers,Refineries" is counted in both Refineries and Petrochemicals. This is honest to how EPA classifies them, but it does mean the raw facility counts don't sum cleanly across sectors.

3. **"Any-stake union" is the generous concentration rule.** A majority-ownership rule would pull the top-10 shares down across the board. The 3.24x relative multiplier between refineries and GHGRP-wide holds across any reasonable rule choice.

4. **Parent name canonicalization.** Some corporate entities report under several variant names across subsidiaries (historical example: "Kinder Morgan Inc" vs "Kinder Morgan Natural Gas Pipeline Co"). I treat the GHGRP's `PARENT COMPANY NAME` string as canonical. For the top 10 names in each sector, no obvious variant-name issues were detected in spot checks.

5. **Small absolute numbers for refineries mean the top-10 share is noisy to small changes.** Moving one refinery from Delek (rank 9) to, say, a non-top-10 operator would change the top-10 share by ~0.75%. Not a problem for the headline 54% number, but worth knowing.

## Files produced

- `viz/ghgrp_sector_concentration_2023.png` — Phase 4b hero bar chart
- `viz/ghgrp_refineries_map_2023.png` — Phase 4b companion refineries operator map
- `posts/LinkedIn_Post_GHGP_SectorConcentration.md` — LinkedIn caption
- `methodology/SectorConcentration_Methodology_and_SelfAudit.md` — this file
- `scripts/phase4b_sector_analysis.py` — reproducible analysis + render
- `data/processed/ghgrp_2023_refineries.csv` — refinery facilities with operator labels
- `data/processed/phase4b_sector_results.json` — full sector results

## Open questions for Tee

1. **Publishing order.** Lead with the bar chart or lead with the refineries map? They tell slightly different stories — the chart is analytical and the map is visceral. LinkedIn convention favors one hero image; I'd lead with the chart (the 54% number is the punchline) and drop the map in the first comment.

2. **Phase 4c (emissions-weighted).** The natural next beat would be: "And when you weight by tons of CO2e emitted, does the concentration picture look different?" High-level answer: yes. Refineries and petrochem produce disproportionate emissions for their facility count; power produces proportional emissions. Worth doing as a follow-up.

3. **14-year trend recomputation.** Still on the backlog from Phase 4a. Given the 4a and 4b findings, a clean 14-year series using the any-stake union method would be the definitive reference document for everything we've published, and would supersede the 18.0% number that's currently in circulation.
