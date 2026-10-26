# maps-mcp

An [MCP](https://modelcontextprotocol.io) server that gives AI assistants map capabilities (geocoding, places, routing, distance matrices, isochrones and static maps) from several providers behind one coherent tool surface.

> **Status: early development.** The server skeleton runs over stdio and streamable HTTP and exposes a `ping` tool. No provider adapters yet. The backlog is in [Issues](../../issues) and the design questions are in [Discussions](../../discussions).

## Planned provider coverage

| Area | Providers |
|---|---|
| Google Maps Platform | Places (New), Routes, Geocoding, Address Validation (later: Solar, Area Insights, Route Optimization, Isochrones) |
| OpenStreetMap | Nominatim (geocode, reverse, lookup), Overpass (POI and feature queries) |
| Open-source routing engines | OSRM, Valhalla, OpenRouteService, GraphHopper |
| Other open geocoders and tiles | Photon, Pelias, static map rendering |

## Approach

- **Stack:** Python 3.11+ and [FastMCP](https://gofastmcp.com) 4.1.4 (`fastmcp`, built on the official `mcp` Python SDK). Tools and provider calls are `async` throughout.
- **Transports:** stdio (default, for local MCP clients) and streamable HTTP (for remote use), both from the start.
- **One tool surface:** provider-agnostic tools (`geocode`, `search_places`, `get_directions`, ...) with an explicit `provider` option and configurable fallbacks. This is still an open design question, so join the discussion.
- **Policy-aware:** each adapter respects the provider's usage policy and terms (rate limits, caching, attribution).
- **Scrum, epics first:** work is organised as epics, stories and spikes. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Running the server

```sh
uv run maps-mcp                                      # stdio (default)
uv run maps-mcp --transport http                     # streamable HTTP on http://127.0.0.1:8000/mcp
uv run maps-mcp --transport http --host 0.0.0.0 --port 9000
uv run maps-mcp --version
```

| Option | Environment variable | Default | Notes |
|---|---|---|---|
| `--transport` | `MAPS_MCP_TRANSPORT` | `stdio` | `stdio`, `http` or `streamable-http` (the last two are the same) |
| `--host` | `MAPS_MCP_HOST` | `127.0.0.1` | HTTP only. Local only by default |
| `--port` | `MAPS_MCP_PORT` | `8000` | HTTP only |

Command-line options win over environment variables. The HTTP endpoint is served at `/mcp`.

> **Security:** the HTTP transport has no authentication yet (tracked in [#84](../../issues/84)). It binds to `127.0.0.1` by default. Do not expose it beyond localhost or a trusted network until auth lands.

### The `ping` tool

`ping` takes no arguments and returns the server version and the enabled providers, identically on both transports:

```json
{ "version": "0.1.0", "providers": [] }
```

`providers` is empty until the provider registry lands.

### Connecting MCP clients

Replace `/absolute/path/to/maps-mcp` with your checkout.

**Claude Code, stdio:**

```sh
claude mcp add maps-mcp -- uv run --directory /absolute/path/to/maps-mcp maps-mcp
```

**Claude Desktop, stdio** (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS). Claude Desktop does not inherit your shell `PATH`, so use the absolute path from `which uv`:

```json
{
  "mcpServers": {
    "maps-mcp": {
      "command": "/opt/homebrew/bin/uv",
      "args": ["run", "--directory", "/absolute/path/to/maps-mcp", "maps-mcp"]
    }
  }
}
```

**Claude Code, streamable HTTP** (start the server first with `uv run maps-mcp --transport http`):

```sh
claude mcp add --transport http maps-mcp http://127.0.0.1:8000/mcp
```

or in a project `.mcp.json`, here for a hosted deployment:

```json
{
  "mcpServers": {
    "maps-mcp": {
      "type": "http",
      "url": "https://maps-mcp.example.com/mcp"
    }
  }
}
```

**Claude Desktop, streamable HTTP:** add a remote server under Settings, Connectors, Add custom connector. That route goes through Anthropic's cloud, so the URL must be publicly reachable (and, until [#84](../../issues/84) lands, unauthenticated, so do not do this with real deployments yet). For a server on your own machine, bridge it to stdio with [`mcp-remote`](https://www.npmjs.com/package/mcp-remote):

```json
{
  "mcpServers": {
    "maps-mcp": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "http://127.0.0.1:8000/mcp"]
    }
  }
}
```

### MCP Inspector

```sh
# stdio: the Inspector launches the server itself
npx @modelcontextprotocol/inspector uv run maps-mcp

# streamable HTTP: start the server in one terminal ...
uv run maps-mcp --transport http
# ... then open the Inspector, pick "Streamable HTTP" and enter http://127.0.0.1:8000/mcp
npx @modelcontextprotocol/inspector
```

For a non-interactive check, use the Inspector CLI mode:

```sh
npx @modelcontextprotocol/inspector --cli .venv/bin/maps-mcp --method tools/call --tool-name ping
npx @modelcontextprotocol/inspector --cli http://127.0.0.1:8000/mcp --transport http --method tools/call --tool-name ping
```

## Development

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/) (`brew install uv` on macOS, see the uv docs for other platforms).

```sh
uv sync                      # install the project and dev tools into .venv
uv run ruff check .          # lint (add --fix to autofix)
uv run ruff format .         # format
uv run mypy                  # type-check (strict)
uv run pytest                # tests
uv run maps-mcp              # run over stdio (see "Running the server" for HTTP)
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
