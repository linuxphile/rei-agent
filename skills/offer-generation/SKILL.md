---
name: offer-generation
description: Calculate maximum allowable offers (MAO), draft letters of intent (LOIs), model negotiation scenarios, and develop offer strategies for real estate investment deals. Use this skill whenever someone asks "what should I offer?", "what's my max offer?", wants to draft an LOI or offer letter, needs help with negotiation strategy, wants to model counter-offer scenarios, or is preparing to make an offer on an investment property. Also trigger for any question about offer price, negotiation tactics, or deal structuring from the buyer's perspective.
---

# Offer Generation Skill

This skill handles everything from calculating the right price to making the offer: MAO calculations, offer strategy, LOI drafting, and negotiation scenario modeling.

## Maximum Allowable Offer (MAO) Calculations

### Method 1: Cash Flow MAO
Work backward from the investor's minimum acceptable cash-on-cash return:

```
GIVEN:
  Target CoC return:          ____%  [from investor profile]
  Available cash to invest:    $______
  Monthly gross rent:          $______
  Operating expense ratio:     ____%  [from comps or estimate]
  Financing terms:             rate, term, LTV

CALCULATE:
  Annual gross rent:           $______ = Monthly × 12
  Annual NOI:                  $______ = Gross Rent × (1 - OpEx Ratio - Vacancy)
  Required annual cash flow:   $______ = Available Cash × Target CoC
  Max annual debt service:     $______ = NOI - Required Cash Flow
  Max loan amount:             $______ = [reverse amortization from max payment]
  Max purchase price:          $______ = Max Loan / (1 - Down Payment %)

CASH FLOW MAO:                $______
```

### Method 2: Cap Rate MAO
Based on target cap rate for the market:

```
GIVEN:
  Annual NOI:                  $______
  Target cap rate:             ____%  [market-appropriate]

CALCULATE:
  Cap Rate MAO = NOI / Target Cap Rate
  
EXAMPLE:
  NOI = $24,000, Target cap = 8%
  MAO = $24,000 / 0.08 = $300,000
```

### Method 3: BRRRR MAO (70% Rule Refined)
For BRRRR deals, work backward from the refinance:

```
GIVEN:
  After-Repair Value (ARV):    $______  [from sales comps]
  Rehab costs:                 $______  [from contractor estimates]
  Refi LTV:                    ____%   [typically 75%]
  Target cash left in deal:    $______  [ideally $0 or negative]
  Closing costs (buy + refi):  $______

CALCULATE:
  Refi loan amount:            $______ = ARV × Refi LTV
  Max all-in cost:             $______ = Refi Loan - Target Cash Left
  Max purchase price:          $______ = Max All-In - Rehab - Closing Costs
  
BRRRR MAO:                    $______

SANITY CHECK:
  All-in / ARV ratio:          _____% [should be ≤ 75-80%]
  Purchase / ARV ratio:        _____% [should be ≤ 60-70%]
```

### Method 4: GRM MAO
Quick screening based on Gross Rent Multiplier:

```
GIVEN:
  Annual gross rent:           $______
  Target GRM:                  ____  [market-appropriate, typically 8-14]

CALCULATE:
  GRM MAO = Annual Gross Rent × Target GRM

EXAMPLE:
  Annual rent = $36,000, Target GRM = 10
  MAO = $36,000 × 10 = $360,000
```

### MAO Summary Output
Always present multiple methods together:

```
MAO ANALYSIS — [Address]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Method              | MAO        | Based On
--------------------|-----------|---------------------------
Cash Flow (___% CoC)| $______   | Target return + financing
Cap Rate (___%)     | $______   | Market cap rate
BRRRR (70% rule)    | $______   | ARV - rehab - margin
GRM (___x)          | $______   | Market GRM
--------------------|-----------|---------------------------
RECOMMENDED MAO     | $______   | [Method most aligned with strategy]
Asking Price        | $______   |
Discount to asking  | ____%     |
```

Choose the recommended MAO based on the investor's strategy:
- Buy-and-hold → Cash Flow MAO
- Value-add → Cap Rate MAO (using stabilized NOI)
- BRRRR → BRRRR MAO
- Quick screen → GRM MAO

## Offer Strategy

### Market Intelligence
Before recommending an offer price, assess the negotiation landscape:

