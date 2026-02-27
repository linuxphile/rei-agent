#!/usr/bin/env python3
"""
REI Agent — Core Financial Calculations Engine

All return metrics, cash flow models, and financial analysis functions.
Import this module for consistent calculations across all skills.

Usage:
    python scripts/calculate_returns.py --input deal_params.json --output results.json
    
    # Or import directly:
    from scripts.calculate_returns import (
        calculate_mortgage_payment, calculate_noi, calculate_cash_flow,
        calculate_coc, calculate_cap_rate, calculate_irr, calculate_dscr,
        full_underwriting, sensitivity_analysis
    )
"""

import json
import math
import sys
import argparse
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict


@dataclass
class PropertyData:
    """Property physical and location data."""
    address: str = ""
    property_type: str = ""  # sfr, duplex, triplex, quad, small_multi
    units: int = 1
    sqft: int = 0
    year_built: int = 0
    condition: int = 5  # 1-10 scale


@dataclass 
class IncomeData:
    """Rental income data."""
    unit_rents: List[float] = field(default_factory=list)  # Monthly rent per unit
    other_income: float = 0.0  # Monthly (laundry, parking, etc.)
    
    @property
    def gross_monthly(self) -> float:
        return sum(self.unit_rents) + self.other_income
    
    @property
    def gross_annual(self) -> float:
        return self.gross_monthly * 12


@dataclass
class ExpenseData:
    """Operating expense data. Monthly amounts unless noted."""
    taxes: float = 0.0
    insurance: float = 0.0
    hoa: float = 0.0
    management_pct: float = 0.08  # As decimal (8% = 0.08)
    management_flat: Optional[float] = None  # Use instead of pct if set
    maintenance_pct: float = 0.05
    capex_pct: float = 0.05
    vacancy_pct: float = 0.08
    credit_loss_pct: float = 0.02
    utilities: float = 0.0  # Owner-paid only
    landscaping: float = 0.0
    pest_control: float = 0.0
    legal_accounting: float = 0.0  # Annual
    advertising: float = 0.0  # Annual
    misc_pct: float = 0.02


@dataclass
class FinancingData:
    """Loan terms."""
    loan_amount: float = 0.0
    interest_rate: float = 0.065  # Annual as decimal
    term_months: int = 360
    loan_type: str = "conventional"
    points: float = 0.0
    closing_costs: float = 0.0


@dataclass
class DealData:
    """Complete deal parameters."""
    purchase_price: float = 0.0
    down_payment_pct: float = 0.20
    closing_costs: float = 0.0
    rehab_budget: float = 0.0
    holding_period_years: int = 5
    property: PropertyData = field(default_factory=PropertyData)
    income: IncomeData = field(default_factory=IncomeData)
    expenses: ExpenseData = field(default_factory=ExpenseData)
    financing: FinancingData = field(default_factory=FinancingData)


@dataclass
class UnderwritingResults:
    """Complete underwriting output."""
    # Income
    gross_potential_income: float = 0.0
    vacancy_loss: float = 0.0
    credit_loss: float = 0.0
    effective_gross_income: float = 0.0
    
    # Expenses
    total_operating_expenses: float = 0.0
    expense_breakdown: Dict[str, float] = field(default_factory=dict)
    opex_ratio: float = 0.0
    
    # NOI
    noi: float = 0.0
    
    # Debt Service
    monthly_payment: float = 0.0
    annual_debt_service: float = 0.0
    
    # Cash Flow
    annual_cash_flow: float = 0.0
    monthly_cash_flow: float = 0.0
    per_unit_monthly: float = 0.0
    
    # Returns
    cash_on_cash: float = 0.0
    cap_rate: float = 0.0
    grm: float = 0.0
    dscr: float = 0.0
    roe: float = 0.0
    irr: float = 0.0
    equity_multiple: float = 0.0
    
    # Investment
    total_cash_invested: float = 0.0
    loan_amount: float = 0.0
    
    # Break-even
    break_even_vacancy: float = 0.0
    break_even_rent_reduction: float = 0.0
    break_even_rate: float = 0.0


