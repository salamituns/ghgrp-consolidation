# Top-N Concentration vs. HHI in U.S. Industrial Emissions Infrastructure: A Reproducible 14-Year Analysis of the EPA Greenhouse Gas Reporting Program

**Olatunde Salami**
Stratdevs (Tareony)

**April 2026**

**SSRN Working Paper — DRAFT**

---

## Abstract

This paper analyzes 14 years (2010-2023) of facility-level ownership data from the U.S. Environmental Protection Agency's Greenhouse Gas Reporting Program (GHGRP) to characterize the market structure of America's industrial emissions infrastructure. Using an any-stake union methodology applied to the EPA's parent-company dataset, we find that the top 10 parent companies increased their share of reporting facilities from 11.7% to 16.7% over the study period, a 43% relative gain driven primarily by acquisition-led consolidation in midstream natural gas. We decompose this finding across four major sectors (petroleum refining, oil and gas production, petrochemicals, and electric power), finding that petroleum refining exhibits the highest top-10 concentration at 54% by facility count and 80% by emissions weight. However, when we apply the Herfindahl-Hirschman Index (HHI) used in U.S. antitrust review, every sector falls below the Department of Justice threshold for "moderately concentrated" markets. The divergence between these two metrics is the paper's central contribution: top-N cumulative concentration and HHI dispersion-weighted concentration measure structurally different phenomena, and conflating them produces misleading policy conclusions. We additionally show that upstream oil and gas production is fragmented at the basin level (the Permian Basin has 130 parent companies with a top-1 share of 3.2%), while midstream pipeline infrastructure serving the same basins is highly consolidated, suggesting that sector-level aggregation obscures fundamentally different competitive dynamics. All analysis is conducted on publicly available data with reproducible scripts. The findings are presented against the backdrop of EPA's September 2025 proposal to remove 46 source categories from the GHGRP, which would terminate the longitudinal dataset that makes this analysis possible.

**Keywords:** greenhouse gas reporting, market concentration, Herfindahl-Hirschman Index, industrial emissions, pipeline consolidation, environmental monitoring, GHGRP, EPA, antitrust metrics

**JEL Classification:** L11 (Production, Pricing, Market Structure), Q53 (Air Pollution), Q58 (Environmental Economics: Government Policy), L95 (Gas Utilities, Pipelines)

---

## 1. Introduction

The EPA's Greenhouse Gas Reporting Program, established in 2009 and collecting facility-level data since Reporting Year 2010, is one of the most granular public datasets on industrial emissions in the world. As of reporting year 2023, the program covers 8,106 facilities operated by 3,327 parent companies across all 50 states and U.S. territories (EPA, 2024a). Every facility emitting more than 25,000 metric tons of CO2 equivalent per year must report, making the GHGRP a near-census of large industrial emissions sources.

Despite this richness, most analyses of GHGRP data focus on aggregate emissions trends, sector-level comparisons, or individual facility performance. Relatively little attention has been paid to the *ownership structure* of reporting facilities, and how that structure has evolved over time. This is a significant gap. Who owns emissions infrastructure determines who has leverage over decarbonization decisions, who shapes regulatory lobbying, who bears monitoring and compliance obligations, and whose corporate practices determine the quality of the data itself.

This paper fills that gap by conducting a systematic 14-year longitudinal analysis of ownership concentration in the GHGRP. We track three related questions:

1. Has the ownership of U.S. industrial emissions infrastructure consolidated between 2010 and 2023?
2. How does concentration vary across major industrial sectors, and does the picture change when facilities are weighted by emissions rather than counted equally?
3. Do standard concentration metrics agree with one another, and what are the policy implications when they do not?

The third question proved to be the most consequential. We computed both top-N cumulative concentration (the share held by the largest N firms) and the Herfindahl-Hirschman Index (the sum of squared market shares used in DOJ antitrust review). In petroleum refining, the two metrics tell strikingly different stories: the top 10 parents control 54% of facilities (80% of emissions), but the sector's HHI of 849 falls comfortably below the DOJ's 1,500 threshold for "moderately concentrated." Both numbers are correct. They are measuring different structural properties of the same market, and policy arguments that conflate them will produce flawed conclusions.

The paper also contributes a spatial dimension often missing from market-structure analyses. Approximately 7.7 million Americans live within 10 km of infrastructure owned by just two of the 3,327 parent companies (Kinder Morgan and Energy Transfer), which together hold 415 facilities. The Gulf Coast corridor from South Texas to the Florida panhandle hosts 24% of all reporting facilities while holding 16% of the U.S. population, a 1.5x overrepresentation. These spatial findings connect ownership concentration to questions of environmental justice and population exposure that purely economic analyses would miss.

