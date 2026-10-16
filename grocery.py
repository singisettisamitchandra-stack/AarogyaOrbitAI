
from tools import calculate_grocery_budget, compare_budget


def create_grocery_summary(items: list[dict], budget: float) -> dict:
    """
    Calculate grocery costs and compare them with a budget.
    """

    if budget <= 0:
        raise ValueError("Budget must be greater than zero.")

    grocery = calculate_grocery_budget(items)

    comparison = compare_budget(
        grocery["total_rupees"],
        budget,
    )

    return {
        "grocery_items": grocery["items"],
        "total_rupees": grocery["total_rupees"],
        "budget_comparison": comparison,
        "note": grocery["note"],
    }
