import pytest

import maps_mcp
from maps_mcp.__main__ import main


def test_version_is_exposed() -> None:
    assert maps_mcp.__version__


def test_main_prints_version(capsys: pytest.CaptureFixture[str]) -> None:
    main()
    assert capsys.readouterr().out.strip() == f"maps-mcp {maps_mcp.__version__}"
