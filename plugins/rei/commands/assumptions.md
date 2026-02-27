---
description: Views, sets, or creates named assumption profiles for underwriting
argument-hint: "[view|set|create]"
---

# /rei:assumptions

**Workflow:**
- `view`: Display all named assumption profiles
- `set <name>`: Set active assumption profile for future analyses
- `create <name>`: Interactive flow to create new assumption profile

Assumption profiles are stored in `~/.rei-agent/config/assumptions.json`.

**Default profiles:**
```json
{
  "conservative": {
    "vacancy_rate": 0.10,
    "credit_loss": 0.02,
    "maintenance_pct": 0.08,
    "capex_pct": 0.08,
    "mgmt_pct": 0.10,
    "rent_growth": 0.02,
    "expense_growth": 0.03,
    "appreciation": 0.02,
    "selling_costs_pct": 0.08
  },
  "moderate": {
    "vacancy_rate": 0.07,
    "credit_loss": 0.01,
    "maintenance_pct": 0.06,
    "capex_pct": 0.06,
    "mgmt_pct": 0.08,
    "rent_growth": 0.03,
    "expense_growth": 0.025,
    "appreciation": 0.03,
    "selling_costs_pct": 0.07
  },
  "aggressive": {
    "vacancy_rate": 0.05,
    "credit_loss": 0.01,
    "maintenance_pct": 0.05,
    "capex_pct": 0.05,
    "mgmt_pct": 0.08,
    "rent_growth": 0.04,
    "expense_growth": 0.02,
    "appreciation": 0.04,
    "selling_costs_pct": 0.06
  }
}
```
