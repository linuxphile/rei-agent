---
name: financing
description: Model, compare, and optimize real estate financing structures. Use this skill whenever someone asks about loan types, mortgage calculations, interest rates, refinancing, DSCR loans, hard money, seller financing, creative financing, amortization schedules, or any debt-related analysis for real estate investment. Also trigger when the deal analysis skill needs financing inputs or when someone asks "how should I finance this deal?" or "should I refinance?" or wants to compare loan products side by side.
---

# Financing Skill

This skill models all aspects of real estate investment financing: loan product comparison, amortization, refinance timing, creative structures, and rate sensitivity analysis.

## Loan Product Reference

### Conventional Investment Loans
```
USE CASE: Standard rental properties, 1-4 units
TYPICAL TERMS:
  Down payment:     15-25% (SFR: 15-20%, 2-4 unit: 20-25%)
  Rate:             Market rate + 0.25-0.75% investor premium
  Term:             30yr fixed, 15yr fixed, 5/1 ARM, 7/1 ARM
  LTV:              75-85%
  DTI:              Max 43-50% (varies by lender)
  Credit:           Min 620, best rates at 740+
  Reserves:         6 months PITI per property
  Property limit:   Up to 10 financed properties (Fannie/Freddie)
PROS: Lowest rates, longest terms, predictable payments
CONS: DTI limits, property count limits, full documentation required
RENTAL INCOME CREDIT: 75% of market rent can offset DTI (if not occupying)
```

### DSCR Loans (Debt Service Coverage Ratio)
```
USE CASE: Investors who exceed DTI limits or want to qualify on property income
TYPICAL TERMS:
  Down payment:     20-25%
  Rate:             Market + 1-3% (higher than conventional)
  Term:             30yr fixed, 5/1 ARM, interest-only options
  LTV:              75-80%
  Min DSCR:         1.0-1.25 (varies by lender)
  Credit:           Min 660, best terms at 720+
  Reserves:         6-12 months PITI
  Property limit:   No limit
QUALIFICATION: Based on property cash flow, not personal income
  DSCR = NOI / Annual Debt Service
PROS: No personal income verification, no DTI limit, unlimited properties
CONS: Higher rates, larger down payment, requires strong property cash flow
```

### FHA Loans (Owner-Occupied House Hacking)
```
USE CASE: House hacking 2-4 unit properties (must owner-occupy)
TYPICAL TERMS:
  Down payment:     3.5% (credit 580+), 10% (credit 500-579)
  Rate:             Market rate (often best available)
  Term:             30yr or 15yr fixed
  LTV:              96.5%
  MIP:              1.75% upfront + 0.55-1.05% annual
  DTI:              Max 43-50%
  Credit:           Min 500 (580 for 3.5% down)
  Occupancy:        Must live in one unit for 12 months
RENTAL INCOME CREDIT: 75% of other units' rent can offset DTI
PROS: Very low down payment, competitive rates, lenient credit
CONS: Must owner-occupy, MIP for life (if <10% down), property standards
HOUSE HACK MATH:
  Gross rent from other units - vacancy - expenses = offset against PITI
  Net housing cost = your PITI - net rent from other units
```

### VA Loans (Veteran House Hacking)
```
USE CASE: Veterans house hacking 1-4 unit properties
TYPICAL TERMS:
  Down payment:     0%
  Rate:             Market rate (typically lowest available)
  Term:             30yr or 15yr fixed
  LTV:              100%
  Funding fee:      1.25-3.3% (can be financed, waived for disability)
  DTI:              Residual income method (more flexible)
  Credit:           No VA minimum, lenders typically want 620+
  Occupancy:        Must owner-occupy
PROS: No down payment, no PMI, best rates, flexible DTI
CONS: Must be veteran, must owner-occupy, funding fee
```

