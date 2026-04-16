# The Oligopoly of Pollution: A Full Audit of Who Controls America's Industrial Emissions

## A 14-year analysis of ownership, geography, and market structure in the U.S. Greenhouse Gas Reporting Program

---

I started this project with one question: *if you trace every facility reporting to the EPA's Greenhouse Gas Reporting Program back to its parent company, and then ask who the parents are, what does the map actually look like?*

What I expected was the familiar story: a few giant corporations own most of the pollution, and the consolidation trend is getting worse. That's the version in most climate coverage. It's roughly the version I had published myself, on LinkedIn and Substack, based on the first pass of the data.

What I found, after pulling the threads for several weeks, is more specific than that. The trend is real. The shape of it is not what the shorthand describes. And when I applied a second concentration metric to double-check the first, the two metrics told different stories about the same industry. That disagreement turned out to be the most useful finding in the whole project.

This piece consolidates a seven-part analysis into a single reference document. Every number is reproducible from public EPA data. Every map and chart can be regenerated from the scripts in the linked repository. If you're an environmental policy analyst, a financial journalist covering pipelines, an academic using GHGRP data, or someone who debates U.S. energy market structure, you are the reader I had in mind.

The short version of what follows:

- Over 13 years, the top 10 parent companies went from 11.7% to 16.7% of reporting facilities. **The trend is real. The magnitude is 43% relative growth.**
- Two of those 10 companies (Kinder Morgan and Energy Transfer) together hold 415 facilities. Roughly 7.7 million Americans live within 10 km of them.
- Petroleum refining is the most concentrated sector by far: 10 parents control 54% of facilities and 80% of emissions. But run the DOJ's antitrust measure on the same market and it comes back "unconcentrated." Both are true, and the distinction matters.
- Upstream oil and gas, contrary to the sector-level picture, is diffuse at the basin level. The Permian has 130 operators. No one company holds more than 3%.
- All of this sits against EPA's September 2025 proposal to remove 46 source categories from the reporting program. The market being measured is consolidating. The measurement is about to stop.

That last point is why the work matters now. Everything below is the evidence.

> **What the GHGRP is**: the federal program, launched in 2010, that requires every U.S. facility emitting more than 25,000 metric tons of CO₂ equivalent per year to report its emissions to the EPA. In 2023, 8,106 facilities reported, across 3,327 parent companies. It is one of the most granular public industrial-emissions datasets in the world.

## The 14-year trend

The foundational question is whether ownership of U.S. industrial emissions infrastructure has actually concentrated over the life of the reporting program.

The data says yes, clearly.

![14-year concentration trend chart](ghgrp_14yr_trend_recomputed.png)
*Figure 1: Top-10 parent share of GHGRP-reporting facilities, 2010 to 2023. Source: EPA GHGRP Parent Company Dataset.*

Three features of the trend matter.

**The direction is unambiguous.** The top-10 share rose steadily from 11.7% to 16.7% over 13 years. Absolute gain of 5.1 percentage points. Relative growth of 43%. The trend is still active. In the latest year of data, it had not plateaued.

**2015 is the step change.** Between 2014 and 2015, the top-10 share jumped from 11.8% to 13.6%, a 1.8-point gain in one year. Two things coincide in 2015. Midstream energy M&A peaked. The EPA also reclassified parent-company names, consolidating several reporting variants into canonical corporate entities. The jump is partly real market consolidation and partly methodological housekeeping. Either way, the post-2015 landscape is fundamentally more concentrated than the pre-2015 one, and it has stayed that way for eight years running.

**The denominator tells its own story.** Total unique parent companies dropped from 4,506 in 2014 to 3,327 in 2023, a 26% decline. Over the same period, total facilities barely moved, from 8,731 to 8,106. More facilities per parent. Fewer parents per facility. The consolidation shows up cleanly in this denominator too, and it doesn't depend on any specific definition of "top 10."

## The top 10 in 2023

Here's the 2023 league table:

![Top 10 parent companies bar chart](ghgrp_top10_barchart.png)
*Figure 2: Top 10 GHGRP parent companies by facility count, 2023 vs. 2010. Pipeline and midstream energy operators drive the growth trajectory.*

A few things stand out.

Kinder Morgan, Waste Management, and Energy Transfer make up the top three. Two pipelines and a trash company. Republic Services, another trash operator, sits at rank 4. This is not what most people picture when they hear "America's biggest emissions infrastructure."

