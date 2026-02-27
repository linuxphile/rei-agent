---
name: due-diligence
description: Generate and manage due diligence checklists, inspection workflows, document tracking, red flag detection, and contractor bid comparison for real estate investment transactions. Use this skill whenever someone is under contract, preparing for an inspection, needs a DD checklist, wants to track documents for a closing, asks about red flags in a property, needs to compare contractor bids, or is managing the timeline between offer acceptance and closing. Trigger for "what should I look for in an inspection?", "create a due diligence checklist", "compare these bids", or any closing-related workflow management.
---

# Due Diligence Skill

This skill manages everything between offer acceptance and closing: inspection planning, document tracking, red flag identification, contractor bid analysis, and timeline management.

## Due Diligence Master Checklist

Generate this checklist customized to the property type, age, and deal structure. Save to `~/.rei-agent/deals/pipeline/<address>/dd_checklist.md`.

### Document Collection

Track status of each document: `[ ]` Not started, `[~]` Requested, `[✓]` Received, `[!]` Issue found

```
TITLE & LEGAL
[ ] Preliminary title report / title commitment
[ ] Title search (verify clear title, no liens)
[ ] Survey (current or recent)
[ ] Legal description verification
[ ] Deed review (warranty deed preferred)
[ ] HOA documents and financials (if applicable)
[ ] CC&Rs and bylaws (if applicable)
[ ] Zoning verification (current use is conforming?)
[ ] Certificate of occupancy
[ ] Building permits (all work permitted and closed?)
[ ] Code violations search
[ ] Pending litigation search
[ ] Easements and encroachments review

FINANCIAL
[ ] Current rent roll (all units)
[ ] Lease copies (all active leases)
[ ] Lease expiration schedule
[ ] Security deposit ledger
[ ] Tenant payment history (12 months)
[ ] Operating statements (2-3 years)
[ ] Property tax bills (2-3 years)
[ ] Insurance declarations page (current)
[ ] Utility bills (12 months, all meters)
[ ] Service contracts (lawn, snow, pest, etc.)
[ ] Capital improvement records
[ ] Pending or recent assessments

PHYSICAL
[ ] General home inspection report
[ ] Roof inspection (age, condition, remaining life)
[ ] HVAC inspection (each system)
[ ] Plumbing inspection (especially older homes)
[ ] Electrical inspection (panel capacity, wiring type)
[ ] Foundation/structural assessment
[ ] Radon test
[ ] Lead paint inspection (pre-1978 properties)
[ ] Asbestos assessment (pre-1980 properties)
[ ] Mold inspection (if indicators present)
[ ] Termite/pest inspection
[ ] Sewer scope (camera inspection of sewer line)
[ ] Well and septic inspection (if applicable)
[ ] Environmental Phase I (commercial or brownfield risk)
[ ] Flood zone verification (FEMA map check)
[ ] Smoke/CO detector compliance

INSURANCE
[ ] Insurance quote obtained
[ ] Flood insurance quote (if in flood zone)
[ ] Landlord/rental dwelling policy (not homeowner's)
[ ] Umbrella policy consideration
[ ] Loss history report (CLUE report)
```

### Customization Rules

**By Property Age:**
- Pre-1950: Add knob-and-tube wiring check, galvanized pipe assessment, foundation settlement evaluation, chimney inspection
- 1950-1978: Add lead paint inspection (federal requirement for disclosure), asbestos check, original electrical panel evaluation
- 1978-2000: Standard checklist
- Post-2000: Reduce structural concerns, focus on builder warranty transfer, check for common era-specific issues (polybutylene pipe, certain HVAC brands)

**By Property Type:**
- Multi-family (2-4 units): Add individual utility meter verification, common area assessment, separate entrance evaluation, fire escape/egress compliance
- Multi-family (5+ units): Add commercial inspection standards, fire suppression systems, elevator inspection, ADA compliance, environmental assessment
- Condos: Add HOA financial health review, reserve study, special assessment history, owner-occupancy ratio, rental restrictions

**By Deal Type:**
- BRRRR: Emphasize structural integrity, code compliance for rehab, utility capacity for planned upgrades
- Turnkey: Emphasize deferred maintenance, CapEx timeline, tenant quality
- Value-add: Emphasize rent comp validation, renovation feasibility, permit requirements

## Red Flag Detection

