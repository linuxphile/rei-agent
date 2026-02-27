# REI Agent — Real Estate Investment Analysis Agent

A Claude Code plugin for sourcing, analyzing, underwriting, and managing residential and small commercial real estate investments.

## Installation

```bash
claude plugin add linuxphile/rei-agent
```

## First-Time Setup

After installing, run the setup script to initialize data directories and your investor profile:

```bash
python scripts/setup.py --interactive
```

This creates `~/.rei-agent/` with default configuration, assumption profiles, and data directories. You can also edit your investor profile directly at `~/.rei-agent/config/investor_profile.json`.

## Quick Start

```bash
# Analyze a deal
/rei:analyze 123 Main St, Minneapolis, MN 55408

# Research a market
/rei:market Minneapolis

# View your portfolio
/rei:portfolio summary
```

## Architecture

```
rei-agent/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── CLAUDE.md                    # Agent profile and behavior instructions
├── README.md                    # This file
├── skills/                      # Modular skill definitions
│   ├── deal-analysis/           # Property underwriting and returns
│   │   └── SKILL.md
│   ├── market-research/         # Market and submarket analysis
│   │   └── SKILL.md
│   ├── financing/               # Loan modeling and comparison
│   │   └── SKILL.md
│   ├── portfolio-tracker/       # Portfolio management and reporting
│   │   └── SKILL.md
│   ├── due-diligence/           # DD checklists and inspection management
│   │   └── SKILL.md
│   └── offer-generation/        # MAO, LOI, and negotiation modeling
│       └── SKILL.md
├── commands/                    # Individual slash command definitions
│   ├── analyze.md
│   ├── compare.md
│   ├── screen.md
│   ├── market.md
│   ├── cashflow.md
│   ├── brrrr.md
│   ├── sensitivity.md
│   ├── offer.md
│   ├── due-diligence.md
│   ├── refi-check.md
│   ├── portfolio.md
│   ├── tax-prep.md
│   ├── watchlist.md
│   ├── assumptions.md
│   └── profile.md
├── scripts/                     # Python calculation engines
│   ├── setup.py                 # First-run initialization
│   └── calculate_returns.py     # Core financial calculations
├── config/                      # Default configuration files
│   ├── investor_profile.json    # Investor goals and constraints
│   └── assumptions.json         # Named assumption profiles
└── templates/                   # Output templates and samples
    └── sample_deal_params.json  # Example deal parameter file
```

## Skills

| Skill | Purpose | Key Outputs |
|-------|---------|-------------|
| **Deal Analysis** | Underwrite any property — cash flow, returns, sensitivity, scoring | Pro forma, sensitivity matrix, deal score |
| **Market Research** | Evaluate markets — demographics, comps, employment, regulatory | Market report, rent/sales comps, submarket scores |
| **Financing** | Model loan structures — conventional, DSCR, creative | Loan comparison, amortization, refi analysis |
| **Portfolio Tracker** | Track performance — equity, cash flow, tax prep | Dashboard, performance vs. pro forma, tax worksheets |
| **Due Diligence** | Manage closing process — inspections, documents, timelines | DD checklist, red flag report, bid comparison |
| **Offer Generation** | Make smart offers — MAO, LOI, negotiation modeling | MAO analysis, draft LOI, negotiation scenarios |

## Commands

| Command | Description |
|---------|-------------|
| `/rei:analyze <address>` | Full deal underwriting |
| `/rei:compare <addr1> <addr2>` | Side-by-side comparison |
| `/rei:screen <criteria>` | Screen deals against criteria |
| `/rei:market <city>` | Market research report |
| `/rei:cashflow <address>` | Cash flow projection |
| `/rei:brrrr <address>` | BRRRR strategy analysis |
| `/rei:sensitivity <address>` | Sensitivity analysis |
| `/rei:offer <address>` | MAO + LOI generation |
| `/rei:due-diligence <address>` | DD checklist + timeline |
| `/rei:refi-check` | Refinance opportunity scan |
| `/rei:portfolio` | Portfolio dashboard |
| `/rei:tax-prep <year>` | Tax preparation worksheet |
| `/rei:watchlist` | Deal watchlist management |
| `/rei:assumptions` | View/set assumption profiles |
| `/rei:profile` | Investor profile management |

## Data Storage

All persistent data is stored in `~/.rei-agent/`:

- **config/** — Investor profile, assumptions, API keys
- **portfolio/** — Property ledger, monthly actuals, transactions
- **deals/** — Pipeline (active), archive (closed/passed), watchlist
- **market_data/** — Cached data and generated reports

## Assumption Profiles

Five built-in profiles control underwriting assumptions:

- **Conservative** (default) — 10% vacancy, 8% maintenance, 8% CapEx, 2% rent growth
- **Moderate** — 7% vacancy, 6% maintenance, 6% CapEx, 3% rent growth
- **Aggressive** — 5% vacancy, 5% maintenance, 5% CapEx, 4% rent growth
- **House Hack** — No management fee, 5% vacancy, owner-occupied adjustments
- **BRRRR** — Post-rehab assumptions with 15% rehab contingency

Switch profiles: `/rei:assumptions set moderate`

## Key Principles

1. **Show the math** — Every recommendation includes the underlying calculations
2. **Conservative default** — Assumptions start conservative; investor can adjust up
3. **Certainty labeling** — All data points tagged as `[ACTUAL]`, `[ESTIMATED]`, or `[ASSUMED]`
4. **Investor-specific** — Analysis always contextualized against investor profile
5. **Deal journaling** — Every analysis saved for future reference and pattern recognition
6. **Professional review** — Always recommends attorney, CPA, and inspector review before closing

## Extending the Plugin

### Adding a New Skill
1. Create `skills/<skill-name>/SKILL.md` with YAML frontmatter (`name`, `description`)
2. Create any supporting scripts in `skills/<skill-name>/scripts/`

### Adding a New Command
1. Create `commands/<command-name>.md` with YAML frontmatter (`description`, `argument-hint`)
2. Map it to the appropriate skills and workflow in the command body

### Custom Assumption Profiles
Edit `~/.rei-agent/config/assumptions.json` to add profiles matching your market or strategy.

## Disclaimer

This agent provides analytical tools and calculations for real estate investment analysis. It is not a substitute for professional advice. Always consult with a licensed real estate attorney, CPA, property inspector, and financial advisor before making investment decisions. All projections are estimates based on assumptions and should not be considered guarantees of future performance.