The growth story is not in the waste positions, which have been stable for the entire 14 years. It is in midstream natural gas. Kinder Morgan grew from 24 facilities in 2010 to 231 today. Energy Transfer from 19 to 184. Enbridge from 26 to 110. None of them built most of that infrastructure. They bought it. They rolled up pipeline networks, compressor stations, processing plants, and local distribution systems that were previously owned by dozens of smaller regional operators.

When you plot all 415 KM and ET facilities on a national map, the pattern is unmistakable:

![National hero map of KM and ET facilities](ghgrp_hero_map_2023.png)
*Figure 3: 2023 GHGRP facilities in CONUS with Kinder Morgan (red) and Energy Transfer (orange) highlighted. The two operators together hold 415 facilities, including 17 jointly owned via the Florida Gas Transmission pipeline system.*

Two operators, one corporate footprint tracing the interstate natural gas pipeline network across the country. This is not geography-neutral consolidation. It is the buy-up of a specific physical network that happens to carry most of America's natural gas.

A detail worth calling out, because it surprised me: 17 of those 415 facilities are jointly owned by Kinder Morgan *and* Energy Transfer. Most of them are the Florida Gas Transmission pipeline, a 50/50 joint venture running from south Texas across the Deep South into central Florida. The story that treats KM and ET as competing rollups isn't wrong, but it's incomplete. At the pipeline-systems level, the two largest midstream consolidators are partnered on critical infrastructure. The oligopoly is more interconnected than the league-table framing suggests.

## The neighbors

Here is where the analysis shifts from market structure to people.

Using U.S. Census tract population estimates from the 2019-2023 American Community Survey, I computed the total population within 3 km and 10 km of any facility owned by Kinder Morgan or Energy Transfer. The buffers were built in an equal-area projection, which is important because lat-long buffers at U.S. latitudes are wrong by 30-50%.

![National exposure map with 10km buffers](ghgrp_exposure_map_2023.png)
*Figure 4: Population exposure to KM and ET facilities. 7.7 million Americans live within 10 km of the combined 391-facility footprint. Tract-level population density shown in greyscale under the buffer polygons.*

**Within 3 km: 701,744 people.**

**Within 10 km: 7,703,643 people.**

7.7 million Americans live within a 10-kilometer walk of a facility operated by just two of the 3,327 parent companies reporting to the GHGRP. That population is larger than Tennessee's. Larger than Massachusetts'. Larger than the metro populations of Denver and Seattle combined.

The combined 10 km buffer footprint covers roughly 100,000 square kilometers, about the size of Kentucky. Two companies. A Kentucky-sized shadow.

I want to be precise about what this number represents. Proximity to a facility is not the same thing as emissions exposure. A compressor station releases different pollutants than a refinery. Prevailing winds direct plumes in specific directions. Dose-response depends on distance measured in meters, not kilometers. What the 7.7 million figure quantifies is *who lives near consolidated pipeline and midstream infrastructure*, not *who is being harmed by it*. Those are related questions, but they are not the same question, and I will not pretend they are.

Where does the density show up most? The Gulf Coast.

![Gulf Coast corridor population density with facilities overlaid](ghgrp_corridor_map_2023.png)
*Figure 5: The Gulf Coast corridor from South Texas to the Florida panhandle. 1,840 GHGRP facilities in a band holding 54.4 million residents. The corridor carries 1.5x its population share of large industrial emitters.*

1,840 GHGRP facilities in a corridor that holds 54.4 million Americans. Twenty-three percent of the country's large industrial reporters, sixteen percent of the country's population, in one regional band. If facilities were distributed uniformly with population, the ratio would be 1.0. It's 1.5.

If you drive I-10 from Houston to Baton Rouge, you will pass more GHGRP-reporting facilities per hour than on any other stretch of interstate in the country. The region is sometimes called the Chemical Corridor, sometimes Cancer Alley for the Louisiana segment specifically. Whatever you call it, it is the physical manifestation of a century of industrial and petrochemical siting decisions made in response to deep-water ports, pipeline access, refining capacity, a favorable regulatory climate, and available labor. The communities along that corridor have known this for generations. What this analysis adds is a sharp number for the whole band.

Harris County, Texas, which contains Houston, is the densest node inside the densest corridor. 4.8 million people and one of the densest clusters of GHGRP reporters in the country. Dense city, dense industry, same zip codes. That coincidence is the sharpest data point in the whole series.

