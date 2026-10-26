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

## Contributing

Start with [Discussions](../../discussions) for ideas and design questions, then pick up an issue labelled `ready`. Details are in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE). The licence choice is open for discussion before the first release.
