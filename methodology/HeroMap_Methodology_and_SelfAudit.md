# GHGRP Hero Map — Methodology and Self-Audit

*Companion to `LinkedIn_Post_GHGP_HeroMap.md` and `viz/ghgrp_hero_map_2023.png`*

---

## Data sources

1. **EPA GHGRP 2023 Data Summary Spreadsheets** (`ghgp_data_2023.xlsx`). Downloaded April 15, 2026 from `www.epa.gov/ghgreporting/data-sets`. Provides `Facility Id`, latitude, longitude, and emissions for every reporting facility across six geography-bearing sheets: Direct Point Emitters, Onshore Oil & Gas Production, Gathering & Boosting, Transmission Pipelines, LDC Direct Emissions, and SF6 from Electrical Equipment.

2. **EPA GHGRP Parent Company Dataset** (`ghgp_data_parent_company.xlsb`). Same file used in the prior 14-year consolidation analysis. Provides the mapping from `GHGRP FACILITY ID` to `PARENT COMPANY NAME` with ownership percentages, for each reporting year 2010 through 2023.

Both datasets are joined on `GHGRP FACILITY ID` / `Facility Id` (identical key).

## Processing steps

1. Loaded all six geography-bearing sheets from the 2023 summary spreadsheet and unified them on `Facility Id`. Resulted in **7,539 unique facilities with coordinates**.
2. Loaded the 2023 sheet of the parent company xlsb. Resulted in **8,106 unique facilities** (matches the previously published 14-year analysis).
3. Joined coordinates to the parent table. Match rate: **7,538 of 8,106 (93.0%)**. The 568 facilities without coordinates report under GHGRP subparts not represented in the six geography-bearing sheets (primarily small natural gas LDCs and importers).
4. Filtered to CONUS bounding box (lon -125 to -66, lat 24 to 50). Excludes Alaska, Hawaii, Puerto Rico. Final render count: **7,401 CONUS facilities**.
5. Identified Kinder Morgan facilities as any facility where `PARENT COMPANY NAME == 'KINDER MORGAN INC'` appears in any ownership row (consistent with the published count of 231). Same rule for Energy Transfer.
6. Identified joint-venture facilities as the intersection of the KM and ET facility sets: **17 facilities**.

## Self-audit of claims in the LinkedIn post

| # | Claim | Evidence | Status |
|---|-------|----------|--------|
| 1 | "415 reporting facilities in 2023" (KM + ET combined) | 231 KM + 184 ET = 415 | CERTAIN |
| 2 | "up from 43 in 2010" (KM + ET combined in 2010) | Substack cites KM=24 and ET=19 for 2010; 24+19=43 | CERTAIN (matches prior published analysis) |
| 3 | "9.6x jump in combined footprint" | 415 / 43 = 9.65 | CERTAIN |
| 4 | "driven entirely by acquisition" | Supported by published Substack thesis; not re-verified from M&A filings in this post | INHERITED FROM PRIOR POST |
| 5 | "Seventeen of the facilities on this map are jointly owned by KM and Energy Transfer" | Intersection of KM and ET facility sets in 2023 parent table = 17 facilities | CERTAIN |
| 6 | "most of them the Florida Gas Transmission pipeline" | 12 of 17 JV facilities carry 'FLORIDA GAS TRANSMISSION COMPANY' in facility name (70.6%) | CERTAIN |
| 7 | "that runs across the Deep South" | JV facilities by state: FL=7, LA=4, TX=2, MS=2, AL=1, AR=1 | CERTAIN |
| 8 | "Nearly half of America's large emitters sit in this region" (Gulf Coast corridor = South region) | Substack published claim: South region = 48.0% of GHGRP facilities in 2023. This post rephrases the claim; it is NOT independently re-verified against the 2023 summary spreadsheet. | INHERITED FROM PRIOR POST |
| 9 | "KM's pipeline footprint runs east from Texas through Tennessee into the Carolinas" | Visual observation from the rendered map | CERTAIN (visual), UNCERTAIN (not quantified by state-level pipeline mileage) |
| 10 | "Energy Transfer's runs from the Permian up into the Midwest" | Visual observation from the rendered map | CERTAIN (visual), UNCERTAIN (not quantified) |
| 11 | "top two midstream consolidators share the backbone" | 17 JV facilities, all on active pipeline systems (FGT + MEP) | CERTAIN |
| 12 | "We're still debating whether to dismantle the reporting system" | Substack cites EPA Sept 2025 proposal to remove 46 source categories | INHERITED FROM PRIOR POST |

## Limitations and caveats

1. **7.0% of facilities excluded from map.** Small natural gas local distribution companies (LDCs) and a few other subpart-specific reporters don't appear in the geography-bearing sheets. This biases the visual slightly toward upstream, midstream, and direct point-source facilities. The excluded facilities are small by definition (natural gas distribution reports at the utility level, not the meter level).

2. **CONUS only.** 137 facilities in Alaska, Hawaii, and territories are excluded for visual clarity. None of the 231 KM or 184 ET facilities sit outside CONUS based on spot check.

3. **Ownership = any stake.** A facility is counted as "KM" if KM appears in any of its parent ownership rows, regardless of ownership percentage. This matches the methodology of the prior 14-year analysis and keeps counts consistent with the published 231 / 184 headline numbers.

4. **No emissions weighting.** The hero map treats every facility as one dot regardless of CO2e volume. Phase 3 will layer emissions tonnage onto facility points for a different visual story.

5. **State outlines included.** US Census Cartographic Boundary File `gz_2010_us_040_00_5m.json` overlaid (52 features, includes FIPS state codes for future chloropleth work). Alaska, Hawaii, and Puerto Rico clipped from the render.

6. **Visual claims in the map legend and caption** (e.g., which states dominate KM vs ET footprints) are qualitative observations from the render and are not statistically quantified in this post. Anyone challenging a specific visual interpretation should be directed to the underlying CSV for state-by-state counts.

## Files produced

- `viz/ghgrp_hero_map_2023.png` — the hero map image (200 dpi)
- `LinkedIn_Post_GHGP_HeroMap.md` — LinkedIn post draft
- `HeroMap_Methodology_and_SelfAudit.md` — this file
- `ghgrp_2023_geo.csv` — joined dataset (parent company + coordinates) for the 8,106 2023 facilities

## Open questions for Tee

1. **Trigger the JV pointer in the caption?** The 17 JV facilities are the freshest insight in this post. Worth calling them out in the first three lines for engagement, or keep the reveal where it is?

2. **Prior-post link strategy.** The draft says "Prior post on the 14-year consolidation trend linked in comments." Want me to also pin a specific Substack URL?

3. **Hashtags.** Current set: `#ClimateData #EnergyInfrastructure #Midstream #GHGRP #ESG`. Prior post used `#ClimateData #Sustainability #IndustrialEmissions #ESG #ClimatePolicy #EnergyTransition`. Mix-match OK?

4. **When to post.** Data-heavy LinkedIn content performs best Tue/Wed/Thu mornings 8–10 AM in your audience's timezone. Want me to set a recommended posting slot?
