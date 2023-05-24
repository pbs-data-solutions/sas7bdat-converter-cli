from pathlib import Path
from typing import Union

from sas7bdat_converter import dir_to_csv as converter_dir_to_csv
from sas7bdat_converter import to_csv as converter_to_csv
from typer import Argument, Exit, Option, Typer, echo

__version__ = "0.1.0"

app = Typer()


@app.command()
def to_csv(
    file_path: Path = Argument(..., help="Path to the file to convert", show_default=False),
    export_file: Path = Argument(..., help="Path to the new csv file", show_default=False),
) -> None:
    if file_path.suffix != ".sas7bdat" and file_path.suffix != ".xpt":
        exit("File must be either a sas7bdat file or an xpt file")

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
        help="Path to the directory to save the output files",
        show_default=False,
    ),
) -> None:
    export_path = output_dir or dir
    converter_dir_to_csv(dir_path=dir, export_path=export_path, continue_on_error=True)


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
