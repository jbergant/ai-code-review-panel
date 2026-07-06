"""Order store — the baseline before the change under review.

All money is kept as integer cents everywhere in this module. Any code that turns
money into a floating point number is a real defect, not a style choice.
"""


def line_total(price_cents: int, qty: int) -> int:
    """Total for one line, in integer cents."""
    return price_cents * qty


def order_total(lines: list[tuple[int, int]]) -> int:
    total = 0
    for price_cents, qty in lines:
        total += line_total(price_cents, qty)
    return total
