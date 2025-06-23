import json
import shutil
import sys
from pathlib import Path

import pandas as pd
import pytest

from sas7bdat_converter_cli.main import __version__, app

if sys.version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib


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


@pytest.mark.parametrize(
    "fixture_name, expected_name",
    [("sas_file_1", "file1.csv"), ("sas_file_2", "file2.csv"), ("sas_file_3", "file3.csv")],
)
def test_to_csv_sas(fixture_name, expected_name, expected_dir, test_runner, tmp_path, request):
    sas_file = Path(request.getfixturevalue(fixture_name))
    converted_file = tmp_path / expected_name
    expected_file = expected_dir / expected_name
    args = ["to-csv", str(sas_file), str(converted_file)]
    test_runner.invoke(app, args, catch_exceptions=False)

    with open(expected_file) as f:
        expected = f.read().rstrip()

    with open(converted_file) as f:
        got = f.read().rstrip()

    assert got == expected


@pytest.mark.parametrize(
    "fixture_name, expected_name",
    [("xpt_file_1", "file1.csv"), ("xpt_file_2", "file2.csv")],
)
def test_to_csv_xpt(fixture_name, expected_name, xpt_expected_dir, test_runner, tmp_path, request):
    xpt_file = Path(request.getfixturevalue(fixture_name))
    converted_file = tmp_path / expected_name
    expected_file = xpt_expected_dir / expected_name
    args = ["to-csv", str(xpt_file), str(converted_file)]
    test_runner.invoke(app, args, catch_exceptions=False)

    with open(expected_file) as f:
        expected = f.read().rstrip()

    with open(converted_file) as f:
        got = f.read().rstrip()

    assert got == expected


def test_to_csv_invalid_extension(test_runner, tmp_path):
    bad = tmp_path / "bad.txt"
    converted_file = tmp_path / "test.csv"
    args = ["to-csv", str(bad), str(converted_file)]
    result = test_runner.invoke(app, args, catch_exceptions=False)
    out = result.stdout

    assert "File must be either a sas7bdat file or a xpt file" in out


def test_to_csv_invalid_output_extension(test_runner, tmp_path):
    sas_file = tmp_path / "file.sas7bdat"
    converted_file = tmp_path / "test.txt"
    args = ["to-csv", str(sas_file), str(converted_file)]
    result = test_runner.invoke(app, args, catch_exceptions=False)
    out = result.stdout

    assert "The export file must be a csv file" in out


@pytest.mark.parametrize("flag", ["--output-dir", "-o"])
def test_dir_to_csv_different_dir_sas(flag, sas7bdat_dir, test_runner, tmp_path):
    args = ["dir-to-csv", str(sas7bdat_dir), flag, str(tmp_path)]
    test_runner.invoke(app, args, catch_exceptions=False)
    sas_counter = len([name for name in sas7bdat_dir.iterdir() if name.suffix == ".sas7bdat"])
    convert_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".csv"])

    assert sas_counter == convert_counter


@pytest.mark.parametrize("flag", ["--output-dir", "-o"])
def test_dir_to_csv_different_dir_xpt(flag, xpt_dir, test_runner, tmp_path):
    args = ["dir-to-csv", str(xpt_dir), flag, str(tmp_path)]
    test_runner.invoke(app, args, catch_exceptions=False)
    sas_counter = len([name for name in xpt_dir.iterdir() if name.suffix == ".xpt"])
    convert_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".csv"])

    assert sas_counter == convert_counter


def test_dir_to_csv_same_dir_path_sas(sas7bdat_dir, test_runner, tmp_path):
    sas_files = [str(x) for x in sas7bdat_dir.iterdir()]
    for sas_file in sas_files:
        shutil.copy(sas_file, str(tmp_path))

    args = ["dir-to-csv", str(tmp_path)]
    test_runner.invoke(app, args, catch_exceptions=False)
    sas_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".sas7bdat"])
    convert_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".csv"])

    assert sas_counter == convert_counter