# ── Core Calculation Functions ────────────────────────────────────────

def calculate_mortgage_payment(
    principal: float,
    annual_rate: float,
    term_months: int
) -> float:
    """Calculate monthly mortgage payment (P&I only)."""
    if principal <= 0 or annual_rate <= 0 or term_months <= 0:
        return 0.0
    
    monthly_rate = annual_rate / 12
    payment = principal * (
        monthly_rate * (1 + monthly_rate) ** term_months
    ) / (
        (1 + monthly_rate) ** term_months - 1
    )
    return round(payment, 2)


def calculate_loan_balance(
    original_principal: float,
    annual_rate: float,
    term_months: int,
    months_elapsed: int
) -> float:
    """Calculate remaining loan balance after N months."""
    if months_elapsed <= 0:
        return original_principal
    if months_elapsed >= term_months:
        return 0.0
    
    monthly_rate = annual_rate / 12
    balance = original_principal * (
        (1 + monthly_rate) ** term_months - (1 + monthly_rate) ** months_elapsed
    ) / (
        (1 + monthly_rate) ** term_months - 1
    )
    return round(balance, 2)


def generate_amortization_schedule(
    principal: float,
    annual_rate: float,
    term_months: int,
    extra_payment: float = 0.0
) -> List[Dict]:
    """Generate full amortization schedule."""
    monthly_rate = annual_rate / 12
    payment = calculate_mortgage_payment(principal, annual_rate, term_months)
    
    schedule = []
    balance = principal
    cum_principal = 0.0
    cum_interest = 0.0
    
    for month in range(1, term_months + 1):
        interest_payment = round(balance * monthly_rate, 2)
        principal_payment = round(payment - interest_payment + extra_payment, 2)
        
        # Don't overpay
        if principal_payment > balance:
            principal_payment = balance
        
        balance = round(balance - principal_payment, 2)
        cum_principal += principal_payment
        cum_interest += interest_payment
        
        schedule.append({
            "month": month,
            "payment": round(payment + extra_payment, 2),
            "principal": principal_payment,
            "interest": interest_payment,
            "balance": max(balance, 0),
            "cum_principal": round(cum_principal, 2),
            "cum_interest": round(cum_interest, 2)
        })
        
        if balance <= 0:
            break
    
    return schedule


def calculate_noi(deal: DealData) -> Tuple[float, Dict[str, float]]:
    """Calculate Net Operating Income with itemized expenses."""
    # Gross Potential Income
    gpi = deal.income.gross_annual
    
    # Vacancy and Credit Loss
    vacancy_loss = gpi * deal.expenses.vacancy_pct
    credit_loss = gpi * deal.expenses.credit_loss_pct
    egi = gpi - vacancy_loss - credit_loss
    
    # Operating Expenses
    expenses = {}
    expenses["property_taxes"] = deal.expenses.taxes * 12
    expenses["insurance"] = deal.expenses.insurance * 12
    expenses["hoa"] = deal.expenses.hoa * 12
    
    if deal.expenses.management_flat is not None:
        expenses["management"] = deal.expenses.management_flat * 12
    else:
        expenses["management"] = egi * deal.expenses.management_pct
    
    expenses["maintenance"] = egi * deal.expenses.maintenance_pct
    expenses["capex_reserves"] = egi * deal.expenses.capex_pct
    expenses["utilities"] = deal.expenses.utilities * 12
    expenses["landscaping"] = deal.expenses.landscaping * 12
    expenses["pest_control"] = deal.expenses.pest_control * 12
    expenses["legal_accounting"] = deal.expenses.legal_accounting
    expenses["advertising"] = deal.expenses.advertising
    expenses["miscellaneous"] = egi * deal.expenses.misc_pct
    
    total_opex = sum(expenses.values())
    noi = egi - total_opex
    
    return round(noi, 2), {k: round(v, 2) for k, v in expenses.items()}


