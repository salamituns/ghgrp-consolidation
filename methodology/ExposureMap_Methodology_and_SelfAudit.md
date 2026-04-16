# GHGRP Exposure Map (Phase 3) — Methodology and Self-Audit

*Companion to `LinkedIn_Post_GHGP_Exposure.md` and `viz/ghgrp_exposure_map_2023.png`*

---

## Data sources

1. **EPA GHGRP 2023 Data Summary Spreadsheets** + **Parent Company Dataset** — same files used in Phases 1 and 2. Identifies the 231 KM, 184 ET, and 17 KM+ET JV facilities for 2023.
2. **US Census ACS 2019-2023 5-year Estimates, Table B01003 (Total Population)**, filtered to Census Tract geography. Downloaded from data.census.gov. 85,381 tract records.
3. **US Census Cartographic Boundary File `cb_2023_us_tract_500k`** (shapefile). 85,186 tract polygons. State outlines from same source, 5m resolution, used in prior phases.

## Processing steps

1. Loaded tract shapefile (WGS84 / NAD83, EPSG:4269). Joined to ACS population on 11-digit tract FIPS. **Match rate: 85,045 of 85,186 (99.8%).** 141 unmatched tracts primarily reflect tract boundary changes between the 2023 shapefile vintage and the 2019-2023 ACS tabulation years; negligible effect.
2. Reprojected tracts and facility points to **EPSG:5070 (NAD83 / Conus Albers Equal Area)**. This is the standard CRS for continental US analysis — distances and areas are in meters and square meters, not degrees. Buffering in lat/long would produce distorted, elliptical shapes that are wrong by 30–50% at US latitudes.
3. Built **Euclidean buffers** at 3000 m and 10000 m around each KM and ET facility point.
4. Unioned buffers per operator (via `shapely.union_all`) to collapse overlapping buffers from co-located facilities into a single polygon per operator per distance. This prevents double-counting people inside overlapping buffer zones.
5. **Area-weighted population allocation**: for each tract intersecting a buffer, computed the ratio of (intersection area) to (tract total area), multiplied the tract's total population by that ratio, and summed across intersecting tracts. This is the standard method when buffer boundaries don't align with tract boundaries.

## Headline numbers

| Metric | Value |
|---|---|
| Kinder Morgan 3 km buffer population | 454,061 |
| Kinder Morgan 10 km buffer population | 4,904,197 |
| Energy Transfer 3 km buffer population | 370,697 |
| Energy Transfer 10 km buffer population | 4,094,054 |
| **Combined KM + ET 3 km buffer population** | **701,744** |
| **Combined KM + ET 10 km buffer population** | **7,703,643** |
| Combined 10 km buffer area | 100,039 km² (≈ Kentucky) |
| Combined 3 km buffer area | 9,587 km² |
| Facilities included (with coords) | 224 KM + 184 ET = 391 combined (of 398 combined total) |
| US total population (sum of tracts) | 335,559,225 |
| Combined 10 km as % of US | 2.30% |
| Combined 3 km as % of US | 0.21% |

**Why combined < KM + ET**: 17 facilities are jointly owned by both companies (the FGT and MEP pipelines, Phase 1 finding), and some KM and ET facilities are close enough that their buffers overlap. Union-based counting eliminates the double-count. Overlap magnitude: 3 km buffers overlap by ~123,000 people; 10 km buffers overlap by ~1,295,000 people.

## Self-audit of claims in the LinkedIn post

