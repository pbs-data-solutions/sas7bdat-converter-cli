# sas7bdat Converter CLI

[![Tests Status](https://github.com/pbs-data-solutions/sas7bdat-converter-cli/actions/workflows/testing.yaml/badge.svg?branch=main&event=push)](https://github.com/pbs-data-solutions/sas7bdat-converter-cli/actions?query=workflow%3ATesting+branch%3Amain+event%3Apush)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/pbs-data-solutions/sas7bdat-converter-cli/main.svg)](https://results.pre-commit.ci/latest/github/pbs-data-solutions/sas7bdat-converter-cli/main)
[![Coverage](https://codecov.io/github/pbs-data-solutions/sas7bdat-converter-cli/coverage.svg?branch=main)](https://codecov.io/gh/pbs-data-solutions/sas7bdat-converter-cli)
[![PyPI version](https://badge.fury.io/py/sas7bdat-converter-cli.svg)](https://badge.fury.io/py/sas7bdat-converter-cli)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sas7bdat-converter-cli?color=5cc141)](https://github.com/pbs-data-solutions/sas7bdat-converter-cli)

CLI to convert sas7bdat and xport files into other formats

## Installation

Installation with [pipx](https://github.com/pypa/pipx) is recommended.

```sh
pipx install sas7bdat-converter-cli
```

Alternatively sas7bdat Converter CLI can be installed with pip.

```sh
pip install sas7bdat-converter-cli
```

## Usage

```console
Usage: sas7bdat-converter [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version                   Show the installed version
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  dir-to-csv      Convert a directory containing sas7bdat or xpt files to...
  dir-to-excel    Convert a directory of sas7bdat or xpt files to xlsx...
  dir-to-json     Convert a directory of sas7bdat or xpt files to json...
  dir-to-xml      Convert a directory of sas7bdat or xpt files to xml files.
  to-csv          Convert a sas7bdat or xpt file to a csv file.
  to-excel        Convert a sas7bdat or xpt file to a xlsx file.
  to-json         Convert a sas7bdat or xpt file to a JSON file.
  to-xml          Convert a sas7bdat or xpt file to a xml file.
```

## Contributing

Contributions to this project are welcome. If you are interesting in contributing please see our
[contributing guide](CONTRIBUTING.md)