def calculate_cash_flow(noi: float, annual_debt_service: float) -> float:
    """Calculate annual cash flow."""
    return round(noi - annual_debt_service, 2)


def calculate_coc(annual_cash_flow: float, total_cash_invested: float) -> float:
    """Calculate cash-on-cash return as percentage."""
    if total_cash_invested <= 0:
        return float('inf') if annual_cash_flow > 0 else 0.0
    return round((annual_cash_flow / total_cash_invested) * 100, 2)


def calculate_cap_rate(noi: float, purchase_price: float) -> float:
    """Calculate capitalization rate as percentage."""
    if purchase_price <= 0:
        return 0.0
    return round((noi / purchase_price) * 100, 2)


def calculate_grm(purchase_price: float, annual_gross_rent: float) -> float:
    """Calculate Gross Rent Multiplier."""
    if annual_gross_rent <= 0:
        return 0.0
    return round(purchase_price / annual_gross_rent, 2)


def calculate_dscr(noi: float, annual_debt_service: float) -> float:
    """Calculate Debt Service Coverage Ratio."""
    if annual_debt_service <= 0:
        return float('inf')
    return round(noi / annual_debt_service, 2)


def calculate_irr(
    initial_investment: float,
    annual_cash_flows: List[float],
    terminal_value: float
) -> float:
    """
    Calculate Internal Rate of Return using Newton's method.
    
    Args:
        initial_investment: Total cash invested (positive number)
        annual_cash_flows: Annual cash flows for each hold year
        terminal_value: Net proceeds from sale in final year
    """
    # Build cash flow series
    flows = [-initial_investment]
    for i, cf in enumerate(annual_cash_flows):
        if i == len(annual_cash_flows) - 1:
            flows.append(cf + terminal_value)
        else:
            flows.append(cf)
    
    # Newton's method for IRR
    guess = 0.10
    for _ in range(1000):
        npv = sum(f / (1 + guess) ** t for t, f in enumerate(flows))
        dnpv = sum(-t * f / (1 + guess) ** (t + 1) for t, f in enumerate(flows))
        
        if abs(dnpv) < 1e-12:
            break
        
        new_guess = guess - npv / dnpv
        if abs(new_guess - guess) < 1e-8:
            guess = new_guess
            break
        guess = new_guess
    
    return round(guess * 100, 2)


def calculate_equity_multiple(
    total_cash_received: float,
    total_cash_invested: float
) -> float:
    """Calculate equity multiple."""
    if total_cash_invested <= 0:
        return 0.0
    return round(total_cash_received / total_cash_invested, 2)


# ── Full Underwriting ─────────────────────────────────────────────────