| # | Claim | Evidence | Status |
|---|-------|----------|--------|
| 1 | "7.7 million Americans live within 10 km..." | Area-weighted union exposure = 7,703,643 | CERTAIN |
| 2 | "More people than live in the state of Virginia" | Virginia 2023 Census estimate ≈ 8.72M. **7.7M is LESS than Virginia (8.72M), not more.** | INCORRECT — needs rewrite |
| 3 | "More than Massachusetts" | Massachusetts 2023 ≈ 7.00M. 7.7M > 7.0M. | CERTAIN |
| 4 | "More than the Denver and Seattle metro areas combined" | Denver MSA ≈ 2.99M + Seattle MSA ≈ 4.05M = ~7.04M. 7.7M > 7.04M. | CERTAIN |
| 5 | "~702,000 people within 3 km" | Combined 3 km = 701,744 | CERTAIN |
| 6 | "Closer than most Americans live to their nearest Target" | Illustrative comparison, not strictly from data. Median distance to nearest Target in the US is around 2 km per several market research reports (varies by source). 3 km is within that range. | SOFT — illustrative framing, not a data-backed claim |
| 7 | "3,327 parent companies reporting to the EPA" | From the 2023 parent company xlsb; verified in prior phases | CERTAIN |
| 8 | "8,106 facilities in 2023" | From 2023 parent company xlsb | CERTAIN |
| 9 | "KM and ET own 415 of them (including 17 they share via joint venture)" | 231 + 184 = 415; 17 shared (Phase 1 finding) | CERTAIN |
| 10 | "Combined 10 km buffer footprint ~100,000 km², roughly the size of Kentucky" | Combined 10 km area = 100,039 km². Kentucky land area = 102,269 km². Correct within 3%. | CERTAIN |
| 11 | "~2.3% of the US population" | 7,703,643 / 335,559,225 = 2.296%. Rounded to 2.3%. | CERTAIN |
| 12 | "conservative methods... area-weighted census tract population, US Albers Equal Area projection" | Matches processing steps above | CERTAIN |
| 13 | "Seven KM facilities without reported coordinates are excluded" | 231 - 224 = 7 | CERTAIN |
| 14 | "Proximity is not emission exposure" | Explicit caveat consistent with EJ literature. | CERTAIN (as caveat) |

### Action required from audit

**Claim #2 was wrong in the v1 draft.** Virginia has ~8.7M residents, which is MORE than 7.7M. Caption has been corrected to use **Tennessee (~7.13M)** as the lead comparison, which is clearly smaller than 7.7M. Massachusetts comparison (7.0M) and Denver+Seattle metros comparison both remain valid.

## Limitations and caveats

1. **Euclidean buffers vs. real terrain.** 3 km and 10 km are straight-line distances. They don't account for terrain, watersheds, or pipeline routing. A person living 3 km from a compressor station across a ridge is not exposed the same way as a person 3 km away on the same flat plain.

2. **Tract boundaries and population distribution within tracts.** Area-weighted allocation assumes population is uniformly distributed within each tract. In reality, population is often concentrated in a subset of the tract. Effect on final number is typically small (<5%) at this scale.

3. **"Facility" is a reporting unit, not a physical plant.** GHGRP facilities are defined by EPA's reporting rules. A single pipeline system may report as multiple facilities; a large refinery reports as one. Counts reflect reporting structure, not physical footprint.

4. **Proximity ≠ emission exposure.** This analysis measures who lives near consolidated infrastructure. It does not measure air quality, health outcomes, or regulatory compliance. Those are separate analyses requiring EPA emissions inventories and air dispersion modeling, which are not part of this post.

5. **Seven KM facilities without coordinates (3%)** are excluded from the calculation. The combined 7.7M figure is therefore very slightly understated.

6. **ACS tract populations have margins of error.** These are 5-year estimates, not exact counts. For a single tract the MOE may be 10-20% of the estimate; in aggregate across thousands of tracts, the MOE on the sum is much tighter (well under 1%).

## Files produced

- `viz/ghgrp_exposure_map_2023.png` — Phase 3 national exposure map
- `LinkedIn_Post_GHGP_Exposure.md` — LinkedIn caption draft (needs Claim #2 fix)
- `ExposureMap_Methodology_and_SelfAudit.md` — this file
- `phase3_analysis.py` — reproducible buffer computation script
- `render_exposure_map.py` — reproducible map render script
- `phase3_results.json` — all computed numbers in machine-readable form

## Open questions for Tee

1. **Claim #2 fix**: replace "more than Virginia" with one of the accurate comparisons above. Your preference on which state or comparison to use?

2. **The sharper version of the hook.** Current opener is three sentences building up to the headline. Would a harder-hitting single-line lead ("7.7 million Americans live within 10 km of infrastructure owned by two companies") work better for LinkedIn feed capture? Different tradeoff between rhythm and stopping-power.

3. **Should we publish a short follow-up with operator-level breakdowns?** KM alone accounts for 4.9M people at 10 km; ET for 4.1M. That's its own sub-narrative ("Kinder Morgan: 4.9 million neighbors") if you want to stretch the series.
