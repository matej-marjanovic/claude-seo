# AGENTS.md

## Cursor Cloud specific instructions

### Product overview

Claude SEO is a Claude Code skill/plugin — not a standalone web application. It consists of
Markdown skill files, subagent definitions, Python helper scripts, JSON schema templates,
and shell install scripts. There is no build step, no server to run, and no database.

### Development commands

| Task | Command |
|------|---------|
| Install deps | `pip install -r requirements.txt` |
| Install Playwright | `python3 -m playwright install --with-deps chromium` |
| CI lint (syntax) | `python3 -m py_compile scripts/fetch_page.py && python3 -m py_compile scripts/parse_html.py && python3 -m py_compile scripts/analyze_visual.py && python3 -m py_compile scripts/capture_screenshot.py` |
| Ruff lint | `ruff check scripts/ hooks/` |
| Fetch a page | `python3 scripts/fetch_page.py <url>` |
| Parse HTML | `python3 scripts/parse_html.py <file> --url <base-url> --json` |
| Visual analysis | `python3 scripts/analyze_visual.py <url> --json` |
| Screenshot capture | `python3 scripts/capture_screenshot.py <url> --output screenshots` |

See `CONTRIBUTING.md` for code style guidelines.

### Gotchas

- The environment's default `pip install` may install to `~/.local/bin` (user site-packages).
  Ensure `$HOME/.local/bin` is on `PATH` when invoking `playwright` CLI directly.
- HTTPS may fail with SSL certificate errors inside some sandbox environments.
  Use `http://` URLs for testing when HTTPS is unavailable.
- `capture_screenshot.py` enforces output paths within CWD or `$HOME`; use relative paths
  like `screenshots/` rather than `/tmp/`.
- There is no `tests/` directory and no `pytest` suite despite `CLAUDE.md` mentioning
  `python -m pytest tests/`. The CI pipeline only runs `py_compile` syntax checks.
- The 3 ruff warnings in `extensions/banana/scripts/setup_mcp.py` (F541 — f-strings without
  placeholders) are pre-existing in the repository.
