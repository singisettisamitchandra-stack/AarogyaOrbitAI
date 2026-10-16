from typing import Any


# Demo grocery data. Replace with actual local shop prices
# before using this for real purchases.
GROCERY_ITEMS = {
    "eggs": {"price": 42, "unit": "6 eggs"},
    "roasted chana": {"price": 35, "unit": "250 g"},
    "soya chunks": {"price": 35, "unit": "200 g"},
    "peanuts": {"price": 40, "unit": "200 g"},
    "dal": {"price": 75, "unit": "500 g"},
    "milk": {"price": 60, "unit": "1 litre"},
}


def calculate_grocery_budget(items: list[dict[str, Any]]) -> dict:
    """Calculate grocery cost from known demo prices and quantities."""
    total = 0
    breakdown = []

    for item in items:
        name = str(item.get("name", "")).strip().lower()
        quantity = item.get("quantity", 1)

        if name not in GROCERY_ITEMS:
            breakdown.append({
                "name": name,
                "error": "Item not found in demo price list."
            })
            continue

        if not isinstance(quantity, (int, float)) or isinstance(quantity, bool):
            raise ValueError("Quantity must be a number.")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        unit_price = GROCERY_ITEMS[name]["price"]
        cost = unit_price * quantity
        total += cost

        breakdown.append({
            "name": name,
            "quantity": quantity,
            "unit": GROCERY_ITEMS[name]["unit"],
            "unit_price_rupees": unit_price,
            "cost_rupees": round(cost, 2),
        })

    return {
        "items": breakdown,
        "total_rupees": round(total, 2),
        "note": "Demo prices only; confirm current prices with your local shop."
    }


def compare_budget(total: float, budget: float) -> dict:
    """Compare a calculated grocery total with a user's budget."""
    if budget < 0 or total < 0:
        raise ValueError("Budget and total cannot be negative.")

    difference = round(budget - total, 2)

    return {
        "budget_rupees": budget,
        "total_rupees": total,
        "remaining_rupees": max(0, difference),
        "over_budget_rupees": max(0, -difference),
        "within_budget": total <= budget,
    }