Not all dense regions look like this. The Atlanta metro has among the highest population densities in the country but carries relatively few GHGRP facilities. Population density alone does not predict industrial density. The Gulf Coast is what happens when historical resource geography, labor markets, infrastructure, and regulatory environment stack in the same place. Most metros don't have all four.

## Sector structure

When you zoom from the full GHGRP into individual sectors, the concentration story sharpens for some and flatlines for others.

![Sector concentration comparison bar chart](ghgrp_sector_concentration_2023.png)
*Figure 6: Top-10 parent share by sector, 2023. Petroleum refining is the outlier, with 10 parents controlling 54% of facilities in a sector of only 133 facilities.*

The outlier is petroleum refining. In a sector with only 133 reporting facilities in the entire country, 10 parent companies control 72 of them. 54%. Valero owns 14. Marathon Petroleum another 13. Phillips 66 another 12. PBF Energy 6. Those four names alone account for one out of every three U.S. refineries.

![National refineries operator map](ghgrp_refineries_map_2023.png)
*Figure 7: 133 U.S. petroleum refineries colored by parent company. Gulf Coast, Midwest refining belt, and West Coast clusters visible.*

This is not an accident of the modern market. It is the end state of 30 years of structural change. Across the 2000s and 2010s, the integrated oil majors (Chevron and ExxonMobil most visibly) divested much of their U.S. downstream refining. Some of it was to refocus on higher-margin upstream exploration. Some was to get out of a business with thin crack-spread margins and constant regulatory pressure. Either way, they sold. And mid-cap refiners bought. Valero, Marathon, PBF, HF Sinclair: these companies built scale by acquiring what the majors dropped. Phillips 66 itself is a 2012 spinoff from ConocoPhillips' downstream operations. Five of the 10 largest U.S. refiners today did not exist in their current corporate form 15 years ago.

If you're reading this as a financial analyst covering the refining sector, none of that is news. What might be new is seeing the 54% number quantified cleanly and defensibly.

**Oil and gas tells a different story.** 1,433 facilities, about 11 times the refinery count, with top-10 concentration of 27%. The names in the top 10 are largely the same midstream consolidators that dominate the overall GHGRP: Kinder Morgan, Energy Transfer, Enterprise Products, Enbridge, Williams. Five more names appear that don't make the overall top 10 because their footprint is narrowly focused on Subpart W:

- **Targa Resources**: 44 facilities, Permian and Gulf Coast gathering and processing
- **MPLX**: 33 facilities, Marathon Petroleum's midstream MLP
- **EOG Resources**: 30 facilities, pure-play upstream Permian and Eagle Ford producer
- **ExxonMobil**: 35 facilities, integrated major's upstream operations
- **Enbridge (U.S.) Inc.**: 40 facilities, pipeline system

These are the second-tier consolidators. They don't show up in the GHGRP-wide top 10 because their work is narrowly inside oil and gas. Inside the sector, they are shape-making operators.

**Power plants are the least consolidated major sector.** 1,320 facilities, 596 unique parents, no single operator owning more than 44 plants. Duke Energy, Vistra, Berkshire Hathaway, Xcel Energy, Southern Company, Entergy: all of them sit between 25 and 44 facilities apiece. This reflects how U.S. electricity markets were historically structured. Regulated utilities held geographic monopolies, and after deregulation, ownership stayed tied to specific state and regional markets. Power's top-10 concentration of 23.6% is not far from the full GHGRP baseline of 16.7%. Fragmented by the standards of U.S. industry.

**Petrochemicals** sits at 26%. The top three are industrial gas companies: Air Products & Chemicals (27 facilities), Linde (18), Air Liquide (12). That surprised me. When you hear "chemical industry consolidation" the names that usually come to mind are Dow, LyondellBasell, DuPont spinoffs. All of those operators sit below the industrial-gas majors on the ranking. The sector is shaped by gas suppliers, not commodity chemical producers.

## When you weight by emissions, the story sharpens

Facility counts are one way to measure concentration. Tons of CO₂ equivalent are another. They answer related but distinct questions. Facility count asks *who owns the infrastructure*. Emissions weight asks *who produces the pollution*.

I re-ran top-10 concentration using CO₂e tonnage, weighted by ownership percentage where available. The answers shifted across every sector:

![Facility count vs emissions weight by sector](ghgrp_emissions_weighted_2023.png)
*Figure 8: Top-10 share by facility count vs. by emissions weight, per sector. Refineries pass 80% by emissions. Petrochemicals more than doubles. Every sector is more concentrated when weighted by emissions than by count.*