def test_dir_to_csv_same_dir_path_xpt(xpt_dir, test_runner, tmp_path):
    sas_files = [str(x) for x in xpt_dir.iterdir()]
    for sas_file in sas_files:
        shutil.copy(sas_file, str(tmp_path))

    args = ["dir-to-csv", str(tmp_path)]
    test_runner.invoke(app, args, catch_exceptions=False)
    sas_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".xpt"])
    convert_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".csv"])

    assert sas_counter == convert_counter


@pytest.mark.parametrize("continue_on_error", ["--continue-on-error", "-c"])
def test_dir_to_csv_continue(continue_on_error, test_runner, tmp_path, sas7bdat_dir, bad_sas_file):
    sas_files = [str(x) for x in sas7bdat_dir.iterdir()]
    for sas_file in sas_files:
        shutil.copy(sas_file, str(tmp_path))

    shutil.copy(bad_sas_file, str(tmp_path))

    args = ["dir-to-csv", str(tmp_path), continue_on_error]
    test_runner.invoke(app, args, catch_exceptions=False)

    sas_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".sas7bdat"]) - 1
    convert_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".csv"])

    assert sas_counter == convert_counter


@pytest.mark.parametrize(
    "fixture_name, expected_name",
    [("sas_file_1", "file1.xlsx"), ("sas_file_2", "file2.xlsx"), ("sas_file_3", "file3.xlsx")],
)
def test_to_excel_sas(fixture_name, expected_name, expected_dir, test_runner, tmp_path, request):
    sas_file = Path(request.getfixturevalue(fixture_name))
    converted_file = tmp_path / expected_name
    expected_file = expected_dir / expected_name
    args = ["to-excel", str(sas_file), str(converted_file)]
    test_runner.invoke(app, args, catch_exceptions=False)

    df_expected = pd.read_excel(expected_file, engine="openpyxl")
    df_converted = pd.read_excel(converted_file, engine="openpyxl")

    pd.testing.assert_frame_equal(df_expected, df_converted)


@pytest.mark.parametrize(
    "fixture_name, expected_name",
    [("xpt_file_1", "file1.xlsx"), ("xpt_file_2", "file2.xlsx")],
)
def test_to_excel_xpt(
    fixture_name, expected_name, xpt_expected_dir, test_runner, tmp_path, request
):
    xpt_file = Path(request.getfixturevalue(fixture_name))
    converted_file = tmp_path / expected_name
    expected_file = xpt_expected_dir / expected_name
    args = ["to-excel", str(xpt_file), str(converted_file)]
    test_runner.invoke(app, args, catch_exceptions=False)

    df_expected = pd.read_excel(expected_file, engine="openpyxl")
    df_converted = pd.read_excel(converted_file, engine="openpyxl")

    pd.testing.assert_frame_equal(df_expected, df_converted)


def test_to_excel_invalid_extension(test_runner, tmp_path):
    bad = tmp_path / "bad.txt"
    converted_file = tmp_path / "test.xlsx"
    args = ["to-excel", str(bad), str(converted_file)]
    result = test_runner.invoke(app, args, catch_exceptions=False)
    out = result.stdout

    assert "File must be either a sas7bdat file or a xpt file" in out


def test_to_excel_invalid_output_extension(test_runner, tmp_path):
    sas_file = tmp_path / "file.sas7bdat"
    converted_file = tmp_path / "test.txt"
    args = ["to-excel", str(sas_file), str(converted_file)]
    result = test_runner.invoke(app, args, catch_exceptions=False)
    out = result.stdout

    assert "The export file must be a xlsx file" in out


@pytest.mark.parametrize("flag", ["--output-dir", "-o"])
def test_dir_to_excel_different_dir_sas(flag, sas7bdat_dir, test_runner, tmp_path):
    args = ["dir-to-excel", str(sas7bdat_dir), flag, str(tmp_path)]
    test_runner.invoke(app, args, catch_exceptions=False)
    sas_counter = len([name for name in sas7bdat_dir.iterdir() if name.suffix == ".sas7bdat"])
    convert_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".xlsx"])

    assert sas_counter == convert_counter


