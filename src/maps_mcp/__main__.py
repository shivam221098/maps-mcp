import argparse
import os
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Literal

from maps_mcp import __version__
from maps_mcp.server import create_server

Transport = Literal["stdio", "http"]

TRANSPORTS: dict[str, Transport] = {
    "stdio": "stdio",
    "http": "http",
    "streamable-http": "http",
}
DEFAULT_TRANSPORT = "stdio"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000


@dataclass(frozen=True)
class Settings:
    transport: Transport
    host: str
    port: int


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="maps-mcp",
        description="MCP server for map capabilities. Defaults to stdio for local MCP clients.",
        epilog=(
            "Each option can also be set with an environment variable: "
            "MAPS_MCP_TRANSPORT, MAPS_MCP_HOST, MAPS_MCP_PORT. Command-line options win."
        ),
    )
    parser.add_argument("--version", action="version", version=f"maps-mcp {__version__}")
    parser.add_argument(
        "--transport",
        help=f"One of: {', '.join(TRANSPORTS)} ('http' and 'streamable-http' are the same). "
        f"Default: {DEFAULT_TRANSPORT}.",
    )
    parser.add_argument(
        "--host", help=f"Bind address for HTTP (default: {DEFAULT_HOST}, local only)."
    )
    parser.add_argument("--port", help=f"Port for HTTP (default: {DEFAULT_PORT}).")
    return parser


def parse_settings(
    argv: Sequence[str] | None = None, env: Mapping[str, str] | None = None
) -> Settings:
    env = os.environ if env is None else env
    parser = _build_parser()
    args = parser.parse_args(argv)

    raw_transport = args.transport or env.get("MAPS_MCP_TRANSPORT") or DEFAULT_TRANSPORT
    transport = TRANSPORTS.get(raw_transport)
    if transport is None:
        parser.error(f"invalid transport {raw_transport!r}, choose from: {', '.join(TRANSPORTS)}")

    host = args.host or env.get("MAPS_MCP_HOST") or DEFAULT_HOST

    raw_port = args.port or env.get("MAPS_MCP_PORT") or str(DEFAULT_PORT)
    try:
        port = int(raw_port)
    except ValueError:
        parser.error(f"invalid port {raw_port!r}, expected an integer between 1 and 65535")
    if not 1 <= port <= 65535:
        parser.error(f"invalid port {port}, expected an integer between 1 and 65535")

    return Settings(transport=transport, host=host, port=port)


def main(argv: Sequence[str] | None = None) -> None:
    settings = parse_settings(argv)
    server = create_server()
    if settings.transport == "stdio":
        server.run(transport="stdio", show_banner=False)
    else:
        server.run(transport="http", host=settings.host, port=settings.port, show_banner=False)


if __name__ == "__main__":
    main()
