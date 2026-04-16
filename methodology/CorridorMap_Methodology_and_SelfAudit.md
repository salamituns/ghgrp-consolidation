# GHGRP Corridor Map (Phase 2) — Methodology and Self-Audit

*Companion to `LinkedIn_Post_GHGP_Corridor.md` and `viz/ghgrp_corridor_map_2023.png`*

---

## Data sources

1. **EPA GHGRP 2023 Data Summary Spreadsheets** — same file used in Phase 1, with lat/long for 7,538 CONUS facilities.
2. **EPA GHGRP Parent Company Dataset** — same 2023 sheet used in Phase 1, identifies KM (231), ET (184), and KM+ET JV (17) facilities.
3. **US Census Bureau County Population Estimates, 2023** (`co-est2023-alldata.csv`). Published by the Population Estimates Program. Covers annual county population estimates 2020–2023. 3,195 county-level records.
4. **US Census Cartographic Boundary Files** — `gz_2010_us_050_00_500k.json` (3,221 counties) and `gz_2010_us_040_00_5m.json` (52 states). Resolution 500k used for county polygons in this view.

## Processing steps

1. Loaded county GeoJSON, joined to population file on 5-digit FIPS (`STATE` + `COUNTY`). Match rate: **3,131 of 3,221 counties (97.2%)**.
2. **Connecticut's 8 counties and 2 reclassified Alaska counties** did not match. Reason: Connecticut replaced its county system with "Planning Regions" starting with the 2020 ACS; Census population estimates now report Connecticut at the planning-region level. Not in this view.
3. Computed county population density as `POPESTIMATE2023 / CENSUSAREA` (sq. mi).
4. Defined the **Gulf Coast corridor extent** as lon [-97, -81], lat [28.5, 35.5]. Extent chosen to include all 17 KM+ET joint-venture facilities plus the full Cancer Alley corridor in Louisiana.
5. Population within extent computed from counties whose **centroid** falls inside the bounding box (avoids double-counting or partial attribution from counties that straddle the edge). Result: **618 counties, 54,385,443 residents**.
6. Facility filter: lat/long inside extent → **1,840 GHGRP facilities**, broken down as 1,665 other + 80 KM + 78 ET + 17 JV.

## Self-audit of claims in the LinkedIn post

| # | Claim | Evidence | Status |
|---|-------|----------|--------|
| 1 | "1,840 large industrial facilities reporting to the EPA in 2023" in the corridor | Count of 2023 GHGRP facilities with coords inside extent = 1,840 | CERTAIN |
| 2 | "24% of all geocoded GHGRP facilities in the country" | 1,840 / 7,538 = 24.4% | CERTAIN (rounded to "24%") |
| 3 | "54.4 million Americans" in the corridor | Sum of POPESTIMATE2023 for counties with centroid inside extent = 54,385,443 | CERTAIN |
| 4 | "16% of the US population" | 54,385,443 / 334,914,895 (sum of all US counties in Census file) = 16.24% | CERTAIN |
| 5 | "1.5x more large emitters than its share of people would predict" | 24.4% / 16.2% = 1.51. Rounded to "roughly 1.5x." | CERTAIN |
| 6 | "Harris County alone: 4.8 million residents" | Census POPESTIMATE2023 for Harris County TX = 4,835,125 | CERTAIN |
| 7 | "one of the densest clusters of GHGRP reporters in the country" | Visual from the map + Phase 1 map. Not quantified against other counties in this post. | CERTAIN (visual), UNCERTAIN (not ranked) |
| 8 | "The darkest counties on the map cluster around Atlanta" | Top 10 densest in corridor: Dallas County TX, DeKalb GA, Harris County TX, Cobb GA, Gwinnett GA, Orleans Parish, Clayton GA, Fulton GA, Orange County FL, Seminole County FL. 5 of top 10 are Atlanta metro. | CERTAIN |
| 9 | "Louisiana and Mississippi have moderate density and a thick facility presence" | Visual observation consistent with map | CERTAIN (visual), UNCERTAIN (not quantified) |
| 10 | "Cancer Alley sits in that band" | Reference to the 85-mile Baton Rouge-to-New Orleans industrial corridor between approximately 30.0°N-30.5°N, 90.5°W-91.3°W. Falls inside the extent. Name is widely used in academic and environmental justice literature; not a contested label. | CERTAIN |
| 11 | "17 facilities co-owned by Kinder Morgan and Energy Transfer" | Phase 1 JV set calculation, verified | CERTAIN |
| 12 | "run from urban termini (Orlando, Zachary near Baton Rouge) through mostly rural compressor stations" | Density check: 11 of 17 JV facilities sit in counties with <100 people/sq mi (rural). Only Orlando (1,629/sqmi) and Zachary-area (985/sqmi) exceed 500/sqmi. | CERTAIN |
| 13 | "top 10 parents went from 11.7% to 18.0% of facilities in 13 years" | Directly from prior published analysis | INHERITED FROM PRIOR POST |
| 14 | "EPA's September 2025 proposal removes 46 source categories" | Directly from prior published analysis | INHERITED FROM PRIOR POST |

