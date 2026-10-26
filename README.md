# maps-mcp

An [MCP](https://modelcontextprotocol.io) server that gives AI assistants map capabilities (geocoding, places, routing, distance matrices, isochrones and static maps) from several providers behind one coherent tool surface.

> **Status: planning.** No server code yet. The backlog is in [Issues](../../issues) and the design questions are in [Discussions](../../discussions).

## Planned provider coverage

| Area | Providers |
|---|---|
| Google Maps Platform | Places (New), Routes, Geocoding, Address Validation (later: Solar, Area Insights, Route Optimization, Isochrones) |
| OpenStreetMap | Nominatim (geocode, reverse, lookup), Overpass (POI and feature queries) |
| Open-source routing engines | OSRM, Valhalla, OpenRouteService, GraphHopper |
| Other open geocoders and tiles | Photon, Pelias, static map rendering |

## Approach

- **Stack:** Python and FastMCP.
- **One tool surface:** provider-agnostic tools (`geocode`, `search_places`, `get_directions`, ...) with an explicit `provider` option and configurable fallbacks. This is still an open design question, so join the discussion.
- **Policy-aware:** each adapter respects the provider's usage policy and terms (rate limits, caching, attribution).
- **Scrum, epics first:** work is organised as epics, stories and spikes. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Development

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/) (`brew install uv` on macOS, see the uv docs for other platforms).

```sh
uv sync                      # install the project and dev tools into .venv
uv run ruff check .          # lint (add --fix to autofix)
uv run ruff format .         # format
uv run mypy                  # type-check (strict)
uv run pytest                # tests
uv run maps-mcp              # run (prints the version until the stdio server lands)
```

Before opening a PR, make sure all of these are clean:

```sh
uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest
```

Add dependencies with `uv add <pkg>` (or `uv add --dev <pkg>`) and commit the updated `uv.lock`.

## Contributing

Start with [Discussions](../../discussions) for ideas and design questions, then pick up an issue labelled `ready`. Details are in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE). The licence choice is open for discussion before the first release.
