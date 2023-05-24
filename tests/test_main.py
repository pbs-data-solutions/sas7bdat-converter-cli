from pathlib import Path

import pytest

from sas7bdat_converter_cli.main import __version__, app

try:
    import tomli as tomllib  # type: ignore
except ModuleNotFoundError:
    import tomllib  # type: ignore


def test_versions_match():
    pyproject_file = Path().absolute() / "pyproject.toml"
    with open(pyproject_file, "rb") as f:
        data = tomllib.load(f)
        pyproject_version = data["tool"]["poetry"]["version"]
    assert __version__ == pyproject_version


@pytest.mark.parametrize("args", [["--version"], ["-v"]])
def test_version(args, test_runner):
    result = test_runner.invoke(app, args, catch_exceptions=False)
    out = result.stdout
    assert __version__ in out