## Limitations and caveats

1. **Centroid-based county assignment to the corridor.** Counties on the extent boundary are included only if their geometric centroid is inside. Minor edge effect: a few counties extend slightly past the visual frame, and a few counties whose centroid is just outside may have a sliver inside the frame and still get excluded from the population count. Net error well under 1%.

2. **Population counts are 2023 Census Bureau estimates, not decennial.** These are annual estimates produced by the Population Estimates Program, which are the most current county-level counts available. For demographic subsets (race, age, income), ACS 5-year estimates would be the correct source. This post uses only total population.

3. **Industrial density ≠ emissions volume.** This map treats every GHGRP reporter as one dot. Phase 3 will introduce per-facility emission totals (tons CO2e) so the color weight of each dot reflects its actual emission footprint, not just its presence.

4. **"Corridor" is a defined extent, not an official region.** The 11-state span captured here overlaps with multiple official Census divisions. The extent was chosen to include the full KM+ET JV pipeline footprint, Cancer Alley, the Texas Gulf refining cluster, and the FL panhandle, because those are the features the prior Substack analysis discussed. Someone defining "Gulf Coast" differently (e.g., strict coastline counties only) would get different numbers.

5. **Facility-coordinate coverage is 93% (Phase 1 caveat).** 568 of 8,106 2023 GHGRP facilities have no coordinates in the EPA summary spreadsheets. Corridor facility count of 1,840 reflects the 7,538 geocoded subset, not the full population.

## Files produced

- `viz/ghgrp_corridor_map_2023.png` — Phase 2 corridor map (200 dpi)
- `LinkedIn_Post_GHGP_Corridor.md` — LinkedIn caption
- `CorridorMap_Methodology_and_SelfAudit.md` — this file
- `render_corridor_map.py` — reproducible render script
- `ghgrp_2023_geo.csv` — joined facility-level dataset (shared with Phase 1)

## Open questions for Tee

1. **Caption framing.** Draft leans on the "infrastructure + population" tension (mild EJ voice), stops short of naming specific demographic disparities (race, income). Want to keep that restraint, or lean harder into the published EJ literature (which already exists for the Cancer Alley area specifically)?

2. **Headline choice on the image.** Currently reads *"The corridor sits where the people are."* Alternatives considered: *"The concentration has neighbors"* (echoes the "concentration has a shape" line from Phase 1), *"Infrastructure plus people"* (drier, more neutral). Easy swap if you have a preference.

3. **Phase 3 trigger.** This post sets up the exposure-buffer story (3km / 10km population within buffer rings of KM+ET facilities). Want to ship Phase 2 first and gauge response, or run Phase 3 in parallel so we have the full arc ready?
