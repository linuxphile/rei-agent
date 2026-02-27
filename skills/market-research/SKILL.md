---
name: market-research
description: Evaluate real estate markets and submarkets for investment viability. Use this skill whenever someone asks about a market, wants rent comps, sales comps, demographic data, employment trends, landlord-friendliness, supply pipeline, or any location-level analysis. Trigger for questions like "should I invest in [city]?", "what's the rental market like in [area]?", "pull comps for [address]", or any assessment of whether a market or submarket supports the investor's strategy. Also use when the deal analysis skill needs market context for proper underwriting.
---

# Market Research Skill

This skill provides location-level intelligence for investment decisions: demographic trends, rental and sales comps, economic indicators, supply/demand dynamics, and regulatory environment.

## Market Research Framework

Market analysis operates at three levels. Always identify which level is needed:

1. **Metro-Level** — MSA-wide trends for market selection (population, job growth, diversification)
2. **Submarket-Level** — Neighborhood/zip analysis for strategy refinement (rent trends, supply pipeline, school districts)
3. **Property-Level Comps** — Specific comparable properties for underwriting (rent comps, sales comps)

Most analyses require at least two levels. A deal analysis needs property-level comps validated against submarket trends.

## Metro-Level Analysis

### Demographic Indicators

Gather and report these metrics. Flag any metric trending negatively over 3+ years.

```
POPULATION
- Current population
- 5-year population growth rate (%)
- 10-year population growth rate (%)
- Net migration (domestic + international)
- Population growth vs. national average
- Median age and trend

INCOME
- Median household income
- Median household income growth (5yr)
- Income growth vs. rent growth (affordability gap)
- Poverty rate and trend

HOUSING
- Median home price
- Price-to-income ratio
- Homeownership rate
- Median rent (1BR, 2BR, 3BR)
- Rent-to-income ratio
- Rent growth YoY (1yr, 3yr, 5yr)
```

**Data Sources:**
- Census Bureau / American Community Survey (ACS): `data.census.gov`
- Bureau of Labor Statistics (BLS): `bls.gov`
- FRED Economic Data: `fred.stlouisfed.org`
- Zillow Research: `zillow.com/research/data/`
- Apartment List Rent Estimates: `apartmentlist.com/research`

When using web search to pull data, always note the date of the data and the source. Stale data (>18 months) should be flagged.

### Employment Analysis

Employment diversification is one of the strongest predictors of market resilience.

```
EMPLOYMENT METRICS
- Unemployment rate (current, 1yr trend, vs. national)
- Total nonfarm employment
- Job growth rate (1yr, 3yr)
- Labor force participation rate

TOP EMPLOYERS (Top 10)
For each:
- Company name
- Sector
- Approximate employee count
- Stability assessment (growing/stable/at risk)

SECTOR DIVERSIFICATION
- % of employment by sector
- Herfindahl-Hirschman Index if calculable
- Flag any single sector > 20% of employment
- Flag any single employer > 5% of total employment

GROWTH SECTORS
- Which sectors are adding jobs?
- Any major announced relocations, expansions, or closures?
- University/research institution presence
```

**Risk Flag:** If any single employer represents >5% of metro employment, or any single sector >25%, flag as "concentration risk" and explain the impact scenario if that employer/sector contracts.

### Economic Indicators

```
COST OF LIVING
- Cost of living index (vs. national = 100)
- Trajectory (rising/stable/falling)

BUSINESS CLIMATE
- State income tax rate
- Property tax rate (effective)
- Business-friendly ranking (if available)
- Major infrastructure investments planned

DEVELOPMENT ACTIVITY
- Total building permits (residential, 1yr trend)
- Multi-family permits as % of total
- Commercial development pipeline
- Infrastructure projects (transit, highways)
```

## Submarket Analysis

### Rent Comps

Pull comparable rentals for the target property type and configuration.

#### Comp Selection Criteria
- **Distance:** Within 1 mile for urban, 3 miles for suburban, 5 miles for rural
- **Property type:** Same type (SFR-to-SFR, apartment-to-apartment)
- **Configuration:** Same bedroom count, ±1 bathroom
- **Size:** Within 20% of subject square footage
- **Condition:** Similar condition class (A/B/C/D)
- **Recency:** Listed or leased within last 6 months (prefer 3 months)

#### Comp Data Points
For each comp, capture:
```
- Address
- Monthly rent
- Beds / Baths / Sqft
- Rent per sqft
- Condition (estimated)
- Days on market
- Amenities (garage, W/D, updated kitchen, etc.)
- Date listed/leased
- Source
```

#### Comp Analysis Output
```
RENT COMP SUMMARY
Subject Property: [address]
Number of comps found: ___
Comp range: $____ - $____ /month
Average rent: $____ /month
Median rent: $____ /month
Rent per sqft range: $____ - $____
Recommended market rent: $____ /month [ESTIMATED]
Confidence level: High / Medium / Low
Reasoning: [explain any adjustments made]
```

**Confidence Level Guide:**
- **High:** 5+ close comps within 3 months, tight range (±10%)
- **Medium:** 3-4 comps or wider range or some are 3-6 months old
- **Low:** <3 comps, or stale data, or significant adjustments needed

### Sales Comps

For purchase price validation and ARV estimation.

#### Comp Selection Criteria
- **Distance:** Within 0.5 miles for urban, 1 mile for suburban, 3 miles for rural
- **Property type:** Same type and configuration
- **Size:** Within 15% of subject square footage
- **Condition:** For ARV, match target post-rehab condition
- **Recency:** Sold within last 6 months (prefer 3 months)
- **Transaction type:** Arm's-length only (exclude foreclosures, family transfers, auctions unless analyzing distressed market)

