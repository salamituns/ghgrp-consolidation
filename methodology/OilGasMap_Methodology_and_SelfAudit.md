# GHGRP Oil & Gas Map (Phase 4a) — Methodology and Self-Audit

*Companion to `posts/LinkedIn_Post_GHGP_OilGas.md` and `viz/ghgrp_oilgas_map_2023.png`*

---

## Scope

"Oil and Gas" in this post = **GHGRP Subpart W (Petroleum and Natural Gas Systems)**. This covers:

- **W-ONSH**: Onshore oil and gas production (basin-level reporting)
- **W-GB**: Gathering and boosting (midstream collection)
- **W-PROC**: Natural gas processing plants (sits in the "Direct Point Emitters" sheet, identified by the `W-PROC` tag in the subparts column)
- **W-TRANS**: Transmission compression (pipeline compressor stations)
- **W-LDC**: Local distribution companies (utility-level gas distribution)

**Not included in this post** (deferred to Phase 4b): petroleum refineries (Subpart Y), petrochemicals (Subpart X), power plants (Subpart D). Each is a distinct regulatory category and deserves its own analysis.

Facility count check:

| Subpart | Sheet | Facilities |
|---|---|---|
| W-ONSH | Onshore Oil & Gas Prod. | 445 |
| W-PROC | Direct Point Emitters (filtered) | 445 |
| W-GB | Gathering & Boosting | 349 |
| W-LDC | LDC - Direct Emissions | 157 |
| W-TRANS | Transmission Pipelines | 37 |
| **Total unique** | | **1,433** |

(Facilities that report under multiple subparts are deduplicated in the total.)

## Data sources

1. **EPA GHGRP 2023 Data Summary Spreadsheets** — identifies which facilities report under Subpart W.
2. **EPA GHGRP Parent Company Dataset** — 2023 ownership records (any-stake ownership row per facility × parent pair).
3. **Census Cartographic Boundary File** — state outlines (5m resolution) for basemap.

## Processing steps

1. Scanned five sheets of the 2023 summary spreadsheet to collect Subpart W facility IDs. For Natural Gas Processing (W-PROC), the facility sits in the "Direct Point Emitters" sheet and was identified by the `W-PROC` token in its subparts column.
2. Joined the 1,433 Subpart W facility IDs to the 2023 parent-company table.
3. Computed **top 10 O&G parent companies by unique facility count, any-stake rule**: a facility counts toward a parent if that parent appears in any ownership row for the facility, regardless of ownership percentage. Joint-venture facilities count in multiple parents' totals.
4. Computed **top 10 share** = share of unique O&G facilities in which any top-10 parent holds an ownership stake.
5. Computed the same metric GHGRP-wide as a comparison baseline, using identical methodology.
6. Assigned each facility a display label for the map: if any top-10 O&G parent owns a stake, use that parent's name (rank-order priority: rank 1 wins over rank 2 in co-ownership cases); otherwise label as "other."

## Headline numbers

| Metric | Value |
|---|---|
| Unique O&G facilities (Subpart W) | 1,433 |
| Unique O&G parent companies | 593 |
| Top 10 O&G parents — share of O&G facilities | **27.1%** |
| Top 10 GHGRP-wide parents — share of all GHGRP facilities (same method) | **16.7%** |
| O&G concentration multiplier | **1.62x GHGRP-wide** |
| O&G facilities with coordinates | 1,432 of 1,433 (99.9%) |

**Top 10 O&G parents (2023):**

| Rank | Parent | Facilities |
|---|---|---|
| 1 | Energy Transfer LP | 89 |
| 2 | Kinder Morgan Inc | 45 |
| 3 | Phillips 66 | 44 |
| 4 | Targa Resources Corp | 44 |
| 5 | Enterprise Products Partners LP | 44 |
| 6 | Enbridge (US) Inc | 40 |
| 7 | ExxonMobil Corp | 35 |
| 8 | Williams Cos Inc | 34 |
| 9 | MPLX LP | 33 |
| 10 | EOG Resources Inc | 30 |

**Overlap with GHGRP-wide top 10**: 5 names shared (Energy Transfer, Kinder Morgan, Phillips 66, Enterprise Products, Williams). **5 are O&G-specific**: Targa, Enbridge US, ExxonMobil, MPLX, EOG. These are the companies with footprints large inside oil and gas but small enough on the rest of the reporting program to miss the overall top 10.

## Self-audit of claims in the LinkedIn post