All of this sits against a regulatory development that lends the work urgency. In September 2025, EPA proposed permanently removing 46 source categories from the GHGRP (EPA, 2025). If finalized, most industrial sources would stop reporting after Reporting Year 2024, and the 14-year longitudinal dataset underlying this paper would terminate. The market being measured is consolidating. The measurement apparatus is being dismantled. This coincidence is the practical motivation for publishing the analysis now.

The remainder of the paper is organized as follows. Section 2 reviews existing literature on industrial emissions ownership and concentration metrics. Section 3 describes the data sources and methodology. Section 4 presents the results in five subsections: the 14-year trend, the 2023 cross-section, sector-level decomposition, emissions-weighted concentration, and the HHI divergence finding. Section 5 provides a basin-level counter-analysis. Section 6 discusses policy implications, limitations, and directions for future work. Section 7 concludes.

## 2. Literature and Context

### 2.1 Ownership Concentration in Emissions-Intensive Industries

The question of who owns emissions infrastructure sits at the intersection of industrial organization economics and environmental policy. A small body of work addresses this directly. Heede (2014) traced 63% of cumulative industrial CO2 and methane emissions between 1854 and 2010 to just 90 entities (the "Carbon Majors" study), demonstrating that historical emissions are highly concentrated at the entity level. The Climate Accountability Institute has maintained and updated this dataset, most recently through 2018 (Heede, 2019). However, the Carbon Majors framework attributes emissions to the *producers* of fossil fuels rather than to the *operators* of emissions-reporting infrastructure, making it complementary to rather than overlapping with the GHGRP-based analysis presented here.

Within the U.S. specifically, Brandt et al. (2014) and Alvarez et al. (2018) analyzed methane emissions from the oil and gas sector, finding significant discrepancies between EPA inventories and top-down estimates derived from atmospheric observations. Their work highlights the accuracy limitations of self-reported data but does not examine the ownership structure of reporting entities.

The environmental justice literature has extensively documented the co-location of industrial facilities and disadvantaged communities, particularly along the Gulf Coast corridor (Bullard, 1990; Lerner, 2005; Terrell and St. Julien, 2022). The Louisiana stretch from Baton Rouge to New Orleans, frequently termed "Cancer Alley," has been a focal point for research on cumulative pollution burden (Castellon, 2024). Our spatial analysis contributes to this literature by quantifying the population within fixed-radius buffers of facilities owned by specific parent companies, providing a bridge between ownership-level and community-level analyses.

### 2.2 Concentration Metrics: Top-N vs. HHI

The distinction between top-N concentration ratios (CR-k) and the Herfindahl-Hirschman Index is well established in industrial organization theory. Tirole (1988, Chapter 5) provides the standard treatment. CR-k measures the cumulative market share of the k largest firms; HHI sums the squared shares of all firms in the market. The two metrics can diverge substantially when market share is distributed relatively evenly across the top firms (high CR-k, low HHI) versus concentrated in one or two dominant players (both high CR-k and high HHI).

The U.S. Department of Justice and Federal Trade Commission use HHI as the primary structural screen in horizontal merger review. The 2010 Horizontal Merger Guidelines establish three tiers: unconcentrated (HHI below 1,500), moderately concentrated (1,500 to 2,500), and highly concentrated (above 2,500) (DOJ/FTC, 2010). While these thresholds were designed for product markets and pricing concerns rather than emissions infrastructure, they provide a well-understood benchmark for interpreting concentration levels.

To our knowledge, no prior study has applied both CR-k and HHI systematically across sectors of the GHGRP, or examined the divergence between the two in the context of environmental monitoring and policy.

### 2.3 Midstream Consolidation

The consolidation of U.S. midstream natural gas infrastructure is well documented in industry and financial literature but underrepresented in academic environmental policy research. The wave of midstream M&A that accelerated after 2010 was driven by the shale gas revolution, which created massive demand for gathering, processing, and long-haul pipeline capacity (Makholm, 2012). Master limited partnerships (MLPs) like Kinder Morgan, Energy Transfer, Enterprise Products, and Williams used the MLP structure's tax advantages and yield-oriented investor base to fund acquisition-driven growth.

Kinder Morgan's trajectory illustrates the pattern: from 24 GHGRP-reporting facilities in 2010 to 231 in 2023, an 862% increase almost entirely through acquisition. Energy Transfer grew from 19 to 184 over the same period (868%). These two companies alone account for 415 of the 8,106 facilities in the 2023 GHGRP. The Florida Gas Transmission pipeline, a 50/50 joint venture between them, adds 17 jointly owned facilities, demonstrating that the two largest midstream consolidators are also operationally interlinked on critical infrastructure.

## 3. Data and Methodology

### 3.1 Data Sources

The analysis draws on four primary data sources, all publicly available:

1. **EPA GHGRP Parent Company Dataset** (`ghgp_data_parent_company.xlsb`): Annual worksheets for reporting years 2010 through 2023, containing facility ID, parent company name, ownership percentage, and related identifiers. This is the primary ownership dataset. Downloaded from EPA's Envirofacts system (EPA, 2024a).

2. **EPA GHGRP 2023 Data Summary Spreadsheets** (`ghgp_data_2023.xlsx`): Facility-level data including geographic coordinates (latitude, longitude), total CO2e emissions, and sector/subpart classifications across 10 subpart-specific worksheets. Downloaded from EPA's GHGRP data publication page (EPA, 2024b).

3. **U.S. Census Bureau Population Estimates**: County-level population estimates for 2020-2023 (`co-est2023-alldata.csv`) from the Population Estimates Program, and tract-level population from the American Community Survey 5-year estimates, Table B01003, 2019-2023 vintage (Census Bureau, 2024a; 2024b).

4. **U.S. Census Cartographic Boundary Files**: State boundaries (5m resolution), county boundaries (500k resolution), and census tract boundaries (500k resolution) for spatial analysis (Census Bureau, 2024c).

### 3.2 Ownership Attribution

GHGRP facilities may report multiple parent companies with varying ownership stakes. We adopt two attribution rules depending on the analysis:

**Any-stake union rule (for facility-count concentration):** A facility counts toward a parent company if that parent appears in any ownership row for the facility. When computing the top-N share, we identify the N parents with the most unique facilities, then count the total unique facilities in which any of those N parents holds any stake. This avoids double-counting facilities shared by multiple top-N parents (e.g., Florida Gas Transmission stations owned 50/50 by Kinder Morgan and Energy Transfer).

**Ownership-percentage-weighted allocation (for emissions-weighted concentration):** Each facility's total CO2e emissions are allocated across its listed parents proportional to their reported ownership percentages. Where ownership percentages are null or missing, emissions are split equally among listed parents.

### 3.3 Sector Classification

We classify facilities into four major sectors based on EPA subpart designation:

- **Petroleum refining**: Subpart Y
- **Oil and gas (petroleum and natural gas systems)**: Subpart W
- **Petrochemicals**: Subpart X
- **Electric power**: Subpart D

Facilities may report under multiple subparts. For sector-specific analyses, a facility is included in a sector if it reports emissions under the corresponding subpart in the 2023 data summary.

### 3.4 Concentration Metrics

**Top-N concentration ratio (CR-N):** The share of total facilities (or emissions) held by the N largest parent companies. We use N=10 throughout for comparability.

**Herfindahl-Hirschman Index (HHI):** Computed as the sum of squared percentage market shares across all firms:

$$HHI = \sum_{i=1}^{N} s_i^2$$

where *s_i* is firm *i*'s market share expressed as a percentage (0-100 scale). We compute HHI on both facility-count shares and emissions-weighted shares. DOJ thresholds: unconcentrated (< 1,500), moderately concentrated (1,500 - 2,500), highly concentrated (> 2,500).

### 3.5 Spatial Analysis

All spatial calculations use the NAD83 Conus Albers Equal Area projection (EPSG:5070) to ensure accurate distance and area measurement. Euclidean buffers of 3 km and 10 km are constructed around each facility with valid coordinates. Population exposure is estimated using area-weighted tract-population allocation: each Census tract's total population is allocated to an overlapping buffer in proportion to the geometric intersection area relative to the total tract area.

Of the 8,106 facilities in the 2023 GHGRP, 7,538 (93%) have coordinates in the data summary spreadsheets. The 568 facilities lacking coordinates are primarily small natural gas local distribution companies. These are included in ownership and concentration analyses but excluded from spatial computations.

**Validation:** The sum of tract-level ACS population estimates used yields 335.6 million, within 0.3% of the Census Bureau's 2023 national population estimate. County-population join match rate: 3,131 of 3,221 counties (97.2%). Tract-population join match rate: 85,045 of 85,186 tracts (99.8%).

### 3.6 Reproducibility

All analysis scripts, intermediate data files, and per-phase methodology notes are published in a public GitHub repository. The pipeline runs from raw EPA and Census data to all figures and summary statistics. No manual data transformations are performed outside of code.

## 4. Results

### 4.1 14-Year Ownership Trend

The top-10 parent-company share of GHGRP reporting facilities increased from 11.7% in 2010 to 16.7% in 2023, an absolute gain of 5.1 percentage points and a relative increase of 43% (Figure 1).

![14-year concentration trend](viz/ghgrp_14yr_trend_recomputed.png)
*Figure 1: Top-10 parent share of GHGRP-reporting facilities, 2010 to 2023, computed using the any-stake union method. Source: EPA GHGRP Parent Company Dataset, annual sheets.*

