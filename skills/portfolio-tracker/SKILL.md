---
name: portfolio-tracker
description: Track, report on, and optimize a real estate investment portfolio. Use this skill whenever someone asks about their portfolio performance, wants to add or update a property, needs equity position reporting, wants cash flow tracking vs. pro forma, needs tax preparation summaries, depreciation schedules, 1031 exchange planning, or portfolio-level risk analysis. Trigger for questions like "how is my portfolio doing?", "what's my total equity?", "which properties should I refi?", "am I concentrated in one market?", or any portfolio-level reporting and decision-making.
---

# Portfolio Tracker Skill

This skill manages portfolio-level data, reporting, and optimization: property ledger, performance tracking, equity management, tax preparation, and portfolio risk analysis.

## Data Model

### Property Record Schema

Each property in the portfolio is stored in `~/.rei-agent/portfolio/properties.json`:

```json
{
  "properties": [
    {
      "id": "prop_001",
      "address": "123 Main St, Minneapolis, MN 55401",
      "type": "duplex",
      "units": 2,
      "sqft": 2400,
      "year_built": 1965,
      "acquisition": {
        "purchase_date": "2023-06-15",
        "purchase_price": 285000,
        "closing_costs": 8550,
        "rehab_costs": 35000,
        "total_basis": 328550,
        "down_payment": 71250,
        "total_cash_invested": 114800
      },
      "financing": {
        "original_loan_amount": 213750,
        "current_balance": 208200,
        "rate": 6.75,
        "term_months": 360,
        "monthly_pi": 1386,
        "loan_type": "conventional",
        "maturity_date": "2053-06-15"
      },
      "current_value": {
        "estimated_value": 320000,
        "estimate_date": "2024-11-01",
        "estimate_source": "Zillow + local comps",
        "confidence": "medium"
      },
      "income": {
        "unit_1_rent": 1350,
        "unit_2_rent": 1250,
        "other_income": 50,
        "gross_monthly": 2650
      },
      "expenses": {
        "taxes_monthly": 350,
        "insurance_monthly": 165,
        "mgmt_monthly": 265,
        "maintenance_monthly": 132,
        "capex_reserve_monthly": 132,
        "vacancy_reserve_pct": 8,
        "utilities_monthly": 0,
        "other_monthly": 53
      },
      "status": "active",
      "strategy": "buy_and_hold",
      "market": "Minneapolis-St Paul",
      "notes": "Good duplex in Uptown area. Both units updated during rehab."
    }
  ]
}
```

### Monthly Actuals Schema

Track actual monthly performance in `~/.rei-agent/portfolio/monthly/`:

```json
{
  "property_id": "prop_001",
  "year": 2024,
  "months": {
    "01": {
      "gross_income": 2650,
      "vacancy_loss": 0,
      "effective_income": 2650,
      "expenses": {
        "taxes": 350,
        "insurance": 165,
        "management": 265,
        "repairs": 450,
        "capex": 0,
        "utilities": 0,
        "other": 0
      },
      "total_expenses": 1230,
      "noi": 1420,
      "debt_service": 1386,
      "cash_flow": 34,
      "notes": "Furnace repair in unit 2 - $450"
    }
  }
}
```

## Portfolio Dashboard

When asked for a portfolio summary, generate this report:

### Portfolio Overview
```
PORTFOLIO SNAPSHOT — [Date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total properties:          ___
Total units:               ___
Total portfolio value:     $______
Total debt:                $______
Total equity:              $______
Portfolio LTV:             ____%
Total monthly income:      $______
Total monthly expenses:    $______
Total monthly cash flow:   $______
Annualized cash flow:      $______
Portfolio CoC return:      ____%
Portfolio avg cap rate:     ____%
```

### Property-Level Summary Table
```
| Property | Units | Value    | Debt     | Equity   | Monthly CF | CoC   | DSCR |
|----------|-------|----------|----------|----------|-----------|-------|------|
| 123 Main | 2     | $320,000 | $208,200 | $111,800 | $34       | 3.6%  | 1.02 |
| ...      |       |          |          |          |           |       |      |
| TOTAL    | ___   | $______  | $______  | $______  | $______   | ____% |      |
```

### Performance vs. Pro Forma
Compare actual results to original underwriting:

```
| Metric              | Pro Forma  | Actual YTD | Variance | Flag |
|---------------------|-----------|-----------|----------|------|
| Gross Income        | $31,800   | $30,500   | -$1,300  | ⚠️   |
| Vacancy Rate        | 8%        | 11%       | +3%      | ⚠️   |
| Operating Expenses  | $13,200   | $14,800   | +$1,600  | ⚠️   |
| NOI                 | $18,600   | $15,700   | -$2,900  | 🔴   |
| Cash Flow           | $5,160    | $2,260    | -$2,900  | 🔴   |
| Cash-on-Cash        | 8.2%      | 3.6%      | -4.6%    | 🔴   |
```

Variance flags:
- ✅ Within ±5% of pro forma
- ⚠️ 5-15% variance — monitor
- 🔴 >15% variance — action needed

When flagging 🔴 items, provide specific diagnosis and recommended actions.

## Equity Management

### Equity Waterfall Report
```
EQUITY POSITION — [Date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                       Acquisition   Appreciation   Loan Paydown   Total Equity
Property A:            $71,250       $35,000        $5,550        $111,800
Property B:            $______       $______        $______       $______
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Portfolio Total:       $______       $______        $______       $______
```

### Return on Equity Analysis
For each property, calculate current ROE:
```
ROE = Annual Cash Flow / Current Equity × 100
```

Flag properties where ROE < investor's target CoC return. These are candidates for:
1. **Cash-out refinance** — harvest equity for reinvestment
2. **1031 exchange** — sell and reinvest in higher-performing asset
3. **Equity optimization** — accept lower ROE if property has other strategic value

### Refi Opportunity Scanner
Scan portfolio for refinance candidates. Flag properties where:
- Current LTV < 70% (significant equity available)
- ROE < target CoC (equity trapped in low-return position)
- Current rate > market rate by ≥0.75%
- Seasoning requirements met (typically 6-12 months for cash-out)

For each candidate, calculate:
```
Property: [address]
Current value:         $______
Current balance:       $______
Current LTV:           ____%
Available equity (75% LTV): $______
Current ROE:           ____%
If cash-out deployed at target CoC:
  Additional annual income: $______
  Portfolio CoC improvement: +_____%
Recommendation: [Refi / Hold / 1031]
```

## Tax Preparation

### Annual Tax Summary
Generate for each tax year:

```
TAX SUMMARY — [Year]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RENTAL INCOME (Schedule E)
| Property | Gross Rent | Other Income | Total Income |
|----------|-----------|-------------|-------------|
| 123 Main | $31,800   | $600        | $32,400     |
| TOTAL    | $______   | $______     | $______     |

RENTAL EXPENSES (Schedule E)
| Expense Category    | Prop A  | Prop B  | Total    |
|--------------------|---------|---------|---------| 
| Advertising         | $____   | $____   | $______  |
| Auto & travel       | $____   | $____   | $______  |
| Cleaning/maintenance| $____   | $____   | $______  |
| Commissions         | $____   | $____   | $______  |
| Insurance           | $____   | $____   | $______  |
| Legal & professional| $____   | $____   | $______  |
| Management fees     | $____   | $____   | $______  |
| Mortgage interest   | $____   | $____   | $______  |
| Repairs             | $____   | $____   | $______  |
| Supplies            | $____   | $____   | $______  |
| Taxes               | $____   | $____   | $______  |
| Utilities           | $____   | $____   | $______  |
| Other               | $____   | $____   | $______  |
| TOTAL EXPENSES      | $____   | $____   | $______  |
```

### Depreciation Schedule
```
DEPRECIATION — [Year]
Standard residential depreciation: 27.5 years straight-line

| Property | Depreciable Basis | Annual Depr. | Accum. Depr. | Remaining |
|----------|------------------|-------------|-------------|----------|
| 123 Main | $262,840          | $9,558      | $14,337     | $248,503 |
```

**Depreciable Basis Calculation:**
```
Purchase Price:              $______
+ Closing costs (allocable):  $______
+ Rehab/improvements:         $______
= Total Basis:                $______
- Land value (not depreciable): $______
= Depreciable Basis:          $______
Annual Depreciation:          Depreciable Basis / 27.5
```

Note: Land is typically 15-25% of total value. Use county assessor allocation or get a professional appraisal for cost segregation.