@pytest.mark.parametrize("flag", ["--output-dir", "-o"])
def test_dir_to_excel_different_dir_xpt(flag, xpt_dir, test_runner, tmp_path):
    args = ["dir-to-excel", str(xpt_dir), flag, str(tmp_path)]
    test_runner.invoke(app, args, catch_exceptions=False)
    sas_counter = len([name for name in xpt_dir.iterdir() if name.suffix == ".xpt"])
    convert_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".xlsx"])

    assert sas_counter == convert_counter


def test_dir_to_excel_same_dir_path_sas(sas7bdat_dir, test_runner, tmp_path):
    sas_files = [str(x) for x in sas7bdat_dir.iterdir()]
    for sas_file in sas_files:
        shutil.copy(sas_file, str(tmp_path))

    args = ["dir-to-excel", str(tmp_path)]
    test_runner.invoke(app, args, catch_exceptions=False)
    sas_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".sas7bdat"])
    convert_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".xlsx"])

    assert sas_counter == convert_counter


def test_dir_to_excel_same_dir_path_xpt(xpt_dir, test_runner, tmp_path):
    sas_files = [str(x) for x in xpt_dir.iterdir()]
    for sas_file in sas_files:
        shutil.copy(sas_file, str(tmp_path))

    args = ["dir-to-excel", str(tmp_path)]
    test_runner.invoke(app, args, catch_exceptions=False)
    sas_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".xpt"])
    convert_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".xlsx"])

    assert sas_counter == convert_counter


@pytest.mark.parametrize("continue_on_error", ["--continue-on-error", "-c"])
def test_dir_to_excel_continue(
    continue_on_error, test_runner, tmp_path, sas7bdat_dir, bad_sas_file
):
    sas_files = [str(x) for x in sas7bdat_dir.iterdir()]
    for sas_file in sas_files:
        shutil.copy(sas_file, str(tmp_path))

    shutil.copy(bad_sas_file, str(tmp_path))

    args = ["dir-to-excel", str(tmp_path), continue_on_error]
    test_runner.invoke(app, args, catch_exceptions=False)

    sas_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".sas7bdat"]) - 1
    convert_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".xlsx"])

    assert sas_counter == convert_counter


@pytest.mark.parametrize(
    "fixture_name, expected_name",
    [("sas_file_1", "file1.json"), ("sas_file_2", "file2.json"), ("sas_file_3", "file3.json")],
)
def test_to_json_sas(fixture_name, expected_name, expected_dir, test_runner, tmp_path, request):
    sas_file = Path(request.getfixturevalue(fixture_name))
    converted_file = tmp_path / expected_name
    expected_file = expected_dir / expected_name
    args = ["to-json", str(sas_file), str(converted_file)]
    test_runner.invoke(app, args, catch_exceptions=False)

    with open(expected_file) as f:
        expected = json.load(f)

    with open(converted_file) as f:
        got = json.load(f)

    assert got == expected


@pytest.mark.parametrize(
    "fixture_name, expected_name",
    [("xpt_file_1", "file1.json"), ("xpt_file_2", "file2.json")],
)
def test_to_json_xpt(fixture_name, expected_name, xpt_expected_dir, test_runner, tmp_path, request):
    xpt_file = Path(request.getfixturevalue(fixture_name))
    converted_file = tmp_path / expected_name
    expected_file = xpt_expected_dir / expected_name
    args = ["to-json", str(xpt_file), str(converted_file)]
    test_runner.invoke(app, args, catch_exceptions=False)

    with open(expected_file) as f:
        expected = json.load(f)

    with open(converted_file) as f:
        got = json.load(f)

    assert got == expected


def test_to_json_invalid_extension(test_runner, tmp_path):
    bad = tmp_path / "bad.txt"
    converted_file = tmp_path / "test.json"
    args = ["to-json", str(bad), str(converted_file)]
    result = test_runner.invoke(app, args, catch_exceptions=False)
    out = result.stdout

    assert "File must be either a sas7bdat file or a xpt file" in out