The trend exhibits three distinct phases. From 2010 to 2014, the top-10 share oscillated between 9.4% and 11.8%, with no clear directional trend. In 2015, a step-change occurred: the share jumped from 11.8% to 13.6% in a single year. This coincides with peak midstream M&A activity and an EPA reclassification of parent-company naming conventions that consolidated several reporting variants into canonical corporate entities. From 2015 to 2023, the trend has been consistently upward, reaching 16.7% in the final year of data.

The denominator tells its own story. Total unique parent companies declined from 4,506 in 2014 to 3,327 in 2023, a 26% reduction, while total facilities decreased only modestly from 8,731 to 8,106 (7%). More facilities per parent, fewer parents per facility. This consolidation signal is independent of how the "top 10" is defined.

Only four parent entities appear in the top 10 for more than eight of the 14 years: the U.S. Government, Waste Management, Republic Services, and Kinder Morgan. The remaining slots cycle as mergers, spin-offs, and corporate restructurings shuffle the roster. Corporate structures are fluid; emissions infrastructure is fixed.

### 4.2 The 2023 Cross-Section

In 2023, the top 10 parent companies by facility count are:

| Rank | Parent Company | Facilities | Primary Sector |
|------|---------------|-----------|----------------|
| 1 | Kinder Morgan Inc. | 231 | Pipeline/midstream |
| 2 | Waste Management Inc. | 225 | Waste |
| 3 | Energy Transfer LP | 184 | Pipeline/midstream |
| 4 | Republic Services Inc. | 177 | Waste |
| 5 | Berkshire Hathaway Inc. | 130 | Diversified |
| 6 | TransCanada Pipeline USA Ltd. | 116 | Pipeline/midstream |
| 7 | U.S. Government | 85 | Various |
| 8 | The Williams Cos. Inc. | 81 | Pipeline/midstream |
| 9 | Enterprise Products Partners LP | 75 | Pipeline/midstream |
| 10 | Phillips 66 | 72 | Refining/midstream |

*Table 1: Top 10 GHGRP parent companies by unique facility count, 2023.*

![Top 10 parent companies bar chart](viz/ghgrp_top10_barchart.png)
*Figure 2: Top 10 GHGRP parent companies by facility count, 2023 vs. 2010. Pipeline and midstream energy operators drive the growth trajectory.*

The composition is dominated by two sectors: midstream natural gas (six of the top 10) and waste management (two). The growth trajectory is concentrated entirely in the midstream companies. Waste Management and Republic Services have held stable facility counts across the full 14-year period. The midstream operators have grown through acquisition: Kinder Morgan from 24 to 231 facilities (+862%), Energy Transfer from 19 to 184 (+868%), Enbridge from 26 to 110 (+323%).

Seventeen facilities are jointly owned by Kinder Morgan and Energy Transfer through the Florida Gas Transmission pipeline system, a 50/50 joint venture running from south Texas through Louisiana, Mississippi, and Alabama into central Florida. Under the any-stake union rule, these facilities count toward both parents' individual totals but are counted only once in the combined top-10 share calculation.

![National hero map of KM and ET facilities](viz/ghgrp_hero_map_2023.png)
*Figure 3: 2023 GHGRP facilities in CONUS with Kinder Morgan (red) and Energy Transfer (orange) highlighted. The two operators together hold 415 facilities, including 17 jointly owned via the Florida Gas Transmission pipeline system.*

![Gulf Coast corridor population density with facilities overlaid](viz/ghgrp_corridor_map_2023.png)
*Figure 4: The Gulf Coast corridor from South Texas to the Florida panhandle. 1,840 GHGRP facilities in a band holding 54.4 million residents. The corridor carries 1.5x its population share of large industrial emitters.*

![Population exposure map with 10km buffers](viz/ghgrp_exposure_map_2023.png)
*Figure 5: Population exposure to KM and ET facilities. 7.7 million Americans live within 10 km of the combined 391-facility footprint. Tract-level population density shown in greyscale under the buffer polygons.*

### 4.3 Sector-Level Concentration

Table 2 reports top-10 concentration by facility count for four major sectors:

| Sector | Facilities | Parents | Top-10 Share (%) | Multiplier vs. GHGRP |
|--------|-----------|---------|-------------------|---------------------|
| Refineries (Subpart Y) | 133 | 59 | 54.1 | 3.2x |
| Oil & Gas (Subpart W) | 1,433 | 593 | 27.1 | 1.6x |
| Petrochemicals (Subpart X) | 462 | 208 | 25.8 | 1.5x |
| Power Plants (Subpart D) | 1,320 | 596 | 23.6 | 1.4x |
| GHGRP-wide | 8,106 | 3,327 | 16.7 | 1.0x |

