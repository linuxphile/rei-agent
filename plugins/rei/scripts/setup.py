#!/usr/bin/env python3
"""
REI Agent — Setup & Initialization

Creates the required directory structure and initializes config files.
Run once before first use: python scripts/setup.py

Optionally run with --interactive to set up investor profile.
"""

import json
import os
import shutil
import argparse
from datetime import datetime
from pathlib import Path


REI_HOME = os.path.expanduser("~/.rei-agent")

DIRECTORIES = [
    "config",
    "portfolio",
    "portfolio/transactions",
    "portfolio/monthly",
    "deals/pipeline",
    "deals/archive",
    "deals/watchlist",
    "market_data/cache",
    "market_data/reports",
    "templates",
]

# Get the agent root directory (parent of scripts/)
AGENT_ROOT = Path(__file__).parent.parent


def create_directories():
    """Create all required directories."""
    for d in DIRECTORIES:
        path = os.path.join(REI_HOME, d)
        os.makedirs(path, exist_ok=True)
        print(f"  ✓ {path}")


def copy_config_files():
    """Copy default config files if they don't exist."""
    configs = {
        "config/assumptions.json": AGENT_ROOT / "config" / "assumptions.json",
        "config/investor_profile.json": AGENT_ROOT / "config" / "investor_profile.json",
    }
    
    for dest_rel, source in configs.items():
        dest = os.path.join(REI_HOME, dest_rel)
        if not os.path.exists(dest) and source.exists():
            shutil.copy2(source, dest)
            print(f"  ✓ Copied {dest_rel}")
        elif os.path.exists(dest):
            print(f"  ⏭ {dest_rel} already exists, skipping")
        else:
            print(f"  ⚠ Source not found: {source}")


def copy_templates():
    """Copy template files."""
    templates_src = AGENT_ROOT / "templates"
    templates_dst = os.path.join(REI_HOME, "templates")
    
    if templates_src.exists():
        for f in templates_src.iterdir():
            dest = os.path.join(templates_dst, f.name)
            if not os.path.exists(dest):
                shutil.copy2(f, dest)
                print(f"  ✓ Template: {f.name}")


def init_portfolio():
    """Initialize empty portfolio file."""
    portfolio_file = os.path.join(REI_HOME, "portfolio", "properties.json")
    if not os.path.exists(portfolio_file):
        data = {
            "properties": [],
            "last_updated": datetime.now().isoformat(),
            "portfolio_notes": ""
        }
        with open(portfolio_file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"  ✓ Initialized portfolio: {portfolio_file}")
    else:
        print(f"  ⏭ Portfolio already exists, skipping")


def interactive_profile_setup():
    """Interactive investor profile setup."""
    print("\n" + "=" * 60)
    print("  INVESTOR PROFILE SETUP")
    print("=" * 60)
    
    profile_path = os.path.join(REI_HOME, "config", "investor_profile.json")
    
    with open(profile_path, "r") as f:
        profile = json.load(f)
    
    print("\nLet's set up your investor profile. Press Enter to skip any field.\n")
    
    # Basic info
    name = input("Your name: ").strip()
    if name:
        profile["investor_name"] = name
    
    entity = input("Entity name (LLC, etc.): ").strip()
    if entity:
        profile["entity_name"] = entity
    
    # Experience
    print("\nExperience level:")
    print("  1. Beginner (0-2 deals)")
    print("  2. Intermediate (3-10 deals)")
    print("  3. Experienced (10+ deals)")
    exp = input("Choose [1-3]: ").strip()
    exp_map = {"1": "beginner", "2": "intermediate", "3": "experienced"}
    if exp in exp_map:
        profile["experience_level"] = exp_map[exp]
    
    # Strategy
    print("\nPrimary investment strategy:")
    print("  1. Buy and hold (long-term rental)")
    print("  2. BRRRR")
    print("  3. House hacking")
    print("  4. Fix and flip")
    print("  5. Value-add")
    strat = input("Choose [1-5]: ").strip()
    strat_map = {
        "1": "buy_and_hold", "2": "brrrr", "3": "house_hack",
        "4": "fix_and_flip", "5": "value_add"
    }
    if strat in strat_map:
        profile["investment_goals"]["primary_strategy"] = strat_map[strat]
    
    # Capital
    cap = input("\nAvailable capital for investing ($): ").strip().replace(",", "").replace("$", "")
    if cap:
        try:
            profile["financial_position"]["available_capital"] = float(cap)
        except ValueError:
            pass
    
    # Return targets
    print("\nReturn targets (press Enter to keep defaults):")
    
    coc = input(f"  Minimum cash-on-cash return % [{profile['return_targets']['min_cash_on_cash']}]: ").strip()
    if coc:
        try:
            profile["return_targets"]["min_cash_on_cash"] = float(coc)
        except ValueError:
            pass
    
    per_door = input(f"  Minimum per-door monthly cash flow $ [{profile['return_targets']['min_per_door_monthly']}]: ").strip()
    if per_door:
        try:
            profile["return_targets"]["min_per_door_monthly"] = float(per_door)
        except ValueError:
            pass
    
    # Target markets
    markets = input("\nTarget markets (comma-separated cities/metros): ").strip()
    if markets:
        profile["target_markets"]["primary"] = [m.strip() for m in markets.split(",")]
    
    # Max purchase price
    max_price = input("\nMaximum purchase price ($): ").strip().replace(",", "").replace("$", "")
    if max_price:
        try:
            profile["target_properties"]["max_purchase_price"] = float(max_price)
        except ValueError:
            pass
    
    # Save
    profile["created_date"] = datetime.now().isoformat()
    profile["last_updated"] = datetime.now().isoformat()
    
    with open(profile_path, "w") as f:
        json.dump(profile, f, indent=2)
    
    print(f"\n  ✓ Profile saved to {profile_path}")
    print("  You can edit this file directly or use /profile edit to update.\n")


def main():
    parser = argparse.ArgumentParser(description="REI Agent Setup")
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Run interactive investor profile setup")
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("  REI AGENT — SETUP")
    print("=" * 60)
    
    print(f"\nInitializing data directory: {REI_HOME}\n")
    
    print("Creating directories...")
    create_directories()
    
    print("\nCopying config files...")
    copy_config_files()
    
    print("\nCopying templates...")
    copy_templates()
    
    print("\nInitializing portfolio...")
    init_portfolio()
    
    print("\n" + "=" * 60)
    print("  ✅ Setup complete!")
    print("=" * 60)
    
    if args.interactive:
        interactive_profile_setup()
    else:
        print(f"\nRun with --interactive to set up your investor profile.")
        print(f"Or edit directly: {REI_HOME}/config/investor_profile.json\n")


if __name__ == "__main__":
    main()