### Structural Red Flags 🔴
These can be deal-killers or require significant price reduction:

```
FOUNDATION
🔴 Horizontal cracks in block foundation (hydrostatic pressure)
🔴 Stair-step cracks wider than 1/4"
🔴 Bowing basement walls
🔴 Active water intrusion in basement
🔴 Significant settlement (uneven floors, door frames out of square)
⚠️ Minor settling cracks (< 1/4", vertical) — monitor

ROOF
🔴 Active leaks or water stains on upper floor ceilings
🔴 Multiple layers of shingles (max 2 in most codes)
🔴 Sagging roof deck
🔴 Roof age >25 years (asphalt shingle)
⚠️ Minor wear, 15-20 year old roof — budget for replacement

SYSTEMS
🔴 Federal Pacific or Zinsco electrical panels (fire hazard)
🔴 Aluminum wiring without proper remediation
🔴 Knob-and-tube wiring still active (insurance issue)
🔴 Polybutylene plumbing (failure-prone, insurance issue)
🔴 Cast iron sewer line with significant deterioration
🔴 Galvanized supply pipes with low flow
🔴 HVAC at end of life with no replacement budget
⚠️ Aging systems with 3-5 years remaining — budget in CapEx
```

### Financial Red Flags 🔴
```
🔴 Rents significantly above market (artificial income inflation)
🔴 Vacancy rate well below market (too good to be true?)
🔴 Expenses suspiciously low vs. comparable properties
🔴 Deferred maintenance visible but not reflected in financials
🔴 Tenant concentrations (one tenant = >50% of income in small multi)
🔴 Month-to-month leases on all units (turnover risk)
🔴 Below-market leases with long remaining terms (locked-in losses)
🔴 No security deposits held (or improperly held)
🔴 Property tax assessment significantly below market value (reassessment risk)
⚠️ Operating statements inconsistent year-over-year
⚠️ Seller unwilling to provide documentation
```

### Legal Red Flags 🔴
```
🔴 Title defects (liens, judgments, clouded title)
🔴 Unpermitted work (additions, conversions, major renovations)
🔴 Zoning nonconformity (legal nonconforming vs. illegal use)
🔴 Encroachments on or by neighboring properties
🔴 Active code violations
🔴 Environmental contamination (Phase I flags)
🔴 Pending or threatened litigation involving property
🔴 HOA in litigation or financial distress
🔴 Deed restrictions that limit intended use
⚠️ Easements that affect property use or future development
⚠️ Shared driveways, walls, or utilities with neighbors
```

### Red Flag Response Protocol
When a red flag is identified:
1. **Document it** — Add to DD tracker with severity level
2. **Quantify impact** — Estimate cost to remediate or ongoing cost impact
3. **Model scenarios** — Re-run deal analysis with remediation costs included
4. **Determine negotiation position** — Price reduction, seller repair, credit at closing, or walk away
5. **Consult professionals** — Flag items requiring specialist evaluation (structural engineer, environmental, attorney)

## Contractor Bid Comparison

When comparing bids for rehab or repairs:

### Bid Normalization Template
```
| Line Item           | Contractor A | Contractor B | Contractor C | Notes        |
|---------------------|-------------|-------------|-------------|-------------|
| Kitchen demo         | $______     | $______     | $______     |             |
| Kitchen cabinets     | $______     | $______     | $______     | Materials?  |
| Kitchen countertops  | $______     | $______     | $______     | Material?   |
| Kitchen plumbing     | $______     | $______     | $______     |             |
| Kitchen electrical   | $______     | $______     | $______     |             |
| Kitchen flooring     | $______     | $______     | $______     | Material?   |
| Kitchen appliances   | Included?   | Included?   | Included?   |             |
| ...                  |             |             |             |             |
| Subtotal             | $______     | $______     | $______     |             |
| Contingency (15%)    | $______     | $______     | $______     |             |
| TOTAL                | $______     | $______     | $______     |             |
```

### Bid Evaluation Criteria
Score each contractor 1-5:

| Criterion | Weight | Contractor A | Contractor B | Contractor C |
|-----------|--------|-------------|-------------|-------------|
| Price competitiveness | 25% | /5 | /5 | /5 |
| Scope completeness | 20% | /5 | /5 | /5 |
| Timeline | 15% | /5 | /5 | /5 |
| References/reputation | 15% | /5 | /5 | /5 |
| License/insurance | 10% | /5 | /5 | /5 |
| Payment terms | 10% | /5 | /5 | /5 |
| Warranty | 5% | /5 | /5 | /5 |
| **Weighted Score** | | **/5.0** | **/5.0** | **/5.0** |

