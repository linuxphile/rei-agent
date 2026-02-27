---
name: deal-analysis
description: Underwrite and analyze any residential or small commercial (1-50 unit) real estate investment deal. Use this skill whenever someone asks to analyze a property, run numbers on a deal, evaluate cash flow, calculate returns, do a BRRRR analysis, compare properties, run sensitivity analysis, or score a deal. Also trigger when someone provides a property address or listing URL and wants to know if it's a good investment. This is the primary analytical engine — use it aggressively for any property-level financial analysis.
---

# Deal Analysis Skill

This skill handles all property-level financial analysis: cash flow modeling, return calculations, deal scoring, BRRRR analysis, sensitivity testing, and multi-deal comparison.

## Quick Screening (Before Full Analysis)

Before running a full underwriting, apply these rapid screening heuristics to determine if a deal warrants deeper analysis:

### The 1% Rule
Monthly gross rent should be ≥ 1% of purchase price. This is a screening tool, not a decision tool.
- Example: $200,000 property should rent for ≥ $2,000/month
- Markets with high appreciation potential may justify < 1%
- Passes screening → proceed to full analysis
- Fails screening → flag and ask investor if they want full analysis anyway

### The 50% Rule
Estimate that ~50% of gross rent goes to operating expenses (excluding debt service). Use this for quick NOI estimation before you have itemized expenses.
- Gross Rent × 0.50 = Estimated NOI
- Then subtract debt service for estimated cash flow
- This is a sanity check, not a substitute for itemized underwriting

### The 70% Rule (Flips/BRRRR)
Maximum purchase price = (ARV × 70%) - Rehab Costs
- Example: ARV $300,000, Rehab $50,000 → Max offer = $160,000
- Adjust percentage based on market (65-75% range)

## Full Underwriting Model

### Required Inputs
Gather these before running analysis. Flag any that are missing or estimated:

```
PROPERTY DATA
- Address
- Property type (SFR, duplex, triplex, quad, small multi)
- Year built
- Square footage (total and per unit)
- Bedrooms/bathrooms (per unit)
- Lot size
- Current condition (1-10 scale or description)

FINANCIAL DATA
- Asking price or purchase price
- Current rents (per unit, actual or market)
- Property taxes (actual, current year)
- Insurance (actual or estimated)
- HOA/condo fees (if applicable)
- Utility costs (who pays what)
- Property management (% or flat fee)
- Current vacancy status
- Any existing leases (terms, expiration)

DEAL TERMS
- Financing structure (see Financing skill for details)
- Closing costs estimate
- Rehab budget (if applicable)
- Holding period assumption
```

### Core Calculations

Execute these calculations in order. Save intermediate results for the sensitivity analysis.

#### 1. Gross Potential Income (GPI)
```
GPI = Sum of all unit market rents × 12
    + Other income (laundry, parking, pet fees, storage)
```

#### 2. Effective Gross Income (EGI)
```
EGI = GPI - Vacancy Loss - Credit Loss
Vacancy Loss = GPI × vacancy_rate  [DEFAULT: 8%]
Credit Loss = GPI × credit_loss_rate  [DEFAULT: 2%]
```

#### 3. Operating Expenses (OpEx)
Itemize all expenses. Do NOT use percentage estimates when actuals are available.

```
FIXED EXPENSES
- Property taxes          [ACTUAL or estimate from county assessor]
- Insurance               [ACTUAL or estimate $1,200-2,400/yr for SFR]
- HOA/condo fees          [ACTUAL]

VARIABLE EXPENSES
- Repairs & maintenance   [DEFAULT: 5% of EGI for <20yr old, 8% for >20yr]
- CapEx reserves          [DEFAULT: 5% of EGI minimum, see CapEx table below]
- Property management     [DEFAULT: 8-10% of EGI for professional mgmt]
- Vacancy turnover costs  [DEFAULT: $500-1,500 per turn per unit per year]
- Advertising/leasing     [DEFAULT: 1 month rent per vacancy occurrence]
- Landscaping/snow        [ACTUAL or $100-300/month depending on property]
- Utilities (owner-paid)  [ACTUAL]
- Pest control            [DEFAULT: $50-100/month]
- Legal/accounting        [DEFAULT: $500-1,500/year]
- Miscellaneous           [DEFAULT: 2% of EGI]

TOTAL OpEx = Sum of all above
OpEx Ratio = Total OpEx / EGI  [HEALTHY: 35-50% for residential]
```

#### 4. Net Operating Income (NOI)
```
NOI = EGI - Total OpEx
```

#### 5. Debt Service
```
Annual Debt Service = Monthly Payment × 12
Monthly Payment = use standard amortization formula
  P × [r(1+r)^n] / [(1+r)^n - 1]
  where P = loan amount, r = monthly rate, n = total months
```