Refineries go from 54% to 80%. Petrochemicals more than doubles, from 26% to 53%. Power plants shift modestly, from 24% to 36%. Every sector is more concentrated by emissions weight than by facility count.

The interpretation is straightforward: the top 10 in each sector do not just own more facilities than their fair share. They own the bigger, dirtier ones.

One name stood out when I sorted the oil and gas sector by emissions instead of by count: **Hilcorp Energy**. Hilcorp is the second-largest Subpart W emitter in the country, 14.5 million metric tons of CO₂e, 5.6% of sector emissions. By facility count, Hilcorp sits outside the top 10.

Hilcorp's business model is specifically to acquire older, higher-intensity assets from the integrated majors. The former BP Prudhoe Bay operations in Alaska. ConocoPhillips' San Juan Basin. Several ExxonMobil upstream divestitures. The emissions-weighted metric surfaces this acquisition pattern in a way the count metric cannot. When a major sells off methane-leaky mature wells, the assets do not become cleaner. They just change who is reporting the leaks.

This matters for how we read divestiture headlines. A story about an oil major reducing its emissions through divestment is, at the sector level, often a story about those emissions moving to a different line on the same GHGRP ledger.

## What "concentration" actually means, precisely

Here is where the analysis got interesting in a way I did not expect.

Top-10 share is one measure of market concentration. The Herfindahl-Hirschman Index is the other, and it is the one the DOJ uses when reviewing horizontal mergers for antitrust concerns.

> **HHI**: sum of the squared market shares of every firm in a market, with shares expressed as percentages. DOJ thresholds: below 1,500 is "unconcentrated," 1,500 to 2,500 is "moderately concentrated," above 2,500 is "highly concentrated." This is the standard benchmark for U.S. merger review.

When I computed HHI on the GHGRP sectors, here is what came back:

| Sector | Facility-count HHI | Emissions-weighted HHI | DOJ category |
|---|---|---|---|
| Refineries | 432 | **849** | Unconcentrated |
| Petrochemicals | 127 | 363 | Unconcentrated |
| Oil and Gas | 114 | 181 | Unconcentrated |
| Power Plants | 84 | 183 | Unconcentrated |
| GHGRP-wide | 46 | 78 | Unconcentrated |

Every sector, including refineries, is *unconcentrated* by DOJ standards.

If you're reading that and thinking "wait, didn't you just say refineries were 80% controlled by 10 companies?" — yes. Both numbers are correct. They are measuring different things.

Top-10 share is cumulative. It adds up the market power of the largest 10 firms. HHI is dispersive. It squares each firm's share, which penalizes dominance by individual firms and rewards fragmentation even when the tail is short.

80% top-10 share can come from ten firms each holding 8% (what refineries look like) or from one firm at 70% plus a long tail of small ones. Those two distributions have wildly different HHIs. The first is around 850. The second is above 5,000.

U.S. petroleum refining in 2023 fits the first distribution. Valero at 14.8% of sector emissions, Marathon at 14.8%, Phillips 66 at 11.6%, ExxonMobil at 9.5%, PBF around 6%, and six more names between 3% and 6%. No single refiner dominates. Ten refiners collectively do.

The honest framing is **distributed oligopoly**: high top-N cumulative concentration shared across a small group of comparable-sized operators, none of which holds classical market power individually.

This distinction is the single most useful output of the entire analysis, and it took running the data twice to see it. If you are arguing that U.S. refining is "a monopoly," HHI is pointing the other way. If you are arguing it is "competitive and fragmented," 80% top-10 emissions share is pointing the other way. The real answer sits in between, and the policy implications depend entirely on which question you are trying to answer.

**Top-N concentration matters for**:
- Lobbying and policy coordination. A dozen CEOs can be in the same room. Three thousand cannot.
- Decarbonization leverage. A Valero emissions-reduction commitment affects a meaningful share of sector output immediately.
- Compliance and monitoring integrity. Ten parents carrying 80% of refinery reporting infrastructure means data quality depends on a small number of corporate practices.

**HHI concentration matters for**:
- Pricing and market-abuse concerns. The DOJ's actual domain.
- Antitrust review of specific mergers. A refinery merger would be evaluated on incremental HHI change.
- Entry conditions. HHI below 1,500 does not structurally prevent new entrants.