### Hard Money / Bridge Loans
```
USE CASE: Fix-and-flip, BRRRR acquisition/rehab phase, quick closes
TYPICAL TERMS:
  Down payment:     10-30% of purchase (based on ARV or purchase price)
  Rate:             9-14% (higher in tight credit markets)
  Points:           1-4 points origination
  Term:             6-18 months (interest-only)
  LTV:              60-75% of ARV, or 80-90% of purchase price
  Funding speed:    5-14 days
  Rehab draws:      Funded in draws based on completed work
QUALIFICATION: Based on deal quality and borrower experience
  Experience matters: first-time flippers pay more
PROS: Fast closing, flexible on property condition, based on deal not borrower
CONS: Very expensive, short term, extension fees, default risk
TOTAL COST CALCULATION:
  Interest: Loan Amount × Rate × (Months / 12)
  Points: Loan Amount × Point Percentage
  Fees: Origination, doc prep, inspection, extension
  Total Financing Cost = Interest + Points + Fees
  Monthly Cost = Total / Hold Period Months
```

### Seller Financing
```
USE CASE: Off-market deals, flexible terms, avoiding bank qualification
TYPICAL TERMS:
  Down payment:     5-20% (negotiable)
  Rate:             5-8% (negotiable, often below hard money)
  Term:             3-10 years with balloon (or full amortization if lucky)
  Amortization:     20-30 years (with balloon at term end)
  Due-on-sale:      Negotiable
PROS: Flexible terms, no bank qualification, faster closing, creative structures
CONS: Balloon risk, typically above-market rates, seller must agree
KEY NEGOTIATION LEVERS:
  - Price vs. terms tradeoff (pay full asking for better financing)
  - Interest rate vs. down payment
  - Balloon term length
  - Prepayment penalties (avoid if possible)
  - Subordination clause (can you refinance with new first lien?)
```

### Subject-To (Sub2) Financing
```
USE CASE: Taking over existing mortgage, keeping seller's rate
STRUCTURE: Buyer takes title, seller's loan stays in place
RISKS:
  - Due-on-sale clause (lender CAN call the loan)
  - Insurance and escrow complications
  - Seller's credit at risk if buyer defaults
  - Legal complexity varies by state
CONSIDERATIONS:
  - Most viable when seller's rate is below current market
  - Seller needs motivation (distress, relocation, etc.)
  - Title held via land trust or LLC for privacy
  - Always involve an attorney experienced in creative financing
NOTE: This is an advanced strategy. Flag risks prominently.
```

## Loan Comparison Model

When comparing financing options, build this table:

```
| Metric                    | Option A   | Option B   | Option C   |
|---------------------------|-----------|-----------|-----------|
| Loan type                 |           |           |           |
| Loan amount               |           |           |           |
| Interest rate              |           |           |           |
| Term / Amortization       |           |           |           |
| Monthly P&I               |           |           |           |
| Monthly total (PITI)      |           |           |           |
| Total cash to close       |           |           |           |
| Annual debt service       |           |           |           |
| DSCR                      |           |           |           |
| Cash flow (monthly)       |           |           |           |
| Cash-on-cash return       |           |           |           |
| Total interest paid (hold)|           |           |           |
| Total cost of financing   |           |           |           |
| Break-even vs. Option A   |           |           |           |
```

Always include a "Total Cost of Financing" that captures ALL costs: interest, points, fees, PMI/MIP, and closing costs.

## Amortization Schedule

Generate amortization schedules showing:

```
| Month | Payment | Principal | Interest | Balance  | Cum. Principal | Cum. Interest |
|-------|---------|-----------|----------|----------|---------------|--------------|
| 1     | $X      | $X        | $X       | $X       | $X            | $X           |
| ...   |         |           |          |          |               |              |
```

Highlight key milestones:
- When principal exceeds interest in monthly payment
- Equity position at years 1, 3, 5, 10, 15, 20, 25, 30
- Total interest paid at each milestone

## Refinance Analysis

### When to Evaluate a Refinance
Trigger a refinance analysis when:
- Rate environment has dropped ≥0.75% below current rate
- Property has appreciated significantly (equity harvest opportunity)
- Current loan has adjustable rate approaching reset
- BRRRR strategy calls for refinance after rehab
- Investor's Return on Equity has dropped below target CoC