### Cost Segregation Flag
Flag properties where cost segregation study may be beneficial:
- Properties with >$500K basis
- Significant personal property (appliances, fixtures, landscaping)
- Properties acquired or substantially renovated in current tax year
- Investor in high tax bracket seeking accelerated depreciation

Always note: "Consult with a CPA experienced in real estate taxation. Cost segregation studies require professional engineering analysis."

### 1031 Exchange Tracker
If any properties are candidates for 1031 exchange:
```
1031 EXCHANGE PLANNING
Property: [address]
Current value:         $______
Original basis:        $______
Accumulated depr:      $______
Adjusted basis:        $______
Estimated gain:        $______
Estimated tax (if sold normally): $______

1031 REQUIREMENTS:
- 45-day identification period
- 180-day closing deadline
- Replacement property must be equal or greater value
- All equity must be reinvested to fully defer
- Qualified Intermediary required (DO NOT touch proceeds)

TARGET REPLACEMENT:    $______ minimum value
TIMELINE:             Start date → ID deadline → Close deadline
```

## Portfolio Risk Analysis

### Concentration Risk
```
GEOGRAPHIC CONCENTRATION
| Market          | Properties | Units | % of Value | Risk Level |
|-----------------|-----------|-------|-----------|------------|
| Minneapolis     | 3         | 8     | 65%       | ⚠️ HIGH    |
| Rochester       | 1         | 4     | 35%       | ✅ OK      |

RULE: Flag any market >40% of portfolio value
```

### Cash Flow Risk
```
CASH FLOW STRESS TEST
| Scenario              | Monthly CF | Annual CF | Status    |
|-----------------------|-----------|----------|-----------|
| Base case             | $2,400    | $28,800  | ✅ Positive |
| +5% vacancy all props | $1,800    | $21,600  | ✅ Positive |
| +10% vacancy          | $1,200    | $14,400  | ⚠️ Thin    |
| Lose worst tenant     | $900      | $10,800  | ⚠️ Thin    |
| Major repair ($15K)   | -$350     | $24,600  | ⚠️ Neg mo  |
| Rate reset (+2%)      | $800      | $9,600   | ⚠️ Thin    |
```

### Portfolio Health Score
```
| Dimension              | Score  | Weight | Notes               |
|-----------------------|--------|--------|---------------------|
| Cash flow coverage     | /100   | 25%    | DSCR across portfolio |
| Equity position        | /100   | 20%    | LTV and equity growth |
| Diversification        | /100   | 15%    | Geographic/type spread |
| Performance vs plan    | /100   | 15%    | Actuals vs. pro forma |
| Debt structure         | /100   | 15%    | Fixed vs. variable, terms |
| Liquidity/reserves     | /100   | 10%    | Cash reserves adequacy |
| PORTFOLIO HEALTH SCORE | /100   |        |                     |
```

## Property Lifecycle Management

### Adding a Property
When adding a new property to the portfolio:
1. Collect all acquisition data (see schema above)
2. Run initial underwriting (Deal Analysis skill)
3. Save pro forma assumptions for future performance comparison
4. Set up monthly tracking template
5. Calculate initial depreciation schedule
6. Update portfolio totals

### Updating Property Data
Periodically update:
- Rent amounts (on lease renewal)
- Property value estimate (annually at minimum)
- Loan balance (from amortization or statement)
- Expense actuals (monthly)
- Insurance and tax amounts (annually)

### Disposing a Property
When selling or exchanging:
1. Calculate taxable gain (sale price - adjusted basis)
2. Depreciation recapture calculation (25% rate)
3. Capital gains calculation (federal + state rates)
4. 1031 exchange feasibility analysis
5. Net proceeds after all costs and taxes
6. Move property to archive with full transaction record

## Scripts

### `scripts/portfolio_dashboard.py`
Generates the full portfolio dashboard from properties.json and monthly data.

### `scripts/equity_waterfall.py`
Calculates equity positions including appreciation estimates and loan paydown.

### `scripts/tax_prep.py`
Generates tax preparation worksheets with depreciation schedules.

### `scripts/refi_scanner.py`
Scans portfolio for refinance opportunities and models outcomes.

### `scripts/risk_analysis.py`
Runs concentration analysis and cash flow stress tests.
