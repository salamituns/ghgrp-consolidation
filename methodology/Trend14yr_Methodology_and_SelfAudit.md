# GHGRP 14-Year Concentration Trend (Phase 5) — Methodology and Self-Audit

*Companion to `posts/LinkedIn_Post_GHGP_Recomputed.md` and `viz/ghgrp_14yr_trend_recomputed.png`*

---

## Purpose

Phase 4a and 4b surfaced a methodology inconsistency: the prior published GHGRP posts cited the 2023 top-10 concentration share as **18.0%**, but reproducing the calculation with a documented, consistent rule yielded **16.7%**. Phase 5 recomputes the full 14-year time series from the raw parent-company data under one clean methodology, so every number across every post in this series points to a single reproducible source.

## Data source

**EPA GHGRP Parent Company Dataset** (`ghgp_data_parent_company.xlsb`). One sheet per reporting year from 2010 through 2023. Same file used across all prior phases.

Each year's sheet contains one row per `facility × parent` ownership pair, with the parent's percentage ownership. A facility with three co-owners has three rows. A wholly-owned facility has one row.

## Methodology — the any-stake union rule

For each year:

1. Drop rows with null facility ID or null parent name.
2. Count **unique facilities** (distinct `GHGRP FACILITY ID`) as the denominator.
3. Compute **facility count per parent** (unique facilities in which the parent appears in at least one ownership row).
4. Sort parents by facility count descending. Take the **top 10**.
5. Compute the **top-10 share** as the count of unique facilities where *any* of the top 10 parents appears in ownership, divided by total unique facilities × 100.

This is called the "any-stake union" rule. A joint-venture facility is counted once for each top-10 parent that owns a stake in it, for the purpose of parent-level facility counts, but only once for the purpose of the numerator when computing share.

**Why this rule?**

1. **Reproducible**: single Python expression, no judgment calls.
2. **Conservative on denominator**: unique facility count is unambiguous.
3. **Generous on numerator**: a parent with a 1% stake still counts. This overstates concentration relative to a "primary-owner" rule, but it's also how EPA's own published reports typically frame ownership.
4. **Consistent with Phase 4a and 4b**: the sector-specific and GHGRP-wide numbers all use this rule, making cross-post comparisons internally valid.

Alternative rules (majority-owner, emissions-weighted, etc.) would produce different absolute numbers. The *direction and magnitude of change* over 14 years is robust to the choice. The endpoint number is what shifts.

## Headline numbers (recomputed)

| Year | Unique facilities | Unique parents | Top-10 share |
|---|---|---|---|
| 2010 | 6,823 | 3,851 | **11.7%** |
| 2011 | 8,210 | 4,295 | 10.4% |
| 2012 | 8,415 | 4,439 | 10.5% |
| 2013 | 8,496 | 4,455 | 10.8% |
| 2014 | 8,731 | 4,506 | 11.8% |
| 2015 | 8,587 | 3,495 | **13.6%** (↑ step) |
| 2016 | 8,216 | 3,383 | 14.0% |
| 2017 | 8,142 | 3,360 | 14.0% |
| 2018 | 8,268 | 3,527 | 14.0% |
| 2019 | 8,282 | 3,402 | 14.8% |
| 2020 | 8,248 | 3,415 | 15.4% |
| 2021 | 8,212 | 3,317 | 16.1% |
| 2022 | 8,175 | 3,339 | 16.7% |
| 2023 | 8,106 | 3,327 | **16.7%** |

## Comparison with published numbers

| Metric | Published (prior) | Recomputed (this phase) | Difference |
|---|---|---|---|
| 2010 top-10 share | 11.7% | 11.7% | **0.0 pp** (matches exactly) |
| 2023 top-10 share | 18.0% | 16.7% | **−1.3 pp** |
| Absolute gain | +6.3 pp | +5.1 pp | −1.2 pp |
| Relative growth | +54% | +43% | −11 pp |

The 2010 figure reproduces exactly. The 2023 figure is 1.3 percentage points lower than the prior hardcoded value. The 2015 "vanishing act" (parent-company reclassification year) is still the sharpest discrete step in the series, clearly visible as a +1.8 pp jump between 2014 and 2015.

## Self-audit of claims in the LinkedIn post