Both are legitimate concerns. They are different concerns. Future analyses that mix them up will be worse for it.

## The basin-level counter-finding

The last piece of the analysis pushed against the simple consolidation story hardest.

Subpart W oil and gas facilities are reported with a "Basin" attribute, identifying which geological basin they operate in. When I grouped the 2023 Subpart W facilities by basin and asked *who owns the facilities in each specific basin*, the picture fell apart:

![Basin-level ownership concentration](ghgrp_basin_ownership_2023.png)
*Figure 9: Top-5 parent share per basin for the six largest U.S. oil and gas basins. Basin-level ownership is much more fragmented than sector-level ownership. The Permian has 130 parents, with the top operator holding only 3.2% of basin facilities.*

The Permian, the largest U.S. oil and gas basin by facility count, has 157 reporting facilities owned by 130 different parent companies. The top operator in the basin holds 3.2% of facilities. The top 5 combined hold 10.2%.

Every basin in the top 6 has a top-5 share well below the Subpart W sector-level top-10 share of 27.1%. The most concentrated basin, Arkla, tops out at 31%. None of them looks like what a concentrated market would predict.

If you drive West Texas, you pass compressor stations and gas processing units owned by companies most readers outside the industry have never heard of. Lewis Energy, Scout Energy, Fourpoint Operations, Formentera, Aethon United, Coterra. Thirty, fifty, a hundred different small and mid-cap operators each holding a handful of facilities. That is what "fragmented" looks like on the ground.

So how does the Subpart W sector-level top 10 achieve its 27% share? By consolidating *midstream*. Kinder Morgan, Energy Transfer, Enterprise Products, Williams, Enbridge, MPLX. Their facilities are pipelines and processing plants that span multiple basins. At the basin level, where production happens, the picture is diffuse. At the midstream level, where basin production converges into interstate networks, the picture is consolidated.

The corrected framing: **upstream U.S. oil and gas is a fragmented market. Midstream is a consolidated network.** Both report to the GHGRP. They are genuinely different structural pictures.

This matters for how you should read energy market coverage. When a journalist writes about "consolidation in U.S. oil and gas," they are almost always describing midstream. Upstream production, especially in the shale basins, is not consolidated at the basin level. Policy aimed at the wells will not have the same effect as policy aimed at the pipelines. The levers sit at different altitudes.

## What the data supports

Pulling all of this together:

**Supported by the data**:

1. Ownership of GHGRP-reporting facilities has concentrated between 2010 and 2023. The top 10 parent companies went from 11.7% to 16.7% of facilities. The trend is real, secular, and still active.
2. The concentration is geographically patterned. The Gulf Coast corridor from South Texas to the Florida panhandle holds 23% of all reporting facilities in one regional band.
3. Roughly 7.7 million Americans live within 10 km of infrastructure owned by just two companies (Kinder Morgan and Energy Transfer), with 702,000 within 3 km.
4. Inside specific sectors, top-10 concentration is much sharper than the GHGRP baseline. Refineries are the extreme case at 54% by facility count and 80% by emissions weight.
5. Every sector is more concentrated when you weight by emissions than by facility count. Top operators own the bigger and dirtier assets.

**Not supported, despite popular framings**:

1. U.S. petroleum refining is not "highly concentrated" in the classical antitrust sense. HHI is 849, below the DOJ threshold of 1,500. High top-10 share does not mean monopoly.
2. Upstream U.S. oil and gas is not concentrated at the basin level. The Permian has 130 parent companies, and the largest holds 3%.
3. No major GHGRP sector crosses the DOJ HHI threshold for "moderately" or "highly" concentrated markets. Every one is below 1,500.

Both lists matter. The second list makes the first list credible.

If you're a policy staffer or advocate using these numbers, navigate between the lists carefully. If the concern is top-N dominance (lobbying coordination, decarbonization leverage, monitoring integrity), the data backs it strongly. If the concern is classical market-power antitrust, the data points somewhere else, toward specific sub-sectors like industrial gases where Air Products, Linde, and Air Liquide show higher dispersion-weighted concentration.

Either argument is defensible. Just don't mix them up.

## The dismantlement paradox

All of this sits against EPA's September 2025 proposal to remove 46 source categories from the reporting program.

If the rule is finalized, most of the facilities discussed here will stop reporting after Reporting Year 2024. The parent-company dataset that underlies every number in this piece is under direct regulatory threat.

