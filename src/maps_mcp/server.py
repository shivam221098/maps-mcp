from collections.abc import Sequence

from fastmcp import FastMCP
from pydantic import BaseModel

from maps_mcp import __version__

SERVER_NAME = "maps-mcp"


class PingResult(BaseModel):
    version: str
    providers: list[str]


def create_server(providers: Sequence[str] = ()) -> FastMCP:
    server = FastMCP(SERVER_NAME, version=__version__)
    enabled = list(providers)

    @server.tool
    async def ping() -> PingResult:
        """Check that the server is up. Returns the server version and the enabled providers."""
        return PingResult(version=__version__, providers=list(enabled))

    return server