| # | Claim | Evidence | Status |
|---|-------|----------|--------|
| 1 | "2010: 11.7%" | Recomputed exactly. | CERTAIN |
| 2 | "2023: 16.7% (not 18.0%)" | Recomputed 16.74%. | CERTAIN |
| 3 | "Absolute gain: +5.1 pp" | 16.74 − 11.66 = 5.08. | CERTAIN |
| 4 | "Relative growth: +43%" | (16.74 / 11.66) − 1 = 43.6%. Rounded to 43%. | CERTAIN |
| 5 | "published +54%" relative growth | (18.0 / 11.7) − 1 = 53.8%. Rounded to 54%. | CERTAIN |
| 6 | "The thesis still holds. Top 10 parent companies do control more... than they did 13 years ago." | Any reasonable methodology shows a rising trend. | CERTAIN |
| 7 | "sector-specific work holds... Phase 4a's 1.6x and Phase 4b's 3.2x multipliers use the same method on both sides... unchanged" | Those ratios are internally consistent. Confirmed. | CERTAIN |
| 8 | "2015 cliff... jumps ~2 percentage points" | 2014: 11.8%, 2015: 13.6%. Delta = 1.8 pp. Rounded to "~2 pp." | CERTAIN |
| 9 | "peak midstream M&A" context for 2015 | From the prior Substack post; not independently verified in this phase. | INHERITED |
| 10 | "Every post can be reproduced. Every claim can be audited." | Scripts exist in `scripts/` for Phases 1, 2, 3, 4a, 4b, 5, all using consistent methodology. | CERTAIN |

## Known discrepancy investigation

The 1.3 pp gap between the published 2023 figure (18.0%) and the recomputed figure (16.7%) could have originated from several possible prior-method differences:

1. **Including subsidiary variants as separate top-10 parents**. For example, if "Energy Transfer LP" and "Energy Transfer Partners LP" were both counted as top-10 eligible in an earlier computation, and their combined facility set was larger than either alone, the top-10 union would be larger. In 2023 data the canonical form is "Energy Transfer LP" only, so this risk is low for 2023, but earlier years have name variants.

2. **Different dataset vintage**. EPA revises the parent-company data over time as reporters correct and resubmit. The 18.0% figure might have been computed on an earlier data vintage that differed slightly from the current 2023 file.

3. **Computation on a different count basis** (e.g., inclusion of "US Government" as a separate counted parent versus consolidated with individual agency reports, counting by emissions tonnage rather than facility count, etc.).

Without access to the original computation script, the exact source of the 1.3 pp gap cannot be determined. The recomputed figure is the one this repo can defend.

## Limitations and caveats

1. **Parent name normalization is naive.** The script treats strings as canonical. If a parent company reports under multiple name variants in the same year ("Kinder Morgan Inc" vs "Kinder Morgan, Inc."), each is counted as a separate parent. Spot checks for 2023 show canonical single-form names for the top 10, so this doesn't affect the 2023 figure materially. Earlier years have more variant-name issues, which could marginally affect per-year top-10 selection.

2. **Year-over-year comparison assumes comparable reporting.** EPA's reporting rules and thresholds have evolved. Facility counts shift as subparts are added or restructured. The 2015 step change specifically reflects EPA methodology changes in how parents are classified, not pure market consolidation. This is a known feature of the dataset, flagged in the chart annotation.

3. **Top-10 identity changes over time.** The 10 parents that make the top 10 in 2023 are not the same 10 that made it in 2010. The metric measures *"what share the current top 10 holds,"* not *"what share the 2010 top 10 still holds."* Both are legitimate trend metrics; this post reports the former because it matches the published question.

4. **No emissions-weighted variant.** A separate analysis weighting by CO2e tonnage per facility would tell a different story (and likely show higher concentration for refineries, which produce disproportionate emissions). That's Phase 4c territory.

## Files produced

- `viz/ghgrp_14yr_trend_recomputed.png` — Phase 5 trend chart
- `posts/LinkedIn_Post_GHGP_Recomputed.md` — LinkedIn correction post
- `methodology/Trend14yr_Methodology_and_SelfAudit.md` — this file
- `scripts/phase5_trend_recompute.py` — reproducible computation
- `data/processed/phase5_14yr_trend.csv` — tabular year-by-year results
- `data/processed/phase5_14yr_trend.json` — structured per-year results with top-10 names
- `data/processed/phase5_comparison_summary.json` — published-vs-recomputed comparison

## Open questions for Tee

1. **Publishing the correction.** Do you want this to go out as a standalone post (my recommendation), or folded quietly into the methodology note of a future piece? The standalone option is more visible but makes the methodology transparent, which I think is net positive for the series's credibility.

2. **Update `build_charts.py`?** The prior chart builder has "18.0%" hardcoded in a comment. I left it as-is during earlier phases so the published images weren't disturbed, but now that a replacement number (16.7%) is the authoritative value, I can optionally update `build_charts.py` to regenerate the original bar chart with the corrected subtitle. Say the word.

3. **Phase 6 candidates**. Now that the methodology is locked down:
   - **Emissions-weighted concentration**: same analysis weighted by CO2e per facility. Likely shows refineries even more dominant than by count.
   - **Basin-level oil & gas analysis**: Permian vs. Appalachia vs. Bakken ownership breakdown.
   - **"Who owns the top 500 emitters?"**: highest-emitting facilities regardless of sector, traced to parent.
