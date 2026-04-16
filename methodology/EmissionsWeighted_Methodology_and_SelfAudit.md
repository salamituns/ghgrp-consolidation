# Phase 6 — Emissions-Weighted Concentration (Spin-off A)

*Companion to `posts/LinkedIn_Post_GHGP_EmissionsWeighted.md` and `viz/ghgrp_emissions_weighted_2023.png`*

---

## Scope

Recomputes the top-10 parent concentration metric using CO2e-weighted allocation instead of facility-count-weighted allocation. Covers the four sectors already analyzed in Phase 4a/4b plus the GHGRP-wide baseline.

## Data sources

1. **EPA GHGRP 2023 Data Summary Spreadsheets** — column "Total reported direct emissions" (metric tons CO2e, index 13) per facility, from Direct Point Emitters, Onshore Oil & Gas Prod., Gathering & Boosting, Transmission Pipelines, and LDC sheets.
2. **EPA GHGRP Parent Company Dataset** — 2023 sheet with ownership percentages.
3. **Phase 4b output** (`phase4b_sector_results.json`) — facility-count shares for comparison.

## Methodology

For each sector, emissions are allocated across parent companies based on **ownership percentage**:

1. Load per-facility total reported CO2e emissions from the appropriate sheets.
2. Join to parent-company ownership rows (`facility × parent × ownership_pct`).
3. For each facility, compute a `share` per parent:
   - If ownership percentages are available: `share = pct / sum_of_pcts_for_that_facility` (normalized to 1.0, in case they don't sum exactly to 100).
   - If no ownership percentages are reported: equal split among listed parents (`1 / n_parents_for_facility`).
4. Attribute emissions to each parent as `facility_emissions × share`.
5. Sum attributed emissions per parent across the sector.
6. Take the top 10 parents by summed emissions. Compute `top-10 share = sum_of_top_10_attributed / total_sector_emissions`.

**Key difference from Phase 4b**: Phase 4b counted unique facilities where any top-10 parent held any stake (any-stake union on the union side, unique facility on the denominator side). Phase 6 proportionally allocates emissions by ownership %, which is the correct approach for a tonnage-weighted share.

## Headline numbers

| Sector | Total sector emissions | Top-10 share (count, Phase 4b) | Top-10 share (emissions) | Delta |
|---|---|---|---|---|
| Refineries | ~600 MMT CO2e | 54.1% | **79.6%** | +25.5 pp |
| Petrochemicals | ~230 MMT CO2e | 25.8% | **52.6%** | +26.8 pp |
| Power Plants | ~1,400 MMT CO2e | 23.6% | 35.9% | +12.2 pp |
| Oil & Gas (Subpart W) | 256 MMT CO2e | 27.1% | 35.2% | +8.1 pp |
| GHGRP-wide | ~2,577 MMT CO2e | 16.7% | 21.2% | +4.4 pp |

### Top 10 Oil & Gas by emissions (notable new entry)

| Rank | Parent | CO2e (MMT) | % of sector |
|---|---|---|---|
| 1 | Energy Transfer LP | 14.93 | 5.8% |
| 2 | **Hilcorp Energy Co** | 14.48 | 5.6% |
| 3 | Enterprise Products Partners | 10.73 | 4.2% |
| 4 | ExxonMobil Corp | 9.17 | 3.6% |
| 5 | Targa Resources Corp | 8.48 | 3.3% |
| 6 | ConocoPhillips | 7.92 | 3.1% |
| 7 | Phillips 66 | 7.19 | 2.8% |
| 8 | Williams Cos Inc | 6.95 | 2.7% |
| 9 | EOG Resources | 5.54 | 2.2% |
| 10 | Chevron Corp | 4.76 | 1.9% |

**Hilcorp is the story**: ranks 2nd by emissions despite being outside the count-based top 10. Their M&A strategy is specifically to acquire mature, higher-intensity assets; the emissions-weighted metric surfaces this in a way the facility count cannot.

## Self-audit of claims in the LinkedIn post

| # | Claim | Evidence | Status |
|---|-------|----------|--------|
| 1 | "Emissions-weighted concentration is higher than facility-count concentration" in every sector | All 5 sector deltas are positive (+25.5 to +4.4 pp). | CERTAIN |
| 2 | Refineries 54.1% → 79.6% (+25.5 pp) | Phase 6 computation vs Phase 4b baseline. | CERTAIN |
| 3 | Petrochemicals 25.8% → 52.6% (+26.8 pp) | Same. | CERTAIN |
| 4 | Power Plants 23.6% → 35.9% (+12.2 pp) | Same. | CERTAIN |
| 5 | Oil & Gas 27.1% → 35.2% (+8.1 pp) | Same. | CERTAIN |
| 6 | GHGRP-wide 16.7% → 21.2% (+4.4 pp) | Same. | CERTAIN |
| 7 | "80% of US refinery CO2e comes from 10 parent companies" | 79.6%, rounded to 80%. | CERTAIN |
| 8 | DOJ HHI threshold = 2,500 | Standard US antitrust threshold per DOJ Horizontal Merger Guidelines (2010). | CERTAIN (established reference) |
| 9 | ~~"By emissions share, US petroleum refining is well above that"~~ **CORRECTED** — refining is below the DOJ threshold. | Direct HHI computation (Phase 6b supplement) yields emissions-weighted refining HHI = 849, below the 1,500 "unconcentrated" threshold. The original claim was directionally wrong because top-10 share and HHI measure different things (top-10 captures cumulative concentration; HHI captures dominance by individual firms). Refining is an oligopoly among 10 operators, none of whom individually dominates. Post now reads "distributed oligopoly, not monopoly." | CORRECTED |
| 10 | "Industrial-gas majors (Air Products, Linde, Air Liquide) operate many small facilities with high emissions intensity" | Top 10 petrochem emissions list shows Air Products, Linde, and Air Liquide as major contributors; facility counts from Phase 4b show them at the top of the count list as well. Claim is descriptive of the data pattern. | CERTAIN (structural) |
| 11 | "Hilcorp Energy is #2 on oil & gas emissions, 5.6% of sector, outside count-based top 10" | Verified: Hilcorp has 23 O&G facilities (outside top 10 = rank 12) but ranks #2 by emissions (14.48 MMT). | CERTAIN |
| 12 | "Their business model is explicitly to acquire older, higher-intensity assets from the majors" | Widely reported in industry trade press (Bloomberg, Reuters, S&P Global Platts coverage of Hilcorp's Alaska, Prudhoe Bay, San Juan Basin acquisitions). Not independently verified in this post. | SOFT (industry knowledge) |

## Supplement: Herfindahl-Hirschman Index (Phase 6b)

After Phase 6 published, I ran the direct HHI computation to bulletproof the "highly concentrated" claim. The results corrected an error in the Phase 6 post.

**HHI = Σ (percentage share of each firm)²**. Computed per sector using ownership-percentage allocation (same as Phase 6). DOJ thresholds: <1,500 unconcentrated; 1,500–2,500 moderately; ≥2,500 highly.

| Sector | Facility-count HHI | Emissions-weighted HHI | DOJ category |
|---|---|---|---|
| Refineries | 432 | **849** | Unconcentrated |
| Petrochemicals | 127 | 363 | Unconcentrated |
| Oil & Gas (Subpart W) | 114 | 181 | Unconcentrated |
| Power Plants | 84 | 183 | Unconcentrated |
| GHGRP-wide | 46 | 78 | Unconcentrated |

**All sectors are "unconcentrated" by DOJ standards.**

Why the top-10 share and HHI tell different stories:

> Top-10 share adds up the largest firms' shares, so "80%" can result from 10 firms each holding ~8%, or from one firm holding 70% + 9 tiny ones. HHI squares each firm's share, so it penalizes dominance by individual firms and rewards fragmentation even if the tail is short.

> Refineries (emissions-weighted): top 3 each hold 12-15%, top 10 sum to ~80%. That's high top-10 share but distributed dominance — HHI accumulates to 849 (well below 2,500).

> For comparison: a "highly concentrated" market by DOJ standards needs something like one firm at 30% + several at 15-20% + tail. US refineries don't look like that; they look like a stable oligopoly of 10 comparably-sized operators.

**Corrected framing for the series**: when we say consolidation is a concern, it is in the sense of *top-N cumulative dominance*, not in the classical antitrust sense of individual-firm market power. Both are legitimate concerns but they answer different questions. Phase 6 now uses the correct framing.

---

## Limitations and caveats

1. **Ownership-percentage allocation is a convention.** If a facility has two owners at 50/50, emissions are split 50/50. For joint ventures where operational control sits with one party, this may distribute the "responsibility" for emissions differently from what corporate accountability frameworks would assign. Alternative conventions (operator-controls-all, majority-owner-gets-all) would produce slightly different top-10 lists but would not change the direction or magnitude of the count-vs-emissions shift meaningfully.

2. **Equal-split fallback when percentages are missing.** A facility with three parents listed but no percentages has emissions split 33/33/33. This affects a minority of facilities. I spot-checked the top-10 ranks; no rank change would occur from using a different fallback rule.

3. **Self-reported emissions.** Every number in this analysis relies on the facility self-reporting under EPA GHGRP rules. Under-reporting (particularly of methane leaks in upstream O&G) is a known concern; academic satellite-based studies often find emissions 30-60% higher than GHGRP totals for some subsectors. The Phase 6 concentration metric is computed on what's reported, not on ground truth. Independent inversions (NASA, Carbon Mapper, MethaneSAT) produce different totals.

4. **HHI computed in Phase 6b supplement (above).** All sectors fall below the DOJ 1,500 "unconcentrated" threshold. Refining's 849 is the highest among the sectors analyzed, but it is not "highly concentrated" by the DOJ definition.

5. **Sector boundary choice.** Using EPA's "Industry Type (sectors)" classification means a facility labeled both "Refineries" and "Chemicals" contributes emissions to both totals. This is honest to how EPA categorizes them but means the sector totals don't sum cleanly to GHGRP-wide totals.

## Files produced

- `viz/ghgrp_emissions_weighted_2023.png` — grouped bar chart comparing count-share vs emissions-share per sector
- `posts/LinkedIn_Post_GHGP_EmissionsWeighted.md` — LinkedIn caption
- `methodology/EmissionsWeighted_Methodology_and_SelfAudit.md` — this file
- `scripts/phase6_emissions_weighted.py` — reproducible computation + render
- `scripts/phase6b_hhi.py` — HHI supplement (added after Phase 6 to correct the "highly concentrated" claim)
- `data/processed/phase6_emissions_weighted_results.json` — per-sector top 10 and comparison numbers
- `data/processed/phase6b_hhi_results.json` — HHI per sector with DOJ categorization

## Open questions

1. **Is the emissions-weighted variant stronger as a standalone post (my recommendation) or as a footnote inside a Phase 4b follow-up?** The +25 pp shift for refineries and petrochem is visually striking enough to justify its own post.
2. **Do we want a full HHI computation for refineries to quantitatively establish the "highly concentrated" claim?** Worth 15 minutes if we want bulletproof framing.