```
LISTING INTELLIGENCE
Days on market:          _____ days
Price reductions:        _____ (how many, how much, when)
Comparable DOM:          _____ days (market average for this type)
Market temperature:      Hot / Warm / Cool / Cold
Multiple offer situation: Yes / No / Unknown
Seller motivation:       High / Medium / Low / Unknown

MOTIVATION SIGNALS (check all that apply):
[ ] Extended DOM (>2× market average)
[ ] Multiple price reductions
[ ] Vacant property
[ ] Estate/probate sale
[ ] Divorce/legal proceedings
[ ] Out-of-state owner
[ ] Landlord burnout (self-managing, problem tenants)
[ ] Tax delinquency
[ ] Pre-foreclosure
[ ] Relocating seller
[ ] Failed previous sale
```

### Offer Strategy Recommendations

Based on market intelligence, recommend one of these approaches:

**Aggressive (Strong buyer's market, high seller motivation)**
```
Offer: MAO or below
Contingencies: Full (inspection, financing, appraisal)
Earnest money: Standard (1-2%)
Closing timeline: Standard (30-45 days)
Rationale: Market position is strong, no urgency to compete
```

**Competitive (Balanced market, moderate activity)**
```
Offer: MAO to MAO + 3%
Contingencies: Full but with tighter timelines
Earnest money: Above standard (2-3%)
Closing timeline: Slightly accelerated (25-30 days)
Rationale: Show seriousness while protecting downside
```

**Strong (Seller's market, multiple offers likely)**
```
Offer: MAO + 3-7%
Contingencies: Shortened inspection period, may waive appraisal gap
Earnest money: Elevated (3-5%)
Closing timeline: Accelerated (21-25 days)
Escalation clause: Consider up to $______ in $______ increments
Rationale: Need to stand out, but don't chase past investment criteria
⚠️ WARNING: Never exceed the price at which the deal stops making
    financial sense. If MAO + 7% doesn't win, this isn't your deal.
```

**Off-Market Direct**
```
Offer: Below market (typically 70-85% of market value)
Contingencies: Full
Earnest money: Moderate with flexible timeline
Closing timeline: Flexible (accommodate seller's needs)
Sweeteners: Flexibility on closing date, leaseback, simplicity of transaction
Rationale: No competition, but must provide value to seller beyond price
```

## Letter of Intent (LOI) Template

Generate LOIs customized to the deal. Save to `~/.rei-agent/deals/pipeline/<address>/loi.md`.

```markdown
# Letter of Intent

**Date:** [date]
**Property:** [full address, legal description if available]
**Buyer:** [investor name / entity name]
**Seller:** [seller name if known, or "Property Owner"]

---

Dear [Seller/Agent Name],

I am writing to express my interest in purchasing the above-referenced 
property. This Letter of Intent outlines the proposed terms for your 
consideration. This LOI is non-binding and is intended to serve as a 
basis for negotiation of a definitive Purchase Agreement.

## Proposed Terms

**Purchase Price:** $[amount] ([spelled out] dollars)

**Earnest Money Deposit:** $[amount], to be deposited within [3-5] 
business days of mutual execution of the Purchase Agreement, held by 
[escrow agent/title company].

**Due Diligence Period:** [14-21] days from the effective date of the 
Purchase Agreement. During this period, Buyer may conduct inspections, 
review documents, and evaluate the property at Buyer's discretion. 
Buyer may terminate for any reason during this period and receive a 
full refund of the earnest money deposit.

**Financing Contingency:** This offer is contingent upon Buyer obtaining 
satisfactory financing within [21-30] days of the effective date. 
[OR: This is a cash offer with no financing contingency, subject to 
proof of funds provided within [X] business days.]

**Closing Date:** On or before [date], approximately [30-45] days from 
the effective date of the Purchase Agreement.

**Title:** Seller shall convey marketable title via [Warranty/Special 
Warranty] Deed, free and clear of all liens and encumbrances except 
[standard permitted exceptions].

**Closing Costs:** [Standard allocation: Seller pays transfer tax and 
title insurance; Buyer pays lender's title policy and loan costs. / 
Custom allocation as negotiated.]

**Property Condition:** Property to be delivered in substantially the 
same condition as of the date of the Purchase Agreement, normal wear 
and tear excepted.

**Seller Deliverables:** Within [5-7] business days of the effective 
date, Seller shall provide:
- Current rent roll and copies of all leases
- Operating statements for the prior [2-3] years
- Property tax bills for the prior [2-3] years  
- Utility bills for the prior 12 months
- List of all personal property included in sale
- Any known material defects or disclosures
- Insurance loss history
- Service contracts and vendor agreements

[OPTIONAL SECTIONS AS NEEDED:]

**Seller Financing:** [If applicable: Seller agrees to carry a 
[first/second] mortgage in the amount of $[amount] at [rate]% 
interest, amortized over [term] years with a [balloon] year balloon, 
payments of approximately $[amount]/month.]

**Leaseback:** [If applicable: Seller may lease back the property 
for [period] at $[rent]/month following closing.]

**Tenant Estoppels:** Seller shall provide signed tenant estoppel 
certificates from all tenants within [10] days of the effective date.

**Assignment:** Buyer reserves the right to assign this agreement to 
an entity controlled by Buyer prior to closing.

---

This Letter of Intent is non-binding and is subject to the negotiation 
and execution of a mutually acceptable Purchase Agreement. Either party 
may withdraw from negotiations at any time prior to execution of a 
definitive agreement.

This LOI shall remain open for acceptance until [date, typically 3-7 
days from LOI date].

Respectfully submitted,

[Buyer Name]
[Buyer Entity, if applicable]
[Contact information]
[Phone / Email]
```

## Negotiation Scenario Modeling

### Counter-Offer Impact Analysis
When the seller counters, immediately model the impact:

```
COUNTER-OFFER ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                    | Your Offer  | Counter     | Delta
--------------------|-----------|-------------|--------
Purchase price      | $______   | $______     | +$______
Earnest money       | $______   | $______     | +$______
DD period           | ___ days  | ___ days    | -___ days
Closing timeline    | ___ days  | ___ days    | -___ days
Seller concessions  | $______   | $______     | -$______

FINANCIAL IMPACT OF ACCEPTING COUNTER:
  Down payment change:      +$______
  Monthly payment change:   +$______
  Cash flow change:         -$______/month
  CoC return:               ____% → ____%  (Δ -____%)
  Break-even vacancy:       ____% → ____%
  IRR (projected):          ____% → ____%
  Deal score change:        ____ → ____ (Δ ____)

RECOMMENDATION:
  [ ] Accept — still meets investment criteria
  [ ] Counter at $______ — split the difference on key terms
  [ ] Walk — deal no longer pencils at these numbers
  
SUGGESTED COUNTER: $______ (rationale: ____________)
```

### Negotiation Playbook
Model 2-3 rounds of negotiation with likely outcomes:

```
SCENARIO TREE

Round 1: Your offer $250,000
├─ Seller accepts → Close at $250,000 (CoC: 10.2%)
├─ Seller counters $275,000
│  ├─ You counter $260,000
│  │  ├─ Seller accepts → Close at $260,000 (CoC: 8.8%)
│  │  ├─ Seller counters $268,000
│  │  │  ├─ Accept → Close at $268,000 (CoC: 7.9%) ⚠️ Below target
│  │  │  └─ Walk → Move to next deal
│  │  └─ Seller walks → Move to next deal
│  ├─ You accept $275,000 → Close at $275,000 (CoC: 7.1%) 🔴 Below min
│  └─ You walk → Move to next deal
└─ Seller walks → Move to next deal

WALK-AWAY PRICE: $______ (the price above which deal doesn't work)
```

### Negotiation Leverage Factors
Assess and communicate your leverage:

```
BUYER LEVERAGE                    | SELLER LEVERAGE
+ Cash / strong financing         | + Multiple interested buyers
+ Quick close capability          | + No urgency to sell
+ No contingency chains           | + Unique property / limited supply
+ Flexible on closing date        | + Recent price increase
+ Property has been listed long   | + Below-market rents (upside)
+ Needed repairs identified       | + Strong rental market
+ Comparable sales support price  | + Fully occupied / stabilized
+ Market is cooling               | + Market is heating up
```

## Scripts

### `scripts/mao_calculator.py`
Calculates MAO using all four methods from a deal parameters file.

### `scripts/loi_generator.py`
Generates customized LOI from template and deal-specific parameters.

### `scripts/counter_analyzer.py`
Models the financial impact of counter-offers on key return metrics.

### `scripts/negotiation_tree.py`
Generates negotiation scenario trees with financial outcomes at each node.