### Key Bid Questions
Flag if any bid is missing answers to:
- Are permits included in the bid?
- What is the payment schedule (never >50% upfront)?
- What is the warranty period?
- Who supplies materials?
- What's the daily crew size?
- Are dumpster and cleanup included?
- What happens with change orders?
- Is there a penalty for timeline overrun?

## Timeline Management

### Standard DD Timeline (Residential 1-4 units)
```
DAY 0:   Offer accepted — DD period begins
DAY 1-3: Order inspections, title search, survey
         Request seller documents (leases, financials, utilities)
DAY 3-7: General inspection
DAY 5-10: Specialized inspections (sewer scope, radon, etc.)
DAY 7-14: Review all inspection reports
          Get repair estimates if needed
          Review title commitment
DAY 10-15: Negotiate repairs / credits based on findings
DAY 14-17: DD contingency decision point
           ✅ Proceed (waive DD contingency)
           ❌ Terminate (get earnest money back)
           🔄 Negotiate (request extension if needed)
DAY 15-25: Finalize financing (appraisal, underwriting)
DAY 20-28: Final walkthrough
DAY 28-30: CLOSING
```

### Critical Deadlines Tracker
```
| Deadline              | Date        | Status     | Action Needed        |
|-----------------------|-------------|-----------|---------------------|
| DD contingency        | [date]      | ⏳ Active  | All inspections done? |
| Financing contingency | [date]      | ⏳ Active  | Appraisal ordered?   |
| Appraisal due         | [date]      | [ ] Pending|                     |
| Title clearance       | [date]      | [ ] Pending|                     |
| Final walkthrough     | [date]      | [ ] Pending| Schedule 24hr before |
| Closing               | [date]      | [ ] Pending|                     |
```

### Earnest Money Protection
Remind the investor:
- Earnest money is at risk after contingencies expire
- Document ALL communications about contingency deadlines in writing
- If extending DD period, get written amendment signed by all parties
- If terminating, send notice BEFORE deadline (not on the deadline day)
- Keep copies of all notices with timestamps

## Post-Inspection Negotiation

### Repair Request Strategy
After inspections, categorize findings:

```
CATEGORY A: Safety & Structural — Request seller repair or equivalent credit
  These items affect habitability, safety, or insurability
  Example: electrical hazard, active leaks, foundation issues

CATEGORY B: Major Systems — Request credit at closing
  Items with significant cost that affect property value
  Example: aging roof, HVAC replacement needed, plumbing issues
  Strategy: get actual quotes, request 80-100% of repair cost as credit

CATEGORY C: Maintenance & Cosmetic — Accept as-is (budget in underwriting)
  Normal wear items you planned to handle anyway
  Example: old carpet, dated fixtures, minor drywall repairs
  Strategy: don't nickel-and-dime — weakens your position on important asks

CATEGORY D: Deal-Breakers — Renegotiate price or walk
  Issues that fundamentally change the deal economics
  Example: foundation failure, environmental contamination, title defects
  Strategy: significant price reduction reflecting true cost, or terminate
```

### Negotiation Request Template
```
Based on the inspection findings dated [date], we are requesting the 
following prior to closing:

SELLER REPAIRS (to be completed by licensed contractors with permits):
1. [Item] — Estimated cost: $______
2. [Item] — Estimated cost: $______

CLOSING CREDIT in lieu of repairs:
1. [Item] — Credit amount: $______
2. [Item] — Credit amount: $______

TOTAL REQUEST: $______

This request is based on [inspector name]'s report and contractor 
estimates from [contractor names]. Copies are available upon request.
```

## Output Structure

Save all DD materials to `~/.rei-agent/deals/pipeline/<address>/due_diligence/`:
```
due_diligence/
├── checklist.md           # Master DD checklist with status
├── red_flags.md           # Identified red flags and responses
├── timeline.md            # Critical deadlines and milestones
├── inspection_summary.md  # Consolidated inspection findings
├── bid_comparison.md      # Contractor bid analysis
├── repair_request.md      # Negotiation request document
└── documents/             # Directory for received documents
```
