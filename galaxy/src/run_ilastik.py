#!/usr/bin/env python
"""
Small helper tool to run ilastik with a configuration file
"""
from pathlib import Path
from typing import Dict
import json
import logging
import platform
import subprocess
import sys

import click
import yaml


logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger()


class IlastikError(Exception):
    pass


class CMDPreconditionError(IlastikError):
    pass


class CFGFileError(IlastikError):
    pass


class DefaultFromContextObj(click.Option):
    def get_default(self, ctx):
        """
        Override default value lookup to first check in context object

        Can be used to with a pre-configured context object.
        See implementation of cli
        """
        self.default = ctx.obj.get(self.name, None)

        return super().get_default(ctx)


class PathlibPath(click.Path):
    def convert(self, value, param, ctx):
        return Path(super().convert(value, param, ctx))


def read_config(config_file: Path) -> Dict[str, str]:
    with open(config_file, "r") as f:
        if config_file.suffix in [".json"]:
            opts = json.load(f)
        elif config_file.suffix in [".yaml", ".yml"]:
            opts = yaml.safe_load(opts)
        else:
            raise CFGFileError("Supplied --config_file type not understood. Expected .yaml/.yml, or .json")
    return opts


@click.group()
@click.option(
    "--verbose/--no-verbose",
    help="Show output related to ilastik startup.",
    default=False,
)
@click.option("--debug/--no-debug", help="Run ilastik in debug mode.", default=False)
@click.option(
    "--config_file",
    type=PathlibPath(exists=True),
    help="json/yaml config file with key-value pairs that match the commands options.",
)
@click.pass_context
def main(ctx, verbose, debug, config_file=None):
    """
    Run ilastik in headless mode with pre-trained projects

    see the subcommand --help for a list of options.
    Note, these options can be either defined via the respective command line option
    (highest priority), an environment variable (COMMAND_LINE_OPTION_IN_UPPER-CASE),
    or the config file.
    """
    if verbose:
        logger.setLevel(logging.DEBUG)
    ctx.obj = {"debug": False}
    if config_file:
        try:
            config_options = read_config(config_file)
        except CFGFileError as e:
            raise click.BadParameter(e)

        # ctx.obj is used to determine values for arguments supplied
        # in the config file
        ctx.obj.update(config_options)
    if debug:
        ctx.obj["debug"] = True


_EXE_LOCATIONS = {
    "Linux": "/path/to/ilastik-1.x.y-Linux/run_ilastik.sh",
    "Darwin": "/path/to/ilastik-1.x.y-OSX.app",
    "Windows": '"C:\\Program Files\\ilastik-1.x.y-win64\\ilastik.exe"',
}

_EXE_MESSAGE = f"Path to ilastik executable, e.g. {_EXE_LOCATIONS.get(platform.system(), 'warning: no default location for system could be determined.')}"


@main.command("pixel_classification")
@click.option(
    "--ilastik_exe",
    help=_EXE_MESSAGE,
    type=PathlibPath(exists=True),
    required=True,
    cls=DefaultFromContextObj,
)
@click.option(
    "--project", required=True, type=PathlibPath(exists=True), cls=DefaultFromContextObj
)
@click.option(
    "--raw_data",
    required=True,
    type=PathlibPath(exists=True),
    cls=DefaultFromContextObj,
)
@click.option("--output_filename_format", required=True, cls=DefaultFromContextObj)
@click.option("--input_axes", required=False, cls=DefaultFromContextObj)
@click.option("--output_filename_format", required=False, cls=DefaultFromContextObj)
@click.option("--cutout_subregion", required=False, cls=DefaultFromContextObj)
@click.pass_context
def run_headless_pixel_classification(
    ctx,
    ilastik_exe: Path,
    project: Path,
    raw_data: Path,
    output_filename_format: str,
    input_axes: str = "",
    output_format: str = "hdf5",
    cutout_subregion: str = "",
):
    """
    Run ilastik pixel classification
    """
    if platform.system == "Darwin":
        ilastik_exe = ilastik_exe / "Contents" / "ilastik-release" / "run_ilastik.sh"

    subprocess_args = [
        str(ilastik_exe),
        "--headless",
        "--project=" + str(project),
        "--raw_data=" + str(raw_data),
        "--output_filename_format=" + output_filename_format,
        "--output_format=" + output_format,
    ]

    if input_axes:
        subprocess_args.append("--input-axes=" + input_axes)

    if ctx.obj["debug"]:
        subprocess_args.append("--debug")
    logger.debug("Subprocess arguments: %s", " ".join(subprocess_args))

    subprocess.run(subprocess_args, check=True, encoding="utf-8")


if __name__ == "__main__":
    main()
