# maps-mcp

MCP server (Python, FastMCP) exposing map capabilities from Google Maps Platform
(Places, Routes, Geocoding, Address Validation), OpenStreetMap (Nominatim, Overpass),
OSS routing engines (OSRM, Valhalla, OpenRouteService, GraphHopper) and other open
geocoders/tiles (Photon, Pelias, static maps) behind one tool surface.

## Status
Planning. No server code yet. Backlog lives in GitHub Issues and the "maps-mcp Scrum
Board" project. Design questions live in GitHub Discussions.

## Stack
Python 3.11+, FastMCP, httpx, pydantic, pytest, ruff, mypy. Package manager: uv
(`brew install uv`). Docker is available for local Nominatim/OSRM/Valhalla.

Layout: `src/maps_mcp/` (package, src layout), `tests/`, `pyproject.toml` (build, ruff,
mypy and pytest config), `uv.lock` (committed). `.python-version` pins dev to 3.11, the
minimum supported version. FastMCP is not a dependency yet (version pending Discussion #94).

## Commands
- Install: `uv sync` (creates `.venv`, installs the project and the dev group)
- Lint: `uv run ruff check .` (add `--fix` to autofix)
- Format: `uv run ruff format .` (CI-style check: `uv run ruff format --check .`)
- Types: `uv run mypy` (strict, covers `src` and `tests`)
- Test: `uv run pytest`
- Run: `uv run maps-mcp` (or `uv run python -m maps_mcp`); prints the version until the
  stdio server lands
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