*Table 2: Top-10 parent share by sector, facility count basis, 2023.*

![Sector concentration comparison bar chart](viz/ghgrp_sector_concentration_2023.png)
*Figure 6: Top-10 parent share by sector, 2023. Petroleum refining is the outlier, with 10 parents controlling 54% of facilities in a sector of only 133 facilities.*

Petroleum refining is the clear outlier. In a sector of only 133 facilities nationwide, 10 parent companies control 72. The top three (Valero, 14; Marathon, 13; Phillips 66, 12) together hold 29% of all U.S. refineries. This concentration reflects three decades of downstream divestiture by integrated oil majors and acquisition by mid-cap pure-play refiners. Five of the 10 largest U.S. refining parents by facility count did not exist in their current corporate form 15 years ago.

![National refineries operator map](viz/ghgrp_refineries_map_2023.png)
*Figure 7: 133 U.S. petroleum refineries colored by parent company. Gulf Coast, Midwest refining belt, and West Coast clusters visible.*

Oil and gas (Subpart W) is the second most concentrated sector. The top 10 includes both midstream operators who also appear in the GHGRP-wide top 10 (Energy Transfer, Kinder Morgan, Enterprise Products, Williams, Enbridge) and sector-specific names (Targa Resources, MPLX, EOG Resources, ExxonMobil, Phillips 66). The 27.1% top-10 share represents a 1.6x multiplier over the GHGRP baseline.

Power plants are the least concentrated major sector. The 23.6% top-10 share reflects the historical structure of U.S. electricity markets: geographic monopolies under regulation, followed by partial deregulation that preserved regionally fragmented ownership. No single power operator holds more than 44 of the 1,320 facilities.

Petrochemicals (25.8%) sits between oil and gas and power. The sector's top three are industrial gas companies (Air Products, Linde, Air Liquide), not the commodity chemical producers most associated with chemical-industry consolidation.

### 4.4 Emissions-Weighted Concentration

When facilities are weighted by CO2e emissions rather than counted equally, concentration increases across every sector (Table 3):

| Sector | Count Share (%) | Emissions Share (%) | Delta (pp) |
|--------|----------------|--------------------|----|
| Refineries | 54.1 | 79.6 | +25.5 |
| Petrochemicals | 25.8 | 52.6 | +26.8 |
| Oil & Gas | 27.1 | 35.2 | +8.1 |
| Power Plants | 23.6 | 35.9 | +12.2 |
| GHGRP-wide | 16.7 | 21.2 | +4.4 |

*Table 3: Top-10 share by facility count vs. emissions weight, 2023.*

![Facility count vs emissions weight by sector](viz/ghgrp_emissions_weighted_2023.png)
*Figure 8: Top-10 share by facility count vs. by emissions weight, per sector. Refineries pass 80% by emissions. Petrochemicals more than doubles. Every sector is more concentrated when weighted by emissions than by count.*

The uniform pattern, that concentration increases when weighted by emissions, indicates that the largest owners operate facilities that are disproportionately emissions-intensive. This is structurally consistent with acquisition strategies that target older, larger-scale assets.

One name surfaces in the emissions-weighted oil and gas ranking that does not appear in the facility-count top 10: **Hilcorp Energy Company**, the second-largest Subpart W emitter (14.5 million metric tons CO2e, 5.6% of sector emissions) despite holding fewer facilities than the count-based top 10. Hilcorp's business model of acquiring mature, high-intensity upstream assets from integrated majors (including former BP operations in Alaska and ConocoPhillips assets in the San Juan Basin) makes it nearly invisible on a count basis but highly significant on an emissions basis. This illustrates how the choice of metric shapes which operators are visible in concentration analysis.

### 4.5 The HHI Divergence

The central finding of this paper emerges when we compute the Herfindahl-Hirschman Index alongside the top-10 concentration ratios (Table 4):

| Sector | Count HHI | Emissions HHI | DOJ Classification |
|--------|----------|--------------|-------------------|
| Refineries | 432 | 849 | Unconcentrated |
| Petrochemicals | 127 | 363 | Unconcentrated |
| Oil & Gas | 114 | 181 | Unconcentrated |
| Power Plants | 84 | 183 | Unconcentrated |
| GHGRP-wide | 46 | 78 | Unconcentrated |

*Table 4: HHI by sector, facility-count and emissions-weighted bases, 2023. All sectors fall below the DOJ threshold of 1,500 for "moderately concentrated."*

Every sector, including petroleum refining with its 80% emissions-weighted top-10 share, is classified as "unconcentrated" under DOJ standards.

This is not a contradiction. It is a structural property of how the two metrics work. Top-N concentration is cumulative: it adds the market shares of the largest firms. HHI is dispersive: it squares each share, which amplifies dominance by individual firms but is insensitive to cumulative share distributed evenly across several players.

