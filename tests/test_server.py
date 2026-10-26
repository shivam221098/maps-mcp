import inspect

import pytest
from fastmcp import Client
from fastmcp.tools import FunctionTool

import maps_mcp
from maps_mcp.server import create_server

pytestmark = pytest.mark.anyio


async def test_ping_returns_version_and_no_providers_by_default() -> None:
    async with Client(create_server()) as client:
        result = await client.call_tool("ping")

    assert result.structured_content == {"version": maps_mcp.__version__, "providers": []}


async def test_ping_reports_enabled_providers() -> None:
    async with Client(create_server(providers=["nominatim", "osrm"])) as client:
        result = await client.call_tool("ping")

    assert result.structured_content == {
        "version": maps_mcp.__version__,
        "providers": ["nominatim", "osrm"],
    }


async def test_ping_is_async() -> None:
    tool = await create_server().get_tool("ping")

    assert isinstance(tool, FunctionTool)
    assert inspect.iscoroutinefunction(tool.fn)


async def test_ping_is_the_only_tool() -> None:
    async with Client(create_server()) as client:
        tools = await client.list_tools()

    assert [tool.name for tool in tools] == ["ping"]
