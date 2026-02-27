---
description: Manages a watchlist of properties to monitor for changes
argument-hint: "[add|remove|check]"
---

# /rei:watchlist

**Skills:** deal-analysis, market-research

**Workflow:**
- `add <address>`: Add property to watchlist with current asking price and key metrics
- `remove <address>`: Remove from watchlist
- `check` (default): Check all watchlist properties for changes (price reductions, status)

Data stored in `~/.rei-agent/deals/watchlist/`.

**Output:** Watchlist status report with changes highlighted.