### Refinance Calculation
```
CURRENT POSITION
  Current loan balance:     $______
  Current rate:             _____%
  Current monthly payment:  $______
  Current property value:   $______ [ESTIMATED - comps needed]
  Current equity:           $______ = Value - Balance
  Current LTV:              _____% = Balance / Value

NEW LOAN TERMS
  New loan amount:          $______ = Value × Target LTV
  New rate:                 _____%
  New monthly payment:      $______
  Cash out:                 $______ = New Loan - Current Balance - Costs
  Refinance costs:          $______ (typically 2-5% of new loan)

ANALYSIS
  Monthly payment change:   $______ (+/-)
  Annual cash flow change:  $______
  Break-even period:        ______ months = Refi Costs / Monthly Savings
  ROE before refi:          _____% = Cash Flow / Equity
  ROE after refi:           _____% = New Cash Flow / Remaining Equity
  Cash-out deployment:      If reinvested at ___% CoC = $___/year additional
```

### Refinance Decision Matrix
```
REFINANCE IF:
✅ Monthly savings pay back refi costs within hold period
✅ Cash-out can be deployed at returns > cost of new debt
✅ ROE is below target and equity is better used elsewhere
✅ Moving from ARM to fixed before rate adjustment
✅ BRRRR strategy: recovering capital for next deal

DO NOT REFINANCE IF:
❌ Break-even period exceeds planned remaining hold
❌ New rate isn't meaningfully better (< 0.5% improvement)
❌ Refi costs eat most of the savings
❌ Property value doesn't support desired LTV
❌ Prepayment penalty on existing loan exceeds benefit
```

## Rate Sensitivity Model

Show how interest rate changes impact the deal:

```
| Rate    | Monthly P&I | Annual DS  | Cash Flow  | CoC     | DSCR   |
|---------|-------------|-----------|-----------|---------|--------|
| 5.0%    | $______     | $______   | $______   | ____%   | ____   |
| 5.5%    | $______     | $______   | $______   | ____%   | ____   |
| 6.0%    | $______     | $______   | $______   | ____%   | ____   |
| 6.5%    | $______     | $______   | $______   | ____%   | ____   |
| 7.0%    | $______     | $______   | $______   | ____%   | ____   |
| 7.5%    | $______     | $______   | $______   | ____%   | ____   |
| 8.0%    | $______     | $______   | $______   | ____%   | ____   |
```

Highlight the rate at which DSCR drops below 1.25 and below 1.0.

## Creative Financing Strategies

### Strategy: Stack Financing
Combine multiple sources to minimize cash investment:
```
Example:
  Purchase price:     $200,000
  First lien (bank):  $150,000 (75% LTV)
  Seller second:      $30,000  (15%)
  Buyer cash:         $20,000  (10%)
  
  Blended rate: (150k × 6.5% + 30k × 7%) / 180k = 6.58%
  Total debt service: calculate both payments
```

### Strategy: Lease Option
```
Option fee:       $______ (typically 1-5% of price, credited at purchase)
Monthly rent:     $______ (portion may credit toward purchase)
Option period:    ______ months
Strike price:     $______ (locked at agreement, or formula-based)
USE CASE: Control property with minimal capital while building equity credit
RISK: Lose option fee if don't exercise
```

### Strategy: Wraparound Mortgage
```
Existing loan:    $______ at _____%
Wrap rate:        _____% (must be higher than underlying)
Wrap amount:      $______
Spread:           _____% arbitrage to wrap holder
USE CASE: Seller keeps existing financing, creates new note wrapping around it
RISK: Due-on-sale, complex documentation, state legality varies
```

## Scripts

### `scripts/amortization.py`
Generates full amortization schedules with milestone highlights.

### `scripts/loan_comparison.py`
Side-by-side loan product comparison with total cost analysis.

### `scripts/refi_analyzer.py`
Refinance break-even and ROE analysis.

### `scripts/rate_sensitivity.py`
Rate impact modeling across the full deal structure.
