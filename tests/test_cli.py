from typing import Any

import pytest

import maps_mcp
from maps_mcp import __main__ as cli
from maps_mcp.__main__ import Settings, parse_settings


def test_defaults_are_stdio_on_localhost() -> None:
    assert parse_settings([], env={}) == Settings(transport="stdio", host="127.0.0.1", port=8000)


def test_environment_variables_configure_http() -> None:
    env = {"MAPS_MCP_TRANSPORT": "http", "MAPS_MCP_HOST": "0.0.0.0", "MAPS_MCP_PORT": "9000"}

    assert parse_settings([], env=env) == Settings(transport="http", host="0.0.0.0", port=9000)


def test_command_line_overrides_environment() -> None:
    env = {"MAPS_MCP_TRANSPORT": "stdio", "MAPS_MCP_HOST": "0.0.0.0", "MAPS_MCP_PORT": "9000"}
    argv = ["--transport", "http", "--host", "127.0.0.2", "--port", "9100"]

    assert parse_settings(argv, env=env) == Settings(transport="http", host="127.0.0.2", port=9100)


def test_streamable_http_is_an_alias_for_http() -> None:
    assert parse_settings(["--transport", "streamable-http"], env={}).transport == "http"


def test_invalid_transport_is_rejected(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        parse_settings(["--transport", "carrier-pigeon"], env={})

    assert exc_info.value.code == 2
    assert "invalid transport 'carrier-pigeon'" in capsys.readouterr().err


def test_invalid_transport_from_environment_is_rejected() -> None:
    with pytest.raises(SystemExit):
        parse_settings([], env={"MAPS_MCP_TRANSPORT": "sse"})


@pytest.mark.parametrize("port", ["abc", "0", "65536", "-1"])
def test_invalid_port_is_rejected(port: str) -> None:
    with pytest.raises(SystemExit) as exc_info:
        parse_settings(["--port", port], env={})

    assert exc_info.value.code == 2


def test_version_flag_prints_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        parse_settings(["--version"], env={})

    assert exc_info.value.code == 0
    assert capsys.readouterr().out.strip() == f"maps-mcp {maps_mcp.__version__}"


class _RecordingServer:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def run(self, **kwargs: Any) -> None:
        self.calls.append(kwargs)


@pytest.fixture
def recording_server(monkeypatch: pytest.MonkeyPatch) -> _RecordingServer:
    for name in ("MAPS_MCP_TRANSPORT", "MAPS_MCP_HOST", "MAPS_MCP_PORT"):
        monkeypatch.delenv(name, raising=False)
    server = _RecordingServer()
    monkeypatch.setattr(cli, "create_server", lambda: server)
    return server


def test_main_runs_stdio_by_default(recording_server: _RecordingServer) -> None:
    cli.main([])

    assert recording_server.calls == [{"transport": "stdio", "show_banner": False}]


def test_main_runs_http_with_host_and_port(recording_server: _RecordingServer) -> None:
    cli.main(["--transport", "http", "--host", "0.0.0.0", "--port", "9000"])

    assert recording_server.calls == [
        {"transport": "http", "host": "0.0.0.0", "port": 9000, "show_banner": False}
    ]