An 80% top-10 emissions share can arise from two very different distributions:

- Ten firms each at 8%: HHI contribution from these ten firms alone is 10 x 64 = 640
- One firm at 70% plus a long tail: HHI from the dominant firm alone is 4,900

U.S. petroleum refining in 2023 approximates the first distribution. The top three emitters (ExxonMobil at 14.8%, Marathon at 14.8%, Valero at 11.6%) hold comparable shares, and the remaining seven firms in the top 10 range from 3% to 9.5%. The result is a high CR-10 with a relatively low HHI. This market structure is best described as a **distributed oligopoly**: high cumulative concentration shared across a group of comparable-sized operators, none of which holds classical market power individually.

The policy implications of this divergence are substantial. Top-N concentration is relevant for concerns about lobbying coordination (a dozen CEOs can coordinate; three thousand cannot), decarbonization leverage (a commitment from Valero affects a meaningful share of sector output immediately), and monitoring integrity (data quality depends on a small number of corporate compliance practices). HHI concentration is relevant for pricing and market-abuse concerns, the domain of antitrust enforcement, and for evaluating whether specific mergers would create harmful market power.

Both are legitimate concerns. They are different concerns. Analysis and policy advocacy that conflates them, arguing from top-N numbers toward antitrust conclusions or from HHI numbers toward claims that markets are "competitive," will produce flawed results.

## 5. Basin-Level Counter-Finding

The sector-level picture of oil and gas concentration (27.1% top-10 share) obscures a fundamentally different competitive structure at the geographic level of production.

Subpart W facilities report a basin attribute identifying their geological operating basin. When we decompose the sector by basin, the fragmentation is striking (Table 5):

| Basin | Facilities | Parents | Top-1 Share (%) | Top-5 Share (%) |
|-------|-----------|---------|----------------|----------------|
| Permian | 157 | 130 | 3.2 | 10.2 |
| Gulf Coast | 89 | 68 | 5.6 | 15.7 |
| Appalachian | 81 | 58 | 6.2 | 19.8 |
| Anadarko | 56 | 48 | 3.6 | 17.9 |
| Williston | 46 | 38 | 4.3 | 21.7 |
| Arkla | 32 | 26 | 6.3 | 31.3 |

*Table 5: Ownership concentration in the six largest U.S. oil and gas basins by GHGRP facility count, 2023.*

![Basin-level ownership concentration](viz/ghgrp_basin_ownership_2023.png)
*Figure 9: Top-5 parent share per basin for the six largest U.S. oil and gas basins. Basin-level ownership is much more fragmented than sector-level ownership. The Permian has 130 parents, with the top operator holding only 3.2% of basin facilities.*

The Permian Basin, the largest by facility count, has 157 facilities owned by 130 different parent companies. The largest operator holds 3.2% of basin facilities. The top 5 combined hold 10.2%. No basin in the top six approaches the sector-level top-10 share of 27.1%. Even Arkla, the most concentrated basin at 31.3% top-5 share, is driven by the small total facility count (32) rather than dominant individual operators.

The resolution of this apparent paradox lies in the distinction between upstream and midstream operations. Basin-level production is fragmented across dozens of small and mid-cap operators. But the midstream infrastructure that gathers, processes, and transports basin production into interstate pipeline networks is consolidated under a small number of operators: Kinder Morgan, Energy Transfer, Enterprise Products, Williams, Enbridge, and MPLX. These midstream operators report to the same Subpart W but operate at a different structural level of the value chain.

When a journalist or policy analyst writes about "consolidation in U.S. oil and gas," they are almost always describing the midstream network. Upstream production, especially in the shale basins, is not consolidated at the basin level. Policy aimed at upstream wells will not achieve the same structural effects as policy aimed at midstream pipelines. The levers sit at different altitudes of the value chain.

## 6. Discussion

### 6.1 Policy Implications

The findings suggest three distinct policy-relevant conclusions:

**First, top-N concentration in U.S. industrial emissions is real, significant, and still increasing.** The 43% relative growth in the top-10 share over 13 years is a structural fact. For policy domains where cumulative control matters, including lobbying coordination, compliance infrastructure, and decarbonization leverage, this concentration is directly relevant. A regulatory framework designed for thousands of independent operators is interfacing with a market where a handful of midstream companies span the national pipeline network.

**Second, the same markets are unconcentrated by classical antitrust standards.** No GHGRP sector crosses the DOJ threshold for "moderately concentrated." Arguments that invoke monopoly or market-abuse framings for these sectors are not supported by the standard metric. This does not mean these markets are "competitive" in any normatively desirable sense for environmental outcomes. It means that the competition-economics framework and the environmental-oversight framework are measuring different things.

