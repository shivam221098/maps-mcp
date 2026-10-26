# maps-mcp

MCP server (Python, FastMCP) exposing map capabilities from Google Maps Platform
(Places, Routes, Geocoding, Address Validation), OpenStreetMap (Nominatim, Overpass),
OSS routing engines (OSRM, Valhalla, OpenRouteService, GraphHopper) and other open
geocoders/tiles (Photon, Pelias, static maps) behind one tool surface.

## Status
Early development. The server skeleton (stdio + streamable HTTP, `ping` tool) is in
place; no provider adapters yet. Backlog lives in GitHub Issues and the "maps-mcp Scrum
Board" project. Design questions live in GitHub Discussions.

## Stack
Python 3.11+, FastMCP 4.1.4 (`fastmcp`, pinned; built on the official `mcp` SDK), httpx,
pydantic, pytest, ruff, mypy. Package manager: uv (`brew install uv`). Docker is
available for local Nominatim/OSRM/Valhalla.

Settled in Discussion #94: both stdio and streamable HTTP from the start, FastMCP 4.1.4,
async throughout. Tools and provider/HTTP calls must be `async` and never block the event
loop. In stdio mode stdout is the protocol channel: never `print()` to it (log to stderr).

Layout: `src/maps_mcp/` (package, src layout; `server.py` has `create_server()` and the
tools, `__main__.py` is the CLI), `tests/`, `pyproject.toml` (build, ruff, mypy and pytest
config), `uv.lock` (committed). `.python-version` pins dev to 3.11, the minimum supported
version.

## Commands
- Install: `uv sync` (creates `.venv`, installs the project and the dev group)
- Lint: `uv run ruff check .` (add `--fix` to autofix)
- Format: `uv run ruff format .` (CI-style check: `uv run ruff format --check .`)
- Types: `uv run mypy` (strict, covers `src` and `tests`)
- Test: `uv run pytest`
- Run (stdio, default): `uv run maps-mcp` (or `uv run python -m maps_mcp`)
- Run (streamable HTTP): `uv run maps-mcp --transport http [--host 127.0.0.1] [--port 8000]`,
  served at `/mcp`. Env vars `MAPS_MCP_TRANSPORT`, `MAPS_MCP_HOST`, `MAPS_MCP_PORT` do the
  same; CLI options win. HTTP has no auth yet (#84), so keep it on localhost.
- Version: `uv run maps-mcp --version`
- Inspector (stdio): `npx @modelcontextprotocol/inspector uv run maps-mcp`; non-interactive:
  `npx @modelcontextprotocol/inspector --cli .venv/bin/maps-mcp --method tools/call --tool-name ping`
- Add a dependency: `uv add <pkg>` (runtime) or `uv add --dev <pkg>` (dev group), and
  commit the updated `uv.lock`
- Definition-of-Done gate: `uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest`

## Workflow (Scrum, epics only)
- Work is tracked as epics, stories and spikes (labels: epic/story/spike/bug/chore/docs,
  area:*, P0-P2, points:*). Sprints are NOT pre-assigned; the user assigns them.
- One issue, one branch, one PR with "Closes #n". Pick up only issues labelled `ready`.
- `needs-discussion` means the design question must be settled in a Discussion first.
- Definition of Done: tests pass, ruff and mypy clean, docs updated, the provider's
  usage/ToS constraints respected.

## Reference material (local only, gitignored)
`sources/Nominatim` (API docs in `docs/api`) and `sources/google-cloud-python`
(`packages/google-maps-*`: places, routing, geocode, addressvalidation, ...). Read-only
references. Never edit them or commit them; each is its own git repo.

## Hard rules
- API keys and secrets come from env or config only. Never commit them, never log them.
- Respect provider policies: Nominatim public instance (max 1 req/s, identifying
  User-Agent, cache results); Overpass and OSRM demo servers are fair-use only; Google
  Maps Platform ToS limits caching and requires field masks to control cost; OSM data
  needs ODbL attribution.
- Tools return normalized models (Coordinates, Place, Route, ...) and GeoJSON where it
  helps. Keep the exposed tool count small to avoid bloating LLM context.

## GitHub CLI notes
- Repo: shivam221098/maps-mcp. Push over SSH (the HTTPS credential helper is osxkeychain).
- `gh` has no discussion command; use `gh api graphql` (`createDiscussion`).
- Sleep briefly between bulk `gh issue create` calls to avoid secondary rate limits.
- `.claude/settings.local.json` allows `gh api *`, which includes mutations. Confirm
  before any destructive call.