| # | Claim | Evidence | Status |
|---|-------|----------|--------|
| 1 | "Top 10 parent companies control 27.1% of facilities in the oil and gas sector" | Any-stake union = 388 / 1,433 = 27.07% | CERTAIN |
| 2 | "GHGRP-wide, the same metric is 16.7%" | Any-stake union = 1,357 / 8,106 = 16.74% | CERTAIN |
| 3 | "roughly 1.6x more concentrated" | 27.07 / 16.74 = 1.617. Rounded to 1.6x. | CERTAIN |
| 4 | Facility counts per operator (89, 45, 44, 44, 44, 40, 35, 34, 33, 30) | Direct from computation | CERTAIN |
| 5 | "Targa Resources — Permian and Gulf Coast gathering and processing" | General industry knowledge; the map shows Targa dots concentrated in TX. | SOFT (descriptive, not quantified) |
| 6 | "Enbridge US — the American arm of Canada's largest pipeline company" | Factual industry knowledge. | CERTAIN |
| 7 | "MPLX — Marathon Petroleum's midstream MLP" | Factual; MPLX is structured as Marathon's midstream subsidiary. | CERTAIN |
| 8 | "EOG Resources — pure-play Permian and Eagle Ford producer" | General industry knowledge; map shows EOG concentrated in west Texas. | SOFT (descriptive) |
| 9 | "The Permian is multi-operator" | Visible in map; not quantified in post. Basin-level concentration analysis would be a follow-up. | CERTAIN (visual), UNCERTAIN (not ranked) |
| 10 | "Williams and MPLX dominate the Marcellus/Utica" | Visible in map; not quantified. | CERTAIN (visual), UNCERTAIN (not ranked) |
| 11 | "The non-top-10 long tail is 73%" | 100% - 27.1% = 72.9%. Rounds to 73%. | CERTAIN |

## Known discrepancies with prior published work

**The prior GHGRP LinkedIn post and Substack cited "18.0%" as the top-10 GHGRP-wide concentration share.** My reproducible calculation using the any-stake union method yields **16.7%**. The 18.0% figure in `scripts/build_charts.py` appears to have been hardcoded from an earlier analysis whose methodology is not documented in this repo.

For Phase 4, both the O&G figure (27.1%) and the GHGRP-wide comparison (16.7%) use the identical any-stake union method. The internal consistency is what supports the "1.6x" multiplier claim. A reader who believes the 18.0% figure from the prior post would compute a slightly different multiplier (27.1 / 18.0 = 1.5x) — the story holds either way.

**If you want this resolved**: compute the 14-year trend using the any-stake union method to produce a single authoritative number series and supersede `build_charts.py`'s hardcoded 18.0%. That's a 30-minute job whenever you want it.

## Limitations and caveats

1. **"Any-stake" counting is generous.** A parent company with a 1% passive stake in a facility counts the same as a parent with 100% ownership for the facility-count share metric. A stricter "majority owner" rule would likely push the O&G top-10 share down by a few percentage points. The story (O&G more concentrated than GHGRP-wide) is robust to the choice.

2. **Joint ventures are counted in multiple parents.** The sum of the top 10's individual facility counts (430) exceeds the union (388) by 42 facilities — these are JVs where two or more top-10 parents co-own. That's why the union is the honest headline metric, and why the "1.6x" comparison uses union on both sides.

3. **Facility count ≠ emissions volume.** A compressor station reports as one facility; a large natural gas processing plant also reports as one. This analysis treats them equally. An emissions-weighted concentration metric (using CO2e tonnage, which is in the same summary spreadsheet) would be a separate and complementary story.

4. **W-PROC facilities may also report under other subparts.** A natural gas processing plant often also reports fuel combustion (Subpart C) or flaring. I tagged it as W-PROC based on the subparts column, but the same physical facility has a multi-subpart reporting profile. Total count of 1,433 is a conservative union of W-tagged facilities.

5. **One facility is missing coordinates.** Of 1,433 Subpart W facilities, 1,432 have lat/long from the summary spreadsheet. The one missing facility is excluded from the map only, not from the concentration calculation.

## Files produced

- `viz/ghgrp_oilgas_map_2023.png` — Phase 4a map
- `posts/LinkedIn_Post_GHGP_OilGas.md` — LinkedIn caption
- `methodology/OilGasMap_Methodology_and_SelfAudit.md` — this file
- `scripts/phase4_og_analysis.py` — reproducible analysis + render
- `data/processed/ghgrp_2023_og_facilities.csv` — facility-level O&G dataset with owner labels
- `data/processed/phase4_og_results.json` — structured summary of all numbers

## Open questions for Tee

1. **The 18% vs 16.7% discrepancy.** Want me to recompute the published 14-year time series using the any-stake union method to produce a single authoritative number? Would supersede `build_charts.py`'s hardcoded figures.

2. **Emissions-weighted variant.** I can produce the same map and concentration metric but weighted by reported CO2e tonnage per facility instead of facility count. Different story, same data. Worth doing as Phase 4a.2 or holding?

3. **Basin-level drill-down.** The Permian vs. Appalachia vs. Bakken story deserves its own chart. Could be a natural next step either as standalone content or as part of the Phase 4b rollout.

4. **Phase 4b timing.** Ready to proceed with power + refineries + petrochemicals when you are. Each has its own subpart structure (D for power, Y for refineries, X for petrochem) but the methodology slot-in cleanly.
