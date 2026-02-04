---
name: python-best-practices
description: Apply Python best practices (PEP 8, typing, docs, tests, security).
argument-hint: "Describe what you want built/changed (e.g., 'refactor src/foo.py', 'add tests for X')."
---

When writing Python for this repo, follow these best practices:

- Style: PEP 8, 4-space indents, readable naming (snake_case funcs/vars, PascalCase classes, UPPER_CASE constants), keep functions small and focused.
- Types: Add type hints for parameters and returns; prefer Python 3.10+ typing (e.g., `list[str]`, `dict[str, int]`).
- Structure: Prefer `pathlib.Path` over `os.path`.
- Docs: Add clear module/class/function docstrings (Google or NumPy style). Include an Examples section for non-trivial functions.
- Errors: Validate inputs early; raise specific exceptions; avoid bare `except:`; use `raise ... from e` when wrapping.
- Logging: Use `logging` (not `print`); don’t log secrets/PII.
- Security: Never hardcode credentials; sanitize/validate user input; avoid `eval`/`exec`/`pickle` with untrusted data.
- Testing: Write `pytest` unit tests for new logic; follow Arrange/Act/Assert; mock external dependencies.

If you’re unsure about a choice (API, structure, dependency), ask a clarifying question before coding.