#### 6. Cash Flow
```
Annual Cash Flow = NOI - Annual Debt Service
Monthly Cash Flow = Annual Cash Flow / 12
Per Unit Cash Flow = Annual Cash Flow / number_of_units
Per Door Monthly = Monthly Cash Flow / number_of_units
```

#### 7. Return Metrics

**Cash-on-Cash Return (CoC)**
```
CoC = Annual Cash Flow / Total Cash Invested × 100
Total Cash Invested = Down Payment + Closing Costs + Rehab + Reserves
```
Target: varies by investor profile, typically 8-12% minimum.

**Cap Rate**
```
Cap Rate = NOI / Purchase Price × 100
```
Note: Cap rate ignores financing. Useful for comparing properties and market-level analysis.

**Gross Rent Multiplier (GRM)**
```
GRM = Purchase Price / Annual Gross Rent
```
Lower is better. Market-dependent; typically 8-15 for cash-flowing properties.

**Debt Service Coverage Ratio (DSCR)**
```
DSCR = NOI / Annual Debt Service
```
Minimum 1.25 for most lenders. Below 1.0 = negative cash flow.

**Return on Equity (ROE)**
```
ROE = Annual Cash Flow / Current Equity × 100
Current Equity = Property Value - Loan Balance
```
Important for refi decisions — if ROE drops below CoC threshold, consider harvesting equity.

**Internal Rate of Return (IRR)**
Calculate using full hold period cash flows:
```
Year 0: -Total Cash Invested
Year 1-N: Annual Cash Flow (with growth assumptions)
Year N: Cash Flow + Net Sale Proceeds
Net Sale Proceeds = Sale Price - Selling Costs - Remaining Loan Balance
```
Use iterative calculation or numpy IRR function.

**Equity Multiple**
```
Equity Multiple = Total Cash Received / Total Cash Invested
```

### CapEx Reserve Guide

Use this table for estimating remaining useful life and annual CapEx reserves:

| Component | Useful Life | Replacement Cost (SFR) | Annual Reserve |
|-----------|-------------|----------------------|----------------|
| Roof | 20-30 yrs | $8,000-15,000 | $400-500/yr |
| HVAC | 15-20 yrs | $5,000-10,000 | $333-500/yr |
| Water Heater | 10-15 yrs | $1,000-2,000 | $100-133/yr |
| Appliances | 10-15 yrs | $2,000-5,000 | $200-333/yr |
| Flooring | 7-15 yrs | $3,000-8,000 | $400-533/yr |
| Paint (ext) | 7-10 yrs | $3,000-6,000 | $428-600/yr |
| Plumbing | 20-30 yrs | $5,000-15,000 | $250-500/yr |
| Electrical | 25-40 yrs | $5,000-12,000 | $200-300/yr |
| Windows | 20-30 yrs | $5,000-15,000 | $250-500/yr |
| Driveway | 15-25 yrs | $3,000-8,000 | $200-320/yr |

Adjust based on property age, condition, and materials. For multi-unit, multiply per-unit items by unit count.

## BRRRR Analysis

When the strategy is Buy-Rehab-Rent-Refinance-Repeat, use this extended model:

### Phase 1: Acquisition
```
Purchase Price
+ Closing Costs (acquisition)
+ Holding Costs During Rehab (insurance, taxes, utilities, loan payments)
+ Rehab Budget (itemized preferred)
= Total Project Cost (All-In Cost)
```

### Phase 2: Rehab
```
Rehab Timeline: _____ months
Rehab Budget Breakdown:
  Kitchen:        $______
  Bathrooms:      $______
  Flooring:       $______
  Paint:          $______
  Exterior:       $______
  Systems:        $______
  Contingency (15-20%): $______
Total Rehab:      $______
```

### Phase 3: Rent
Run standard underwriting (above) using post-rehab market rents.

### Phase 4: Refinance
```
After-Repair Value (ARV):       $______  [from comps]
Refinance LTV:                  ____%    [typically 70-80%]
New Loan Amount:                $______  = ARV × LTV
Cash Out:                       $______  = New Loan - Original Loan Balance
Money Left In Deal:             $______  = Total Project Cost - Cash Out
```

### Phase 5: Final Returns
```
Cash-on-Cash (based on money left in deal):
  CoC = Annual Cash Flow / Money Left In Deal × 100

If Money Left In Deal ≤ 0:
  → "Infinite return" — all capital recovered plus surplus
  → Report surplus cash returned as a dollar amount

Velocity of Money:
  Time from acquisition to refinance completion: ____ months
  Annualized capital efficiency: Total Project Cost / months × 12
```

### BRRRR Feasibility Scorecard
Score each factor 1-5:

| Factor | Score | Notes |
|--------|-------|-------|
| Purchase below ARV | /5 | Need ≥20% discount |
| Rehab scope clarity | /5 | Cosmetic vs. structural |
| Rent comp confidence | /5 | Strong comps available? |
| ARV comp confidence | /5 | Recent sales support value? |
| Refinance feasibility | /5 | Lender will hit target LTV? |
| Cash recovery % | /5 | Will get ≥90% cash back? |
| **Total** | **/30** | ≥24 = strong candidate |

## Sensitivity Analysis

For every full underwriting, run sensitivity on these variables:

### Variables to Stress Test
1. **Purchase price**: ±5%, ±10%
2. **Rent**: ±5%, ±10%
3. **Vacancy rate**: base case, +3%, +5%, +10%
4. **Interest rate**: base case, +0.5%, +1.0%, +1.5%
5. **Expenses**: base case, +10%, +20%
6. **Appreciation**: 0%, 2%, 4% annually

### Output Format
Generate a sensitivity matrix showing CoC Return and Monthly Cash Flow for each variable combination:

```
| Variable      | Downside  | Base Case | Upside   |
|---------------|-----------|-----------|----------|
| Rent -10%     | CoC: X%   | CoC: Y%   | N/A      |
| Vacancy +5%   | CoC: X%   | CoC: Y%   | N/A      |
| Rate +1%      | CoC: X%   | CoC: Y%   | N/A      |
| All downside  | CoC: X%   | CoC: Y%   | CoC: Z%  |
```

Highlight any scenario where cash flow goes negative in **bold red** or with a ⚠️ marker.

### Break-Even Analysis
Calculate the break-even point for:
- Vacancy: what vacancy rate makes cash flow = $0?
- Rent: what rent reduction makes cash flow = $0?
- Rate: what interest rate makes cash flow = $0?

## Deal Scoring Matrix

Use this weighted scoring system for comparing deals:

| Category | Weight | Score Range | Criteria |
|----------|--------|-------------|----------|
| Cash Flow | 25% | 0-100 | Per-door monthly relative to market |
| Returns | 20% | 0-100 | CoC, IRR vs. investor minimums |
| Risk | 20% | 0-100 | DSCR, break-even vacancy, condition |
| Market | 15% | 0-100 | Population growth, rent growth, employment |
| Upside | 10% | 0-100 | Value-add potential, rent-to-market gap |
| Ease | 10% | 0-100 | Turnkey vs. heavy rehab, management needs |

**Total Score = Σ(Category Score × Weight)**

Scoring thresholds (adjust per investor profile):
- 80-100: Strong buy — meets or exceeds all criteria
- 65-79: Worth pursuing — meets most criteria with manageable risks
- 50-64: Marginal — needs specific favorable conditions
- Below 50: Pass — doesn't meet investment criteria

## Multi-Deal Comparison

When comparing 2+ deals, output a comparison table:

```
| Metric                  | Property A | Property B | Property C |
|-------------------------|-----------|-----------|-----------|
| Address                 |           |           |           |
| Price                   |           |           |           |
| Units                   |           |           |           |
| Monthly Gross Rent      |           |           |           |
| 1% Rule                 |           |           |           |
| NOI                     |           |           |           |
| Cap Rate                |           |           |           |
| CoC Return              |           |           |           |
| Monthly Cash Flow       |           |           |           |
| Per Door Cash Flow      |           |           |           |
| DSCR                    |           |           |           |
| Break-even Vacancy      |           |           |           |
| Deal Score              |           |           |           |
| Recommendation          |           |           |           |
```

Follow the comparison table with a narrative analysis explaining why one deal is preferred over others, specific to the investor's goals.

## Output File Structure

Save all analysis to: `~/.rei-agent/deals/pipeline/<sanitized_address>/`

```
<address>/
├── analysis.md           # Full underwriting report
├── pro_forma.xlsx        # Excel pro forma (if xlsx skill available)
├── sensitivity.md        # Sensitivity analysis results
├── assumptions.json      # All assumptions used
├── comps.md              # Comp data used (if available)
└── metadata.json         # Timestamp, data sources, certainty flags
```

## Scripts

### `scripts/calculate_returns.py`
Python script for all return calculations. Import and use for consistency:

```python
# Usage: python scripts/calculate_returns.py --input deal_params.json --output results.json
# Also importable: from scripts.calculate_returns import calculate_coc, calculate_irr, ...
```

Read `scripts/calculate_returns.py` for implementation details before running calculations.

### `scripts/sensitivity.py`
Generates sensitivity matrices. Accepts a base-case parameter file and stress-test ranges.

### `scripts/score_deal.py`
Applies the deal scoring matrix. Accepts analysis output and investor profile.
