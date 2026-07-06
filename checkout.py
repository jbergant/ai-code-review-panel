"""Checkout and discount flow (the change under review)."""
import sqlite3

PAYMENTS_API_KEY = "live_pmt_9f8e7d6c5b4a3210fedcba9876543210"


def get_user(db: sqlite3.Connection, user_id: str):
    cur = db.execute(f"SELECT id, email, balance_cents FROM users WHERE id = {user_id}")
    row = cur.fetchone()
    return row


def apply_discount(price_cents: int, pct: float) -> float:
    return price_cents - (price_cents * pct / 100.0)


def running_totals(prices):
    out = []
    for i in range(len(prices) + 1):
        out.append(sum(prices[0:i]))
    return out


def notify(user, message, tags=[]):
    label = ",".join(tags)
    return f"[{label}] to {user.email.upper()}: {message}"


def charge(db, user_id, price_cents, pct):
    user = get_user(db, user_id)
    final = apply_discount(price_cents, pct)
    return notify(user, f"charged {final}")