The timing is extraordinary. We have just documented, using the agency's own data, that the market being measured is consolidating into fewer hands by every metric that matters for public oversight. The rational response is to strengthen monitoring. The proposed response is to reduce it.

If the rule goes through, the 14-year longitudinal series that made this analysis possible stops at 2023. Parent-company ownership data must be collected continuously. You cannot reconstruct consolidation trends after the fact. Once reporting stops, the window closes.

This is the argument for why this analysis matters now. Not because the consolidation thesis is surprising. It isn't. The industry knows, the regulators know, the environmental advocacy community knows. The reason the data matters is that the infrastructure to know it is being dismantled. Everything in this piece was reproducible in April 2026. Whether it remains reproducible in April 2027 depends on the outcome of a rulemaking currently underway.

If you work in climate policy, industrial emissions monitoring, or energy market analysis: the public comment period on the rollback is the moment to act. The 46 source categories proposed for removal include many of the specific reporters analyzed here.

If you work for one of the parent companies named in this series: your team should probably see this piece, because the questions it enables will be asked by journalists and regulators whether or not the GHGRP continues.

If you're a researcher who would use this data in your own work: the repository below has everything you need. Every number, every script, every intermediate file. Fork it, extend it, disagree with it, improve it. The methodology is specifically designed to be forkable.

---

## Methodological appendix

Everything in this piece runs off a single reproducible pipeline built from public EPA and Census data. The full codebase, processed datasets, and per-phase methodology notes are in the public repository linked at the end.

**Data sources**:

- EPA GHGRP Parent Company Dataset (`ghgp_data_parent_company.xlsb`), reporting years 2010 through 2023.
- EPA GHGRP 2023 Data Summary Spreadsheets, facility-level emissions and coordinates across 10 subpart-specific sheets.
- U.S. Census Bureau: annual county population estimates (`co-est2023-alldata.csv`) and ACS 5-year tract-level population (Table B01003, 2019-2023).
- U.S. Census Cartographic Boundary Files: state, county, and census tract geometries.

**Methodology conventions used throughout**:

1. **Any-stake union rule** for top-N concentration: a facility counts toward a parent if the parent appears in any ownership row for that facility. Top-N share equals the share of unique facilities where any top-N parent holds a stake.
2. **Ownership-percentage-weighted allocation** for emissions metrics: per-facility emissions allocated across listed parents using reported ownership percentages, with equal-split fallback when percentages are null.
3. **Spatial analysis in EPSG:5070 (NAD83 Conus Albers Equal Area)**: all distance and area calculations use a projected coordinate system in meters, not lat-long degrees.
4. **Area-weighted tract population allocation for buffer exposure**: each Census tract's population is allocated to overlapping buffers by the ratio of (buffer-tract intersection area) to (total tract area).

**Key verification checks**:

- Total U.S. population summed from tract-level ACS estimates: 335.6 million, within 0.3% of the Census Bureau's reported 2023 national total.
- County-population join match rate: 3,131 of 3,221 counties (97.2%). Connecticut counties unmatched because the state replaced counties with planning regions in 2020.
- Tract-population join match rate: 85,045 of 85,186 tracts (99.8%).

**Known limitations**:

- Parent name canonicalization is string-exact. Variant-name handling across years may produce minor noise in per-year top-10 selection.
- GHGRP emissions are self-reported. Satellite-based inversions from NASA, Carbon Mapper, and MethaneSAT find aggregate methane emissions 30-60% higher than GHGRP totals for some sub-sectors.
- 568 of 8,106 2023 facilities (7%) lack coordinates in the summary spreadsheets, primarily small natural gas local distribution companies. These are excluded from spatial analyses but included in ownership and concentration metrics.
- Proximity buffers measure geographic adjacency, not emissions exposure dose. Dispersion and air-quality modeling are separate analyses requiring different datasets.

**Full code and data**: [GitHub repository link to be inserted after publication]

**Phase-by-phase methodology documents**: each of the seven phases in the underlying analysis has its own methodology note with full self-audit tables in the repository under `methodology/`.

---

*This analysis was assembled in April 2026. Every number referenced is reproducible on the 2023 vintage of EPA GHGRP data. If the September 2025 EPA rollback proposal is finalized, the 2024 vintage may be the last year against which this series can be extended.*

*Analysis and writing: [@salamituns](https://x.com/salamituns) | Stratdevs (Tareony)*

*Correspondence and collaboration inquiries welcome.*
