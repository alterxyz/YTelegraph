# Repository Guidelines

## Project Structure & Module Organization

YTelegraph is a small Python package for publishing Markdown and DOM content through the Telegraph API.

- `ytelegraph/` contains the package code: `api.py` for page operations, `account.py` for token/account handling, and `md_to_dom.py` for Markdown conversion.
- `examples/` contains runnable usage examples for creating, editing, and inspecting Telegraph pages.
- `draft_tests/` contains exploratory/manual integration scripts. Many call the live Telegraph API or wait for user input.
- `setup.py`, `requirements.txt`, `README.md`, and `CHANGELOG.md` define packaging, dependencies, usage docs, and release history.

## Build, Test, and Development Commands

This project historically uses plain pip/setuptools. Use uv as an additional compatibility path, not as the source of truth.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt -e .
```

Install the package in editable mode with runtime dependencies.

```bash
python -m unittest discover -s tests
python -m compileall ytelegraph tests
python -m pip install build
python -m build
```

Use `compileall` as a quick syntax check. Use `python -m build` to verify source and wheel distributions; install `build` first if needed.

Run the uv compatibility path intentionally:

```bash
uv run --with-requirements requirements.txt python -m unittest discover -s tests
uv run --with-requirements requirements.txt python -m compileall ytelegraph tests
uv run --with build --with-requirements requirements.txt python -m build
```

```bash
python examples/basic_usage.py
python examples/second_usage.py
python draft_tests/test_space_missing.py
```

Run examples and draft tests intentionally because they may create or edit live Telegraph pages.

## Coding Style & Naming Conventions

Use Python 3.8-compatible syntax, 4-space indentation, and clear type hints for public interfaces. Keep module names lowercase with underscores. Follow existing API naming: Markdown helpers end in `_md`, append helpers use explicit names such as `edit_page_md_append_to_front`, and internal helpers are prefixed with `_`.

Keep docstrings concise and focused on behavior, arguments, returns, and exceptions. Avoid broad refactors when fixing targeted API behavior.

## Testing Guidelines

The `tests/` directory contains deterministic unit tests. Treat `draft_tests/` as integration/manual coverage and add isolated tests when changing parsing or path-handling logic. New tests should be named `test_<behavior>.py`; prefer deterministic tests for `md_to_dom` and API payload behavior that do not require network access. For live API checks, use disposable pages and avoid relying on existing public page paths.

## Commit & Pull Request Guidelines

Git history uses short messages, often with Conventional Commit prefixes such as `feat:`, `fix:`, and `chore:`. Prefer that style: `fix: preserve spaces in markdown formatting`.

Pull requests should include a short problem summary, the implementation approach, commands run, and any live Telegraph API effects. Link related issues when available. Include screenshots or page URLs only when they help verify user-visible publishing behavior.

## Security & Configuration Tips

Never commit Telegraph access tokens or generated `ph_token.txt` files. Use `TELEGRA_PH_TOKEN` for an access token, and `PH_TOKEN_PATH` or a local ignored token file for manual testing.
