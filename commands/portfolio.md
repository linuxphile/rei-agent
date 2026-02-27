---
description: Manages portfolio reporting, property tracking, and performance analysis
argument-hint: "[summary|add|update]"
---

# /rei:portfolio

**Skills:** portfolio-tracker

**Workflow:**
- `summary` (default): Generate full portfolio dashboard
- `add`: Interactive flow to add new property to portfolio
- `update`: Update existing property data (rents, value, expenses)

**Subcommands:**
- `/rei:portfolio summary` — Dashboard with all properties, equity, cash flow
- `/rei:portfolio add` — Step-by-step property data collection and entry
- `/rei:portfolio update <address> <field> <value>` — Update specific data point
- `/rei:portfolio performance` — Actuals vs. pro forma comparison
- `/rei:portfolio risk` — Concentration and stress test analysis

**Output:** Varies by subcommand.
