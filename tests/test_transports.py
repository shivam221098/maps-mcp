import os
import socket
import subprocess
import sys
import time
from collections.abc import Iterator

import pytest
from fastmcp import Client
from fastmcp.client.transports import StdioTransport, StreamableHttpTransport

import maps_mcp

pytestmark = pytest.mark.anyio

EXPECTED_PING = {"version": maps_mcp.__version__, "providers": []}


def _clean_env() -> dict[str, str]:
    return {k: v for k, v in os.environ.items() if not k.startswith("MAPS_MCP_")}


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _wait_for_port(port: int, process: subprocess.Popen[bytes], timeout: float = 20.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            pytest.fail(f"server exited early with code {process.returncode}")
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                return
        except OSError:
            time.sleep(0.1)
    pytest.fail(f"server did not start listening on port {port} within {timeout}s")


@pytest.fixture
def http_url() -> Iterator[str]:
    port = _free_port()
    process = subprocess.Popen(
        [sys.executable, "-m", "maps_mcp", "--transport", "http", "--port", str(port)],
        env=_clean_env(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_for_port(port, process)
        yield f"http://127.0.0.1:{port}/mcp"
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


async def test_ping_over_stdio() -> None:
    transport = StdioTransport(command=sys.executable, args=["-m", "maps_mcp"], env=_clean_env())

    async with Client(transport) as client:
        result = await client.call_tool("ping")

    assert result.structured_content == EXPECTED_PING


async def test_ping_over_streamable_http(http_url: str) -> None:
    async with Client(StreamableHttpTransport(http_url)) as client:
        result = await client.call_tool("ping")

    assert result.structured_content == EXPECTED_PING


async def test_stdio_is_the_default_transport() -> None:
    transport = StdioTransport(command=sys.executable, args=["-m", "maps_mcp"], env=_clean_env())

    async with Client(transport) as client:
        tools = await client.list_tools()

    assert [tool.name for tool in tools] == ["ping"]