#### Comp Data Points
```
- Address
- Sale price
- Sale date
- Beds / Baths / Sqft
- Price per sqft
- Days on market
- Condition at sale
- Lot size
- Year built
- Financing type (if known)
- Source (MLS, county records)
```

#### Adjustments
When comps aren't perfect matches, apply adjustments:
```
ADJUSTMENT CATEGORIES
- Size: +/- $____ per sqft difference
- Bedrooms: +/- $5,000-15,000 per bedroom
- Bathrooms: +/- $3,000-10,000 per bathroom
- Garage: +/- $10,000-25,000
- Condition: +/- $5,000-50,000 depending on scope
- Lot size: +/- varies by market
- Location: +/- for school district, proximity to amenities
- Age: minor adjustment for similar era homes
```

Show adjustment math for each comp used.

#### Sales Comp Output
```
SALES COMP SUMMARY
Subject Property: [address]
Number of comps: ___
Unadjusted range: $____ - $____
Adjusted range: $____ - $____
Average adjusted value: $____
Estimated Market Value: $____ [ESTIMATED]
Confidence level: High / Medium / Low
```

### Submarket Scoring

Rate each submarket factor 1-10:

| Factor | Score | Weight | Data Source |
|--------|-------|--------|-------------|
| Rent growth trajectory | /10 | 20% | Historical rent data |
| Vacancy rate | /10 | 15% | Census, local data |
| Population growth | /10 | 15% | Census |
| Employment access | /10 | 15% | Commute times, job centers |
| School quality | /10 | 10% | GreatSchools, state ratings |
| Crime trends | /10 | 10% | Local PD, FBI UCR |
| Supply pipeline | /10 | 10% | Permit data |
| Walkability/transit | /10 | 5% | Walk Score |
| **Weighted Total** | **/100** | | |

Scores:
- 80-100: Strong submarket — supports premium rents and appreciation
- 65-79: Solid submarket — reliable cash flow market
- 50-64: Emerging/transitional — higher risk but potential upside
- Below 50: Proceed with caution — additional due diligence required

## Regulatory Environment

### Landlord-Friendliness Assessment

This significantly impacts investment returns and risk. Evaluate:

```
EVICTION PROCESS
- Average eviction timeline (days from notice to possession)
- Required notice periods by type (nonpayment, lease violation, no-cause)
- Court filing costs
- Right to cure requirements
- Judicial vs. non-judicial process

RENT CONTROL
- State-level rent control laws
- Local rent control or rent stabilization ordinances
- Allowable annual increases
- Exemptions (new construction, SFR, small multi)
- Vacancy decontrol (can reset to market on turnover?)

TENANT PROTECTIONS
- Just-cause eviction requirements
- Source-of-income discrimination laws (Section 8 acceptance required?)
- Relocation assistance requirements
- Security deposit limits and return timelines
- Lease renewal rights

PROPERTY TAX
- Current effective tax rate
- Assessment frequency and methodology
- Homestead vs. non-homestead rate differential
- Tax abatement or exemption programs
- Recent or proposed rate increases
- Transfer tax rate
```

### Landlord-Friendliness Score
Rate 1-10 on each dimension, compute weighted average:

| Dimension | Score | Impact |
|-----------|-------|--------|
| Eviction timeline | /10 | Direct cost and vacancy exposure |
| Rent control | /10 | Revenue ceiling risk |
| Tenant protections | /10 | Operational complexity |
| Property tax burden | /10 | Fixed cost impact on NOI |
| **Overall** | **/10** | |

- 8-10: Very landlord-friendly (TX, FL, IN, TN, etc.)
- 5-7: Moderate (IL, MN, CO, etc.)
- 1-4: Challenging regulatory environment (CA, NY, OR, etc.)

## Supply & Demand Analysis

```
DEMAND SIGNALS
- Population growth rate
- Net in-migration
- Household formation rate
- Rent growth exceeding inflation
- Low vacancy rates (<5%)
- Days on market decreasing
- Multiple applications per listing

SUPPLY SIGNALS
- Building permits (residential, multi-family)
- Units under construction
- Planned developments in pipeline
- Conversion activity (commercial to residential)
- Historical completions vs. absorption

EQUILIBRIUM ASSESSMENT
- Current supply/demand balance: Undersupplied / Balanced / Oversupplied
- Projected balance (2-3 year outlook)
- Risk of oversupply from pipeline
```

## Market Report Output

Save reports to `~/.rei-agent/market_data/reports/<market_name>/`

### Report Structure
```markdown
# Market Analysis: [City/Metro]
**Date:** [date]
**Prepared for:** [investor name from profile]
**Strategy fit:** [which strategies this market supports]

## Executive Summary
[2-3 paragraph overview with key findings and recommendation]

## Demographic Profile
[Census/ACS data with trends]

## Employment & Economy
[BLS data, top employers, diversification]

## Housing Market
[Prices, rents, inventory, trends]

## Regulatory Environment
[Landlord-friendliness assessment]

## Supply & Demand
[Pipeline, absorption, equilibrium]

## Submarket Highlights
[Top 3-5 submarkets for the investor's strategy]

## Risk Factors
[Top risks specific to this market]

## Recommendation
[Buy/Watch/Avoid with supporting rationale]

## Data Sources
[All sources cited with dates]
```

## Scripts

### `scripts/pull_census_data.py`
Fetches ACS data for a given geography. Requires Census API key in config.

### `scripts/rent_comp_analyzer.py`
Normalizes and analyzes rent comp data from multiple sources.

### `scripts/market_scorer.py`
Applies the submarket scoring matrix and generates the score breakdown.