**Third, the dismantlement of GHGRP reporting would close the window on this analysis permanently.** Parent-company ownership data must be collected continuously; consolidation trends cannot be reconstructed after the fact. EPA's September 2025 proposal to remove 46 source categories would eliminate reporting for a large share of the facilities analyzed here. The timing, proposing to reduce monitoring while the market being monitored is consolidating, represents a significant gap in the rationale for the proposed rule.

### 6.2 Limitations

Several limitations should be noted:

1. **Parent-company name canonicalization.** The GHGRP parent-company dataset uses string-exact names that vary across years (e.g., "ENERGY TRANSFER PARTNERS, LP" vs. "ENERGY TRANSFER LP"). EPA performed a major name standardization between 2014 and 2015, which partially explains the step-change in that year. Our analysis relies on the names as reported without additional entity resolution.

2. **Self-reported emissions.** GHGRP emissions are self-reported by facilities. Satellite-based atmospheric inversions from multiple research groups find aggregate methane emissions 30-60% higher than GHGRP totals for some sub-sectors (Alvarez et al., 2018; Chen et al., 2022). The facility-level accuracy of self-reported data is an active area of research and may affect emissions-weighted concentration calculations.

3. **Missing coordinates.** 568 of 8,106 facilities (7%) lack geographic coordinates in the 2023 data summary spreadsheets. These are included in ownership analyses but excluded from spatial computations.

4. **Proximity vs. exposure.** The population buffer analysis quantifies geographic adjacency, not health exposure. Emissions dispersion, wind patterns, stack height, chemical composition, and dose-response relationships are separate analyses requiring different datasets and methodologies.

5. **Snapshot vs. longitudinal sector analysis.** The sector and basin-level analyses use only 2023 data. Whether sector-level concentration has trended similarly to the GHGRP-wide trend is an open question for future work.

6. **Boundary of analysis.** The GHGRP covers facilities above 25,000 metric tons CO2e/year. Smaller emitters and diffuse sources (transportation, agriculture, residential) are excluded. The concentration findings apply to the large-emitter segment, not to total U.S. emissions.

### 6.3 Future Directions

Three extensions would strengthen the analysis. First, applying the 14-year longitudinal trend decomposition at the sector level (particularly for oil and gas, to trace the midstream rollup timeline). Second, integrating satellite-derived emissions estimates (from MethaneSAT, Carbon Mapper, or GHGSat) to compare self-reported concentration against observation-based concentration. Third, linking the ownership data to financial performance, lobbying expenditure, and regulatory-comment activity to test whether top-N concentration predicts coordinated political behavior in ways HHI does not.

## 7. Conclusion

Fourteen years of GHGRP parent-company data reveal a clear consolidation trend in U.S. industrial emissions infrastructure, driven by acquisition-led growth in midstream natural gas. The top 10 parent companies hold 16.7% of all reporting facilities, up from 11.7% in 2010. Within sectors, concentration is sharper: 54% in petroleum refining by facility count, 80% by emissions weight.

But the paper's central contribution is not the consolidation finding itself. It is the demonstration that two standard concentration metrics, top-N share and HHI, tell structurally different stories about the same market. Petroleum refining is simultaneously "80% controlled by 10 companies" and "unconcentrated by DOJ standards." Both are true. They measure different structural properties, and the policy questions they inform are correspondingly different.

The distinction between distributed oligopoly (high top-N, low HHI) and classical monopoly (high top-N, high HHI) has been understood in industrial organization theory for decades. Its application to emissions infrastructure is new, and its implications for environmental monitoring policy are direct: the institutional tools for tracking and regulating these markets need to be calibrated to the market structure that actually exists, not to the market structure that familiar rhetoric assumes.

The window for conducting this analysis may be closing. If the September 2025 EPA proposal to remove 46 source categories from the GHGRP is finalized, most of the longitudinal data underlying this work will stop being generated. It would be historically unfortunate to dismantle the measurement system at the exact moment it reveals the structure most worth measuring.

---

## References

Alvarez, R. A., Zavala-Araiza, D., Lyon, D. R., Allen, D. T., Barkley, Z. R., Brandt, A. R., ... & Hamburg, S. P. (2018). Assessment of methane emissions from the U.S. oil and gas supply chain. *Science*, 361(6398), 186-188.

Brandt, A. R., Heath, G. A., Kort, E. A., O'Sullivan, F., Petron, G., Jordaan, S. M., ... & Harriss, R. (2014). Methane leaks from North American natural gas systems. *Science*, 343(6172), 733-735.

Bullard, R. D. (1990). *Dumping in Dixie: Race, Class, and Environmental Quality*. Westview Press.