def full_underwriting(deal: DealData) -> UnderwritingResults:
    """Run complete property underwriting and return all metrics."""
    results = UnderwritingResults()
    
    # Income
    results.gross_potential_income = deal.income.gross_annual
    results.vacancy_loss = results.gross_potential_income * deal.expenses.vacancy_pct
    results.credit_loss = results.gross_potential_income * deal.expenses.credit_loss_pct
    results.effective_gross_income = (
        results.gross_potential_income - results.vacancy_loss - results.credit_loss
    )
    
    # NOI
    results.noi, results.expense_breakdown = calculate_noi(deal)
    results.total_operating_expenses = sum(results.expense_breakdown.values())
    results.opex_ratio = (
        results.total_operating_expenses / results.effective_gross_income * 100
        if results.effective_gross_income > 0 else 0
    )
    
    # Financing
    down_payment = deal.purchase_price * deal.down_payment_pct
    results.loan_amount = deal.purchase_price - down_payment
    results.monthly_payment = calculate_mortgage_payment(
        results.loan_amount,
        deal.financing.interest_rate,
        deal.financing.term_months
    )
    results.annual_debt_service = results.monthly_payment * 12
    
    # Cash Flow
    results.annual_cash_flow = calculate_cash_flow(
        results.noi, results.annual_debt_service
    )
    results.monthly_cash_flow = round(results.annual_cash_flow / 12, 2)
    results.per_unit_monthly = round(
        results.monthly_cash_flow / max(deal.property.units, 1), 2
    )
    
    # Total Cash Invested
    results.total_cash_invested = (
        down_payment +
        deal.closing_costs +
        deal.rehab_budget +
        deal.financing.closing_costs
    )
    
    # Return Metrics
    results.cash_on_cash = calculate_coc(
        results.annual_cash_flow, results.total_cash_invested
    )
    results.cap_rate = calculate_cap_rate(results.noi, deal.purchase_price)
    results.grm = calculate_grm(
        deal.purchase_price, results.gross_potential_income
    )
    results.dscr = calculate_dscr(results.noi, results.annual_debt_service)
    
    # IRR (projected over hold period)
    annual_cash_flows = []
    for year in range(deal.holding_period_years):
        growth = (1.02) ** year  # 2% rent growth default
        annual_cf = results.annual_cash_flow * growth
        annual_cash_flows.append(annual_cf)
    
    # Terminal value
    terminal_noi = results.noi * (1.02) ** deal.holding_period_years
    exit_cap_rate = results.cap_rate / 100 + 0.005  # Slight cap rate expansion
    if exit_cap_rate > 0:
        sale_price = terminal_noi / exit_cap_rate
    else:
        sale_price = deal.purchase_price
    
    selling_costs = sale_price * 0.07
    remaining_balance = calculate_loan_balance(
        results.loan_amount,
        deal.financing.interest_rate,
        deal.financing.term_months,
        deal.holding_period_years * 12
    )
    terminal_value = sale_price - selling_costs - remaining_balance
    
    results.irr = calculate_irr(
        results.total_cash_invested, annual_cash_flows, terminal_value
    )
    
    total_cash_received = sum(annual_cash_flows) + terminal_value
    results.equity_multiple = calculate_equity_multiple(
        total_cash_received, results.total_cash_invested
    )
    
    # Break-even Analysis
    if results.gross_potential_income > 0:
        # Break-even vacancy
        cf_before_vacancy = results.noi + results.vacancy_loss - results.annual_debt_service
        if results.gross_potential_income > 0:
            results.break_even_vacancy = round(
                (cf_before_vacancy / results.gross_potential_income) * 100, 1
            )
        
        # Break-even rent reduction
        if results.annual_cash_flow >= 0:
            results.break_even_rent_reduction = round(
                (results.annual_cash_flow / results.gross_potential_income) * 100, 1
            )
    
    return results


# ── Sensitivity Analysis ──────────────────────────────────────────────

def sensitivity_analysis(
    deal: DealData,
    variables: Optional[Dict] = None
) -> Dict:
    """
    Run sensitivity analysis on key variables.
    
    Returns dict with base case and stressed scenarios.
    """
    if variables is None:
        variables = {
            "rent_change": [-0.10, -0.05, 0, 0.05, 0.10],
            "vacancy_change": [0, 0.03, 0.05, 0.10],
            "rate_change": [-0.01, -0.005, 0, 0.005, 0.01, 0.015],
            "expense_change": [0, 0.10, 0.20],
            "price_change": [-0.10, -0.05, 0, 0.05, 0.10],
        }
    
    base = full_underwriting(deal)
    results = {"base_case": asdict(base), "scenarios": {}}
    
    # Rent sensitivity
    rent_scenarios = []
    for change in variables.get("rent_change", []):
        modified = DealData(**{
            **asdict(deal),
            "income": IncomeData(
                unit_rents=[r * (1 + change) for r in deal.income.unit_rents],
                other_income=deal.income.other_income
            )
        })
        # Reconstruct nested dataclasses
        modified.property = deal.property
        modified.expenses = deal.expenses
        modified.financing = deal.financing
        
        r = full_underwriting(modified)
        rent_scenarios.append({
            "change": f"{change:+.0%}",
            "monthly_cash_flow": r.monthly_cash_flow,
            "cash_on_cash": r.cash_on_cash,
            "dscr": r.dscr,
            "noi": r.noi
        })
    results["scenarios"]["rent"] = rent_scenarios
    
    # Rate sensitivity
    rate_scenarios = []
    for change in variables.get("rate_change", []):
        modified = DealData(**asdict(deal))
        modified.property = deal.property
        modified.income = deal.income
        modified.expenses = deal.expenses
        modified.financing = FinancingData(
            **{**asdict(deal.financing), 
               "interest_rate": deal.financing.interest_rate + change}
        )
        
        r = full_underwriting(modified)
        rate_scenarios.append({
            "rate": f"{(deal.financing.interest_rate + change)*100:.2f}%",
            "monthly_payment": r.monthly_payment,
            "monthly_cash_flow": r.monthly_cash_flow,
            "cash_on_cash": r.cash_on_cash,
            "dscr": r.dscr
        })
    results["scenarios"]["interest_rate"] = rate_scenarios
    
    return results


