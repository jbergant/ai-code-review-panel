# SPEC — panel-fixture (build-project contract)

The planted-bug sample repository the student runs the three AI reviewers on. This is the ONE code
project for the bitesized edition. It is used by **v05** (intro / get-the-code beat), **v06**, **v09**,
**v10**, and **v12**. Concept lessons need no project.

**Reuse, do not reinvent.** The fixture already exists from the shared spike at
`../../../ai-code-review/spike/panel-fixture/` (a git repo: `store.py` baseline on `main`, `checkout.py`
with the five planted bugs added on branch `feat/checkout`, verified by the spike). `/build-project`
copies that fixture into `projects/panel-fixture/` and adds the README and `verify.py` below. Do not
author a new fixture.

## Why this shape (repository, not a loose folder)

CodeRabbit and Greptile are GitHub apps that review **pull requests on a repository** — they cannot
review a downloaded zip. So the deliverable is a real git repository the student controls:

- `main` branch: `store.py` — the pre-change baseline (integer-cents order store, no bugs).
- `feat/checkout` branch: adds `checkout.py` — the change under review, carrying all five planted bugs
  and the false-positive magnet. `store.py` is also present on this branch (branched from `main`).

The student clones or forks the repo, opens a pull request from `feat/checkout` into `main`, connects
the three reviewers to that PR, and runs the panel. This is why the recommended code-access method is
**github**, and why v05's get-the-code beat should say "clone/fork the repo and open the PR", not
"download".

## Files to create in `projects/panel-fixture/`

1. **`store.py`** — copied verbatim from the spike fixture (`main`). Baseline, no defects. Functions:
   `line_total(price_cents, qty) -> int` and `order_total(lines) -> int`. Establishes the invariant that
   money is integer cents everywhere, so the money-as-float bug in `checkout.py` is a real defect, not a
   style choice.
2. **`checkout.py`** — copied from the spike fixture (`feat/checkout`), **with the `# planted:` and
   `# false-positive magnet:` giveaway comments removed** from the shipped student-facing copy. Those
   comments name each bug and would spoil the exercise (the whole point is the student's own reviewer run
   finds them). The buggy code lines stay exactly as they are; only the answer-key comments come out. The
   enumerated bug list below is the instructor answer key — it lives in this SPEC and in `verify.py`, not
   in narration and not in the shipped code comments.
3. **`README.md`** — short. States plainly: this is a deliberate teaching fixture; `checkout.py` (the
   change on `feat/checkout`) contains intentional defects planted so you can practice running AI
   reviewers against a change with real problems in it. Tells the student to open the PR from
   `feat/checkout` into `main` and connect the reviewers. Does **not** enumerate the bugs (no spoilers).
4. **`verify.py`** — the headless check the `verify_cmd` runs. See "What verify.py checks" below.

## The five planted bugs (instructor answer key — locations in `checkout.py`)

Because this fixture contains INTENTIONAL bugs, "tests pass" is the wrong verification. Correct = each
planted defect is present so the reviewers have real problems to find. Code-level markers (the actual
buggy lines, robust to reformatting and independent of the giveaway comments):

| # | Bug | Location | Code marker verify.py asserts is present |
|---|---|---|---|
| 1 | SQL injection | `get_user()` — user id interpolated into the query via f-string | `WHERE id = {user_id}` |
| 2 | Hardcoded secret | module top — hardcoded API key literal | `PAYMENTS_API_KEY = "live_pmt_` |
| 3 | Money as float | `apply_discount()` returns a float, breaking the integer-cents invariant | `/ 100.0` **and** the signature `def apply_discount(` returning `-> float` |
| 4 | Off-by-one | `running_totals()` iterates one index too far | `range(len(prices) + 1)` |
| 5 | None dereference | `notify()` reads `user.email` when `charge()` may pass a `None` user | `user.email.upper()` |

## The false-positive magnet (must also be present)

`notify(user, message, tags=[])` — a **mutable default argument** that is only ever read (joined into a
label), never mutated. It is safe here, but many reviewers flag mutable defaults reflexively. This is the
piece of safe-looking code a good reviewer should decline to flag; it is what O3/v09 uses to show a
reviewer correctly producing zero false positives. Code marker: `def notify(user, message, tags=[])`.

## Expected behavior

The fixture is not meant to run a passing test suite — it is a change under review. `store.py` and
`checkout.py` must both be valid, importable Python (they parse). The defects are semantic/security
defects a reviewer reports, not syntax errors.

## What `verify_cmd` checks (`python3 verify.py`, run with cwd = `projects/panel-fixture`)

`verify.py` must exit **0 only when the fixture is intact** and fail loud (non-zero exit, naming the
missing item) otherwise. It must be fully headless — no arguments, no human input. It:

1. Reads `store.py` and `checkout.py` from the `feat/checkout` branch (which carries both), e.g. via
   `git show feat/checkout:checkout.py` / `git show feat/checkout:store.py`. Reading from the branch (not
   only the working tree) makes the check independent of which branch happens to be checked out.
2. `ast.parse()` both sources — asserts each is valid, parseable Python (fails loud with the file name
   and the SyntaxError if not).
3. Asserts each of the five planted-bug code markers (table above) appears in `checkout.py`. Missing any
   marker = a planted bug was lost = exit non-zero naming which one.
4. Asserts the false-positive magnet marker (`tags=[]` in `notify`) appears in `checkout.py`.
5. Prints a one-line pass summary ("panel-fixture intact: 5 planted bugs + 1 false-positive magnet
   present, both files parse") and exits 0.

This proves what the course needs: the code is usable Python and every defect the reviewers are supposed
to find — plus the safe code they are supposed to NOT flag — is really there.
