"""Headless integrity check for the panel-fixture teaching repository.

This fixture is a change under review that carries intentional defects, so "tests
pass" is the wrong check. Correct means: both files are valid Python, and every
planted defect (plus the one piece of safe-looking code the reviewers should NOT
flag) is present, so the AI reviewers have real problems to find.

Reads the sources from the feat/checkout branch so the result does not depend on
which branch happens to be checked out. Exits 0 only when the fixture is intact;
otherwise exits non-zero naming what is missing.
"""
import ast
import subprocess
import sys

BRANCH = "feat/checkout"

# (label, marker that must appear in checkout.py)
PLANTED = [
    ("SQL injection (f-string in query)", "WHERE id = {user_id}"),
    ("hardcoded secret (API key literal)", 'PAYMENTS_API_KEY = "live_pmt_'),
    ("money as float (division by 100.0)", "/ 100.0"),
    ("money as float (float return type)", "def apply_discount(price_cents: int, pct: float) -> float"),
    ("off-by-one (iterates one index too far)", "range(len(prices) + 1)"),
    ("None dereference (reads user.email)", "user.email.upper()"),
]
MAGNET = ("mutable default argument (safe here; reviewers must not flag)", "def notify(user, message, tags=[])")


def read_from_branch(path: str) -> str:
    try:
        return subprocess.check_output(["git", "show", f"{BRANCH}:{path}"], text=True)
    except subprocess.CalledProcessError as e:
        sys.exit(f"FAIL: could not read {path} from branch {BRANCH}: {e}")


def main() -> None:
    checkout_src = read_from_branch("checkout.py")
    store_src = read_from_branch("store.py")

    # 1. both files must be valid, parseable Python
    for name, src in (("checkout.py", checkout_src), ("store.py", store_src)):
        try:
            ast.parse(src)
        except SyntaxError as e:
            sys.exit(f"FAIL: {name} does not parse as Python: {e}")

    # 2. every planted-bug marker must be present in checkout.py
    missing = [label for label, marker in PLANTED if marker not in checkout_src]
    if missing:
        sys.exit("FAIL: planted defect(s) missing from checkout.py: " + "; ".join(missing))

    # 3. the false-positive magnet must be present
    magnet_label, magnet_marker = MAGNET
    if magnet_marker not in checkout_src:
        sys.exit(f"FAIL: false-positive magnet missing from checkout.py: {magnet_label}")

    print("panel-fixture intact: 5 planted bugs + 1 false-positive magnet present, both files parse")


if __name__ == "__main__":
    main()