def test_to_json_invalid_output_extension(test_runner, tmp_path):
    sas_file = tmp_path / "file.sas7bdat"
    converted_file = tmp_path / "test.txt"
    args = ["to-json", str(sas_file), str(converted_file)]
    result = test_runner.invoke(app, args, catch_exceptions=False)
    out = result.stdout

    assert "The export file must be a json file" in out


@pytest.mark.parametrize("flag", ["--output-dir", "-o"])
def test_dir_to_json_different_dir_sas(flag, sas7bdat_dir, test_runner, tmp_path):
    args = ["dir-to-json", str(sas7bdat_dir), flag, str(tmp_path)]
    test_runner.invoke(app, args, catch_exceptions=False)
    sas_counter = len([name for name in sas7bdat_dir.iterdir() if name.suffix == ".sas7bdat"])
    convert_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".json"])

    assert sas_counter == convert_counter


@pytest.mark.parametrize("flag", ["--output-dir", "-o"])
def test_dir_to_json_different_dir_xpt(flag, xpt_dir, test_runner, tmp_path):
    args = ["dir-to-json", str(xpt_dir), flag, str(tmp_path)]
    test_runner.invoke(app, args, catch_exceptions=False)
    sas_counter = len([name for name in xpt_dir.iterdir() if name.suffix == ".xpt"])
    convert_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".json"])

    assert sas_counter == convert_counter


def test_dir_to_json_same_dir_path_sas(sas7bdat_dir, test_runner, tmp_path):
    sas_files = [str(x) for x in sas7bdat_dir.iterdir()]
    for sas_file in sas_files:
        shutil.copy(sas_file, str(tmp_path))

    args = ["dir-to-json", str(tmp_path)]
    test_runner.invoke(app, args, catch_exceptions=False)
    sas_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".sas7bdat"])
    convert_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".json"])

    assert sas_counter == convert_counter


def test_dir_to_json_same_dir_path_xpt(xpt_dir, test_runner, tmp_path):
    sas_files = [str(x) for x in xpt_dir.iterdir()]
    for sas_file in sas_files:
        shutil.copy(sas_file, str(tmp_path))

    args = ["dir-to-json", str(tmp_path)]
    test_runner.invoke(app, args, catch_exceptions=False)
    sas_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".xpt"])
    convert_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".json"])

    assert sas_counter == convert_counter


@pytest.mark.parametrize("continue_on_error", ["--continue-on-error", "-c"])
def test_dir_to_json_continue(continue_on_error, test_runner, tmp_path, sas7bdat_dir, bad_sas_file):
    sas_files = [str(x) for x in sas7bdat_dir.iterdir()]
    for sas_file in sas_files:
        shutil.copy(sas_file, str(tmp_path))

    shutil.copy(bad_sas_file, str(tmp_path))

    args = ["dir-to-json", str(tmp_path), continue_on_error]
    test_runner.invoke(app, args, catch_exceptions=False)

    sas_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".sas7bdat"]) - 1
    convert_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".json"])

    assert sas_counter == convert_counter


@pytest.mark.parametrize(
    "fixture_name, expected_name",
    [("sas_file_1", "file1.xml"), ("sas_file_2", "file2.xml"), ("sas_file_3", "file3.xml")],
)
def test_to_xml_sas(fixture_name, expected_name, expected_dir, test_runner, tmp_path, request):
    sas_file = Path(request.getfixturevalue(fixture_name))
    converted_file = tmp_path / expected_name
    expected_file = expected_dir / expected_name
    args = ["to-xml", str(sas_file), str(converted_file)]
    test_runner.invoke(app, args, catch_exceptions=False)

    with open(expected_file) as f:
        expected = f.read().rstrip()

    with open(converted_file) as f:
        got = f.read().rstrip()

    assert got == expected