# ── MAO Calculations ──────────────────────────────────────────────────

def mao_cash_flow(
    target_coc: float,
    cash_available: float,
    monthly_rent: float,
    opex_ratio: float,
    vacancy_rate: float,
    rate: float,
    term_months: int,
    down_payment_pct: float
) -> float:
    """Calculate MAO based on target cash-on-cash return."""
    annual_rent = monthly_rent * 12
    noi = annual_rent * (1 - opex_ratio - vacancy_rate)
    required_cash_flow = cash_available * (target_coc / 100)
    max_debt_service = noi - required_cash_flow
    
    if max_debt_service <= 0:
        return 0.0
    
    max_monthly_ds = max_debt_service / 12
    monthly_rate = rate / 12
    
    # Reverse mortgage payment formula to get max principal
    max_loan = max_monthly_ds * (
        ((1 + monthly_rate) ** term_months - 1) /
        (monthly_rate * (1 + monthly_rate) ** term_months)
    )
    
    max_price = max_loan / (1 - down_payment_pct)
    return round(max_price, 0)


def mao_cap_rate(noi: float, target_cap_rate: float) -> float:
    """Calculate MAO based on target cap rate."""
    if target_cap_rate <= 0:
        return 0.0
    return round(noi / (target_cap_rate / 100), 0)


def mao_brrrr(
    arv: float,
    rehab_costs: float,
    refi_ltv: float,
    closing_costs: float,
    target_cash_left: float = 0
) -> float:
    """Calculate MAO for BRRRR strategy."""
    refi_loan = arv * refi_ltv
    max_all_in = refi_loan - target_cash_left
    max_purchase = max_all_in - rehab_costs - closing_costs
    return round(max(max_purchase, 0), 0)


def mao_grm(annual_gross_rent: float, target_grm: float) -> float:
    """Calculate MAO based on target GRM."""
    return round(annual_gross_rent * target_grm, 0)


# ── Deal Scoring ──────────────────────────────────────────────────────

