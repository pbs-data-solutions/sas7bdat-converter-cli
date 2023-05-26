from pathlib import Path
from typing import Union

from rich.console import Console
from sas7bdat_converter import dir_to_csv as converter_dir_to_csv
from sas7bdat_converter import dir_to_excel as converter_dir_to_excel
from sas7bdat_converter import dir_to_json as converter_dir_to_json
from sas7bdat_converter import dir_to_parquet as converter_dir_to_parquet
from sas7bdat_converter import dir_to_xml as converter_dir_to_xml
from sas7bdat_converter import to_csv as converter_to_csv
from sas7bdat_converter import to_excel as converter_to_excel
from sas7bdat_converter import to_json as converter_to_json
from sas7bdat_converter import to_parquet as converter_to_parquet
from sas7bdat_converter import to_xml as converter_to_xml
from typer import Argument, Exit, Option, Typer, echo

__version__ = "1.0.0"

app = Typer()
console = Console()


@app.command()
def to_csv(
    file_path: Path = Argument(..., help="Path to the file to convert", show_default=False),
    export_file: Path = Argument(..., help="Path to the new csv file", show_default=False),
) -> None:
    """Convert a sas7bdat or xpt file to a csv file."""
    with console.status("Converting file..."):
        if file_path.suffix != ".sas7bdat" and file_path.suffix != ".xpt":
            exit("File must be either a sas7bdat file or a xpt file")

        if export_file.suffix != ".csv":
            exit("The export file must be a csv file")

        converter_to_csv(sas7bdat_file=file_path, export_file=export_file)


@app.command()
def dir_to_csv(
    dir: Path = Argument(
        ..., help="Path to the directory to convert", exists=True, show_default=False
    ),
    output_dir: Union[Path, None] = Option(
        None,
        "--output-dir",
        "-o",
        help="Path to the directory to save the output files. Default = The same directory as dir",
        show_default=False,
    ),
    continue_on_error: bool = Option(
        False,
        "--continue-on-error",
        "-c",
        help="If set conversion will continue after failures",
    ),
    verbose: bool = Option(
        False, "--verbose", "-v", help="If set the amount of information printed is increased."
    ),
) -> None:
    """Convert a directory containing sas7bdat or xpt files to csv files."""
    with console.status("Converting files..."):
        export_path = output_dir or dir
        converter_dir_to_csv(
            dir_path=dir,
            export_path=export_path,
            continue_on_error=continue_on_error,
            verbose=verbose,
        )


@app.command()
def to_excel(
    file_path: Path = Argument(..., help="Path to the file to convert", show_default=False),
    export_file: Path = Argument(..., help="Path to the new Excel file", show_default=False),
) -> None:
    """Convert a sas7bdat or xpt file to a xlsx file."""
    with console.status("Converting file..."):
        if file_path.suffix != ".sas7bdat" and file_path.suffix != ".xpt":
            exit("File must be either a sas7bdat file or a xpt file")

        if export_file.suffix != ".xlsx":
            exit("The export file must be a xlsx file")

        converter_to_excel(sas7bdat_file=file_path, export_file=export_file)


@app.command()
def dir_to_excel(
    dir: Path = Argument(
        ..., help="Path to the directory to convert", exists=True, show_default=False
    ),
    output_dir: Union[Path, None] = Option(
        None,
        "--output-dir",
        "-o",
        help="Path to the directory to save the output files. Default = The same directory as dir",
        show_default=False,
    ),
    continue_on_error: bool = Option(
        False,
        "--continue-on-error",
        "-c",
        help="If set conversion will continue after failures",
    ),
    verbose: bool = Option(
        False, "--verbose", "-v", help="If set the amount of information printed is increased."
    ),
) -> None:
    """Convert a directory of sas7bdat or xpt files to xlsx files."""
    with console.status("Converting files..."):
        export_path = output_dir or dir
        converter_dir_to_excel(
            dir_path=dir,
            export_path=export_path,
            continue_on_error=continue_on_error,
            verbose=verbose,
        )


@app.command()
def to_json(
    file_path: Path = Argument(..., help="Path to the file to convert", show_default=False),
    export_file: Path = Argument(..., help="Path to the new JSON file", show_default=False),
) -> None:
    """Convert a sas7bdat or xpt file to a JSON file."""
    with console.status("Converting file..."):
        if file_path.suffix != ".sas7bdat" and file_path.suffix != ".xpt":
            exit("File must be either a sas7bdat file or a xpt file")

        if export_file.suffix != ".json":
            exit("The export file must be a json file")

        converter_to_json(sas7bdat_file=file_path, export_file=export_file)