@pytest.mark.parametrize(
    "fixture_name, expected_name",
    [("xpt_file_1", "file1.xml"), ("xpt_file_2", "file2.xml")],
)
def test_to_xml_xpt(fixture_name, expected_name, xpt_expected_dir, test_runner, tmp_path, request):
    xpt_file = Path(request.getfixturevalue(fixture_name))
    converted_file = tmp_path / expected_name
    expected_file = xpt_expected_dir / expected_name
    args = ["to-xml", str(xpt_file), str(converted_file)]
    test_runner.invoke(app, args, catch_exceptions=False)

    with open(expected_file) as f:
        expected = f.read().rstrip()

    with open(converted_file) as f:
        got = f.read().rstrip()

    assert got == expected


def test_to_xml_invalid_extension(test_runner, tmp_path):
    bad = tmp_path / "bad.txt"
    converted_file = tmp_path / "test.xml"
    args = ["to-xml", str(bad), str(converted_file)]
    result = test_runner.invoke(app, args, catch_exceptions=False)
    out = result.stdout

    assert "File must be either a sas7bdat file or a xpt file" in out


def test_to_xml_invalid_output_extension(test_runner, tmp_path):
    sas_file = tmp_path / "file.sas7bdat"
    converted_file = tmp_path / "test.txt"
    args = ["to-xml", str(sas_file), str(converted_file)]
    result = test_runner.invoke(app, args, catch_exceptions=False)
    out = result.stdout

    assert "The export file must be a XML file" in out


@pytest.mark.parametrize("flag", ["--output-dir", "-o"])
def test_dir_to_xml_different_dir_sas(flag, sas7bdat_dir, test_runner, tmp_path):
    args = ["dir-to-xml", str(sas7bdat_dir), flag, str(tmp_path)]
    test_runner.invoke(app, args, catch_exceptions=False)
    sas_counter = len([name for name in sas7bdat_dir.iterdir() if name.suffix == ".sas7bdat"])
    convert_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".xml"])

    assert sas_counter == convert_counter


@pytest.mark.parametrize("flag", ["--output-dir", "-o"])
def test_dir_to_xml_different_dir_xpt(flag, xpt_dir, test_runner, tmp_path):
    args = ["dir-to-xml", str(xpt_dir), flag, str(tmp_path)]
    test_runner.invoke(app, args, catch_exceptions=False)
    sas_counter = len([name for name in xpt_dir.iterdir() if name.suffix == ".xpt"])
    convert_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".xml"])

    assert sas_counter == convert_counter


def test_dir_to_xml_same_dir_path_sas(sas7bdat_dir, test_runner, tmp_path):
    sas_files = [str(x) for x in sas7bdat_dir.iterdir()]
    for sas_file in sas_files:
        shutil.copy(sas_file, str(tmp_path))

    args = ["dir-to-xml", str(tmp_path)]
    test_runner.invoke(app, args, catch_exceptions=False)
    sas_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".sas7bdat"])
    convert_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".xml"])

    assert sas_counter == convert_counter


def test_dir_to_xml_same_dir_path_xpt(xpt_dir, test_runner, tmp_path):
    sas_files = [str(x) for x in xpt_dir.iterdir()]
    for sas_file in sas_files:
        shutil.copy(sas_file, str(tmp_path))

    args = ["dir-to-xml", str(tmp_path)]
    test_runner.invoke(app, args, catch_exceptions=False)
    sas_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".xpt"])
    convert_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".xml"])

    assert sas_counter == convert_counter


@pytest.mark.parametrize("continue_on_error", ["--continue-on-error", "-c"])
def test_dir_to_xml_continue(continue_on_error, test_runner, tmp_path, sas7bdat_dir, bad_sas_file):
    sas_files = [str(x) for x in sas7bdat_dir.iterdir()]
    for sas_file in sas_files:
        shutil.copy(sas_file, str(tmp_path))

    shutil.copy(bad_sas_file, str(tmp_path))

    args = ["dir-to-xml", str(tmp_path), continue_on_error]
    test_runner.invoke(app, args, catch_exceptions=False)

    sas_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".sas7bdat"]) - 1
    convert_counter = len([name for name in tmp_path.iterdir() if name.suffix == ".xml"])

    assert sas_counter == convert_counter