def score_deal(
    results: UnderwritingResults,
    investor_targets: Dict,
    market_score: float = 70.0
) -> Dict:
    """
    Score a deal on the standard 0-100 matrix.
    
    Args:
        results: UnderwritingResults from full_underwriting
        investor_targets: Dict with min_coc, min_cap_rate, min_dscr, etc.
        market_score: Market quality score from market research (0-100)
    """
    scores = {}
    
    # Cash Flow Score (25%)
    target_per_door = investor_targets.get("min_per_door_monthly", 200)
    if results.per_unit_monthly >= target_per_door * 1.5:
        scores["cash_flow"] = 100
    elif results.per_unit_monthly >= target_per_door:
        scores["cash_flow"] = 70 + 30 * (results.per_unit_monthly - target_per_door) / (target_per_door * 0.5)
    elif results.per_unit_monthly > 0:
        scores["cash_flow"] = 70 * (results.per_unit_monthly / target_per_door)
    else:
        scores["cash_flow"] = 0
    
    # Returns Score (20%)
    target_coc = investor_targets.get("min_coc", 8.0)
    if results.cash_on_cash >= target_coc * 1.5:
        scores["returns"] = 100
    elif results.cash_on_cash >= target_coc:
        scores["returns"] = 70 + 30 * (results.cash_on_cash - target_coc) / (target_coc * 0.5)
    elif results.cash_on_cash > 0:
        scores["returns"] = 70 * (results.cash_on_cash / target_coc)
    else:
        scores["returns"] = 0
    
    # Risk Score (20%)
    risk = 100
    if results.dscr < 1.0:
        risk = 10
    elif results.dscr < 1.15:
        risk = 30
    elif results.dscr < 1.25:
        risk = 60
    elif results.dscr < 1.5:
        risk = 80
    
    if results.break_even_vacancy < 5:
        risk = min(risk, 20)
    elif results.break_even_vacancy < 10:
        risk = min(risk, 50)
    
    scores["risk"] = risk
    
    # Market Score (15%)
    scores["market"] = min(market_score, 100)
    
    # Upside Score (10%) — placeholder, needs additional data
    scores["upside"] = 50  # Default neutral
    
    # Ease Score (10%) — placeholder, needs property condition data
    scores["ease"] = 50  # Default neutral
    
    # Weighted total
    weights = {
        "cash_flow": 0.25,
        "returns": 0.20,
        "risk": 0.20,
        "market": 0.15,
        "upside": 0.10,
        "ease": 0.10
    }
    
    total = sum(scores[k] * weights[k] for k in weights)
    
    # Recommendation
    if total >= 80:
        recommendation = "STRONG BUY"
    elif total >= 65:
        recommendation = "WORTH PURSUING"
    elif total >= 50:
        recommendation = "MARGINAL"
    else:
        recommendation = "PASS"
    
    return {
        "scores": {k: round(v, 1) for k, v in scores.items()},
        "weights": weights,
        "total_score": round(total, 1),
        "recommendation": recommendation
    }


# ── CLI Entry Point ───────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="REI Financial Calculator")
    parser.add_argument("--input", "-i", required=True, help="Deal parameters JSON file")
    parser.add_argument("--output", "-o", help="Output results JSON file")
    parser.add_argument("--sensitivity", "-s", action="store_true", help="Run sensitivity analysis")
    parser.add_argument("--amortization", "-a", action="store_true", help="Generate amortization schedule")
    
    args = parser.parse_args()
    
    with open(args.input, "r") as f:
        params = json.load(f)
    
    # Build DealData from params
    deal = DealData(
        purchase_price=params.get("purchase_price", 0),
        down_payment_pct=params.get("down_payment_pct", 0.20),
        closing_costs=params.get("closing_costs", 0),
        rehab_budget=params.get("rehab_budget", 0),
        holding_period_years=params.get("holding_period_years", 5),
        property=PropertyData(**params.get("property", {})),
        income=IncomeData(**params.get("income", {})),
        expenses=ExpenseData(**params.get("expenses", {})),
        financing=FinancingData(**params.get("financing", {})),
    )
    
    # Run underwriting
    results = full_underwriting(deal)
    output = {"underwriting": asdict(results)}
    
    # Optional sensitivity
    if args.sensitivity:
        output["sensitivity"] = sensitivity_analysis(deal)
    
    # Optional amortization
    if args.amortization:
        schedule = generate_amortization_schedule(
            results.loan_amount,
            deal.financing.interest_rate,
            deal.financing.term_months
        )
        output["amortization"] = schedule
    
    # Output
    result_json = json.dumps(output, indent=2)
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(result_json)
        print(f"Results written to {args.output}")
    else:
        print(result_json)


if __name__ == "__main__":
    main()
