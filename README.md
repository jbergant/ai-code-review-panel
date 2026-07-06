# AI code review sample repository

This is a deliberate teaching fixture for the course "AI Code Review Without the
Useless Comments." It is not production code and it is not meant to pass a test suite.

The `main` branch holds a working baseline (`store.py`). The `feat/checkout` branch
adds `checkout.py`, a change that contains several intentional problems planted so you
can practice running AI reviewers against a change that has real defects in it.

## How to use it

1. Fork this repository to your own GitHub account.
2. Open a pull request from `feat/checkout` into `main`.
3. Connect the AI reviewers to your fork (the course shows you how).
4. Run the reviewers on the pull request and read what each one reports.

The defects are intentional. Finding them with the reviewers, deciding which comments
to trust, and measuring how often each reviewer is right is the exercise. This README
does not list the problems on purpose.
