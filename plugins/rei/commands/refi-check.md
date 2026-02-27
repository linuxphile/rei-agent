---
description: Analyzes refinance opportunities for a property or the full portfolio
argument-hint: "[address|portfolio]"
---

# /rei:refi-check

**Skills:** financing, portfolio-tracker

**Workflow:**
- If address: Run refinance analysis on specific property
- If "portfolio" or no argument: Scan all properties for refi opportunities
1. Calculate current equity position
2. Model refinance at current market rates
3. Calculate break-even period
4. Calculate ROE improvement
5. Recommend refi / hold / 1031 for each candidate

**Output:** Refinance opportunity analysis with recommendations.
