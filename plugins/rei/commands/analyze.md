---
description: Runs a full deal underwriting report on a property
argument-hint: <address_or_url>
---

# /rei:analyze

**Skills:** deal-analysis, market-research, financing

**Workflow:**
1. Parse address or listing URL
2. Pull property data (web search for listing details)
3. Pull rent comps (market-research skill)
4. Pull sales comps if needed (market-research skill)
5. Load investor profile for return targets
6. Load assumption profile (default: conservative)
7. Run full underwriting (deal-analysis skill)
8. Run sensitivity analysis (deal-analysis skill)
9. Score the deal (deal-analysis skill)
10. Save to `~/.rei-agent/deals/pipeline/<address>/`
11. Present executive summary with recommendation

**Output:** Full analysis report with executive summary, pro forma, sensitivity, and score.