@app.command()
def dir_to_json(
    dir: Path = Argument(
        ..., help="Path to the directory to convert", exists=True, show_default=False
    ),
    output_dir: Union[Path, None] = Option(
        None,
        "--output-dir",
        "-o",
        help="Path to the directory to save the output files. Default = The same directory as dir",
        show_default=False,
    ),
    continue_on_error: bool = Option(
        False,
        "--continue-on-error",
        "-c",
        help="If set conversion will continue after failures",
    ),
    verbose: bool = Option(
        False, "--verbose", "-v", help="If set the amount of information printed is increased."
    ),
) -> None:
    """Convert a directory of sas7bdat or xpt files to json files."""
    with console.status("Converting files..."):
        export_path = output_dir or dir
        converter_dir_to_json(
            dir_path=dir,
            export_path=export_path,
            continue_on_error=continue_on_error,
            verbose=verbose,
        )


@app.command()
def to_parquet(
    file_path: Path = Argument(..., help="Path to the file to convert", show_default=False),
    export_file: Path = Argument(..., help="Path to the new parquet file", show_default=False),
) -> None:
    """Convert a sas7bdat or xpt file to a parquet file."""
    with console.status("Converting file..."):
        if file_path.suffix != ".sas7bdat" and file_path.suffix != ".xpt":
            exit("File must be either a sas7bdat file or a xpt file")

        if export_file.suffix != ".parquet":
            exit("The export file must be a parquet file")

        converter_to_parquet(sas7bdat_file=file_path, export_file=export_file)


@app.command()
def dir_to_parquet(
    dir: Path = Argument(
        ..., help="Path to the directory to convert", exists=True, show_default=False
    ),
    output_dir: Union[Path, None] = Option(
        None,
        "--output-dir",
        "-o",
        help="Path to the directory to save the output files. Default = The same directory as dir",
        show_default=False,
    ),
    continue_on_error: bool = Option(
        False,
        "--continue-on-error",
        "-c",
        help="If set conversion will continue after failures",
    ),
    verbose: bool = Option(
        False, "--verbose", "-v", help="If set the amount of information printed is increased."
    ),
) -> None:
    """Convert a directory of sas7bdat or xpt files to parquet files."""
    with console.status("Converting files..."):
        export_path = output_dir or dir
        converter_dir_to_parquet(
            dir_path=dir,
            export_path=export_path,
            continue_on_error=continue_on_error,
            verbose=verbose,
        )


@app.command()
def to_xml(
    file_path: Path = Argument(..., help="Path to the file to convert", show_default=False),
    export_file: Path = Argument(..., help="Path to the new XML file", show_default=False),
) -> None:
    """Convert a sas7bdat or xpt file to a xml file."""
    with console.status("Converting file..."):
        if file_path.suffix != ".sas7bdat" and file_path.suffix != ".xpt":
            exit("File must be either a sas7bdat file or a xpt file")

        if export_file.suffix != ".xml":
            exit("The export file must be a XML file")

        converter_to_xml(sas7bdat_file=file_path, export_file=export_file)


@app.command()
def dir_to_xml(
    dir: Path = Argument(
        ..., help="Path to the directory to convert", exists=True, show_default=False
    ),
    output_dir: Union[Path, None] = Option(
        None,
        "--output-dir",
        "-o",
        help="Path to the directory to save the output files. Default = The same directory as dir",
        show_default=False,
    ),
    continue_on_error: bool = Option(
        False,
        "--continue-on-error",
        "-c",
        help="If set conversion will continue after failures",
    ),
    verbose: bool = Option(
        False, "--verbose", "-v", help="If set the amount of information printed is increased."
    ),
) -> None:
    """Convert a directory of sas7bdat or xpt files to xml files."""
    with console.status("Converting files..."):
        export_path = output_dir or dir
        converter_dir_to_xml(
            dir_path=dir,
            export_path=export_path,
            continue_on_error=continue_on_error,
            verbose=verbose,
        )


@app.callback(invoke_without_command=True)
def main(
    version: Union[bool, None] = Option(
        None,
        "--version",
        "-v",
        is_eager=True,
        help="Show the installed version",
    ),
) -> None:
    if version:
        echo(__version__)
        raise Exit()


if __name__ == "__main__":
    app()
