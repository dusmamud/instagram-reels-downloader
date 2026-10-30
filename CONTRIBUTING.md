# Contributing

Thanks for helping improve this tool. Keep it simple and honest: real
functionality only, no mock or placeholder features in production code.

## How to contribute
1. Fork the repo, create a branch from `main`.
2. Make one focused change per pull request.
3. Add or update a test in `tests/` for any behaviour change.
4. Run the checks before opening the PR (see below).
5. Describe what you changed, why, and how you tested it in the PR body.

## Checks
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
python -m unittest discover tests
ruff check reels_dl tests
```

## Rules
- Production code: no fake downloads, no hardcoded fake metadata, no TODO stubs
  left as features. Tests may use mocks, but only inside `tests/`.
- Do not commit downloaded videos, cookies, or credentials. `downloads/` is ignored.
- Do not add a feature that bypasses DRM or breaks Instagram's login protections
  beyond the documented cookie modes (browser cookies / cookies.txt you own).
- Keep user-facing messages in the same style as the existing CLI.
- If a claim changes (quality, format, compatibility), update README and the
  relevant doc in the same PR — do not leave docs contradicting code.

## Reporting bugs
Use the bug report template in `.github/ISSUE_TEMPLATE/`. Include:
Python version, OS, command you ran (without your cookies or private URLs),
and the full error output.