Castellon, M. J. (2024). Cancer Alley and the fight against environmental racism in Louisiana. *Environmental Justice*, 17(3), 145-153.

Census Bureau. (2024a). County Population Estimates, 2020-2023. U.S. Census Bureau Population Estimates Program.

Census Bureau. (2024b). American Community Survey 5-Year Estimates, Table B01003, 2019-2023. U.S. Census Bureau.

Census Bureau. (2024c). Cartographic Boundary Files. U.S. Census Bureau.

Chen, Y., Sherwin, E. D., Berman, E. S. F., Jones, B. B., Gordon, M. P., Wetherley, E. B., ... & Brandt, A. R. (2022). Quantifying regional methane emissions in the New Mexico Permian Basin with a comprehensive aerial survey. *Environmental Science & Technology*, 56(7), 4317-4323.

DOJ/FTC. (2010). *Horizontal Merger Guidelines*. U.S. Department of Justice and Federal Trade Commission.

EPA. (2024a). Greenhouse Gas Reporting Program: Parent Company Dataset, Reporting Years 2010-2023. U.S. Environmental Protection Agency.

EPA. (2024b). Greenhouse Gas Reporting Program: 2023 Data Summary Spreadsheets. U.S. Environmental Protection Agency.

EPA. (2025). Proposed Rule: Revisions to the Greenhouse Gas Reporting Rule. Federal Register, September 2025.

Heede, R. (2014). Tracing anthropogenic carbon dioxide and methane emissions to fossil fuel and cement producers, 1854-2010. *Climatic Change*, 122(1-2), 229-241.

Heede, R. (2019). Carbon Majors: Updating activity data, adding entities, & calculating emissions: A Training Manual. Climate Accountability Institute.

Lerner, S. (2005). *Diamond: A Struggle for Environmental Justice in Louisiana's Chemical Corridor*. MIT Press.

Makholm, J. D. (2012). *The Political Economy of Pipelines: A Century of Comparative Institutional Development*. University of Chicago Press.

Terrell, K. A., & St. Julien, G. (2022). Air pollution is linked to higher cancer rates among Black or impoverished communities in Louisiana. *Environmental Research Letters*, 17(1), 014033.

Tirole, J. (1988). *The Theory of Industrial Organization*. MIT Press.

---

## Appendix A: Code Availability

All analysis scripts, processed data files, and per-phase methodology notes are available in a public GitHub repository:

**Repository:** [to be inserted — github.com/salamituns/ghgrp-consolidation]

The repository includes:
- Raw-to-processed data pipeline scripts (Python, using pandas, geopandas, matplotlib, shapely)
- Phase-by-phase methodology documents with self-audit tables
- All figures in publication resolution
- Intermediate JSON result files for independent verification

**Software requirements:** Python 3.10+, pandas, geopandas, matplotlib, shapely, pyxlsb, openpyxl, contextily.

---

## Appendix B: Supplementary Tables

### B.1 Year-by-Year Top-10 Concentration

| Year | Facilities | Parents | Top-10 Share (%) |
|------|-----------|---------|-----------------|
| 2010 | — | — | 11.7 |
| 2011 | — | — | 9.4 |
| 2012 | — | — | 10.0 |
| 2013 | — | — | 10.8 |
| 2014 | — | — | 11.8 |
| 2015 | — | — | 13.6 |
| 2016 | — | — | 14.0 |
| 2017 | — | — | 14.0 |
| 2018 | — | — | 14.0 |
| 2019 | — | — | 14.8 |
| 2020 | — | — | 15.4 |
| 2021 | — | — | 16.1 |
| 2022 | — | — | 16.7 |
| 2023 | — | — | 16.7 |

*Table B.1: Top-10 parent share of GHGRP facilities by reporting year, any-stake union method.*

### B.2 Refinery Top-10 by Emissions

| Parent Company | Emissions (MMT CO2e) | Sector Share (%) |
|----------------|---------------------|-----------------|
| ExxonMobil | 27.2 | 14.8 |
| Marathon Petroleum | 27.2 | 14.8 |
| Valero Energy | 21.3 | 11.6 |
| Phillips 66 | 18.9 | 10.3 |
| Chevron | 12.9 | 7.1 |
| PBF Energy | 10.8 | 5.9 |
| BP America | 7.8 | 4.3 |
| PDV America (CITGO) | 7.8 | 4.3 |
| Koch Industries | 7.0 | 3.8 |
| Aramco Services | 5.0 | 2.7 |

*Table B.2: Top 10 refinery parent companies by ownership-weighted CO2e emissions, 2023.*

---

*Corresponding author: Olatunde Salami, Stratdevs (Tareony). Contact: salamituns@gmail.com*

*Analysis handle: [@salamituns](https://x.com/salamituns)*
