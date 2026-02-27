---
description: Screens deals against investment criteria and ranks matches
argument-hint: <criteria>
---

# /rei:screen

**Skills:** deal-analysis

**Workflow:**
1. Parse screening criteria (e.g., "2-4 units, Minneapolis, under 400k, 8%+ CoC")
2. Apply quick screening rules (1% rule, 50% rule)
3. Score each deal that passes screening
4. Rank by deal score
5. Present top candidates with summary metrics

**Input criteria examples:**
- Property type: SFR, duplex, triplex, quad, small multi
- Location: city, zip, state
- Price range: min-max
- Return targets: min CoC, min cap rate
- Unit count: min-max
- Strategy: buy-and-hold, BRRRR, house-hack, flip

**Output:** Ranked list of deals that pass screening criteria.
