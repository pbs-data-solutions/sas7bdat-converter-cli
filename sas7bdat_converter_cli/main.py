from typing import Union

from typer import Exit, Option, Typer, echo

__version__ = "0.1.0"

app = Typer()


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
