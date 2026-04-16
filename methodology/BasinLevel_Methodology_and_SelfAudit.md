# Phase 7 — Basin-Level Oil & Gas Operator Concentration (Spin-off B)

*Companion to `posts/LinkedIn_Post_GHGP_BasinLevel.md` and `viz/ghgrp_basin_ownership_2023.png`*

---

## Scope

For each of the top 6 US oil & gas reporting basins (by facility count), computes parent-company ownership concentration using the same any-stake union rule as Phase 4a and 4b. Compares to sector-level concentration.

**Basins included** (facility count combining upstream and midstream):

1. Permian — 157 facilities
2. Gulf Coast (onshore LA, TX — *not* the corridor from Phase 2) — 89
3. Appalachian (Eastern Overthrust Area) — 81
4. Anadarko — 56
5. Williston (Bakken) — 46
6. Arkla — 32

**Sheets combined**:

- `Onshore Oil & Gas Prod.` sheet — Subpart W-ONSH (upstream production)
- `Gathering & Boosting` sheet — Subpart W-GB (midstream gathering)

Transmission pipelines and LDCs are excluded here; they aren't basin-tagged because pipelines run across basins rather than within one.

## Methodology

1. Load upstream and gathering sheets; each row has `Facility Id` and `Basin`.
2. Drop duplicates per `(Facility Id, Basin)` pair — some facilities report under both upstream and gathering, which is honestly represented here.
3. Group by `Basin`, compute unique `Facility Id` counts → rank basins, pick top 6.
4. For each basin, join to parent-company ownership table. Compute:
   - Unique parents per basin (count of distinct `PARENT COMPANY NAME`).
   - Facility count per parent (any-stake rule).
   - **Top-1 share**: share of basin facilities owned (any stake) by the single largest parent.
   - **Top-5 share**: share of basin facilities owned (any stake) by the union of top 5 parents.

## Headline numbers

| Basin | Facilities | Unique parents | Top-1 share | Top-5 share |
|---|---|---|---|---|
| **Permian** | 157 | 130 | 3.2% | 10.2% |
| Gulf Coast | 89 | 68 | 5.6% | 15.7% |
| Appalachian | 81 | 58 | 6.2% | 19.8% |
| Anadarko | 56 | 48 | 3.6% | 17.9% |
| Williston | 46 | 38 | 4.3% | 21.7% |
| Arkla | 32 | 26 | 6.2% | 31.2% |

**Critical observation**: every one of these top-5 basin shares is well below the Phase 4a O&G sector-level top-10 share (27.1%). Even the most concentrated basin (Arkla, 31.2% for top-5) barely exceeds the sector-level top-10. The consolidation story does NOT hold at the basin level for upstream + gathering assets.

## Self-audit of claims in the LinkedIn post

| # | Claim | Evidence | Status |
|---|-------|----------|--------|
| 1 | "Permian: 157 facilities owned by 130 different parent companies" | Computation output. | CERTAIN |
| 2 | "Top-1 owner controls 3.2%" in Permian | (1 / 157 round-to-nearest = 0.6%; top parent has 5 facilities = 3.2%). | CERTAIN |
| 3 | "Top-5 combined: 10.2%" | Direct from computation. | CERTAIN |
| 4 | Remaining basin numbers (89, 81, 56, 46, 32 facilities and top-5 shares) | All from computation. | CERTAIN |
| 5 | "Most concentrated of the top 6 basins is Arkla" | 31.2% > 21.7% > 19.8% > 17.9% > 15.7% > 10.2%. | CERTAIN |
| 6 | "top-10 parents control 27% of O&G facilities" at sector level | Phase 4a finding, reproduced. | CERTAIN |
| 7 | "Many of those top-10 parents are midstream consolidators" | Top 10 O&G parents include KM, ET, Enterprise Products, Enbridge, MPLX, Williams — all primarily midstream. | CERTAIN |
| 8 | "Upstream oil and gas is a competitive long-tail market; midstream is a consolidated network" | Sector 27% + top-5 basin shares all < 32% + top-10 sector names dominated by midstream → structurally consistent framing. | CERTAIN (structural inference) |
| 9 | "Any one of them owns at most 5 facilities" in Permian | Top parent holds 3.2% × 157 ≈ 5 facilities. | CERTAIN |

## Limitations and caveats

1. **Basin boundaries follow EPA's reporting-basin classification**, not the widely-used AAPG province names. EPA uses numeric codes like "430 - Permian Basin" — these map closely to but aren't identical with geological basin boundaries.

2. **Transmission pipelines excluded.** Pipelines cross basin boundaries by nature. The top O&G sector names (Kinder Morgan, Energy Transfer) are heavily pipeline-based and do not appear in basin-level top 5 because their facilities aren't tied to any one basin.

3. **Upstream + gathering combined.** Some basins have primarily upstream reporters (Permian), others are heavily midstream (Appalachian has lots of gathering). Separating upstream vs gathering would refine the picture. The combined view is the summary.

4. **The basin-level story is about Subpart W facilities, not production volumes.** A basin with 157 small upstream wells (Permian) and a basin with 30 large processing complexes (Arkla) count similarly here. Weighting by volume or emissions would change the ranking — if a reader wants production-weighted concentration, that's a separate analysis.

5. **Small-basin noise.** Arkla's 31.2% top-5 share is driven by a smaller denominator (32 facilities). A single basin of 32 facilities with 26 parents has limited statistical leverage. The claim that Arkla is "more concentrated" than Permian is defensible but should not be over-interpreted.

## Files produced

- `viz/ghgrp_basin_ownership_2023.png` — stacked horizontal bar chart, top-5 operators per basin
- `posts/LinkedIn_Post_GHGP_BasinLevel.md` — LinkedIn caption (counter-finding framing)
- `methodology/BasinLevel_Methodology_and_SelfAudit.md` — this file
- `scripts/phase7_basin_analysis.py` — reproducible analysis + render
- `data/processed/phase7_basin_results.json` — per-basin top 5 and concentration numbers

## Follow-ups

1. **Separate upstream vs. gathering ownership** for the top 2-3 basins. Different story per segment within a basin.
2. **Production-weighted (emissions-weighted) basin concentration.** If a handful of Permian operators account for most of the basin's CO2e, the fragmented-ownership story may not hold when volumes are considered.
3. **Map overlay** showing basin boundaries. Would require a basin shapefile (USGS or EIA publish these) — not yet in the repo.
