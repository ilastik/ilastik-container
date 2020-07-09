"""
Small helper tool to run ilastik with a configuration file
"""
from pathlib import Path
import json
import logging

import click


logger = logging.getLogger()


class IlastikError(Exception):
    pass


class CMDPreconditionError(IlastikError):
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


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.option("--config_file")
@click.pass_context
def main(ctx, debug, config_file=None):
    if debug:
        logger.setLevel(logging.DEBUG)
    if config_file:
        with open(config_file, "r") as f:
            opts = json.load(f)
            # ctx.obj is used to determine values for arguments supplied
            # in the config file
            ctx.obj = opts


@main.command("pixel_classification")
@click.option("--ilastik_exe", required=True)
@click.option("--project", required=True, cls=DefaultFromContextObj)
@click.option("--raw_data", required=True, cls=DefaultFromContextObj)
@click.option("--output_filename_format", required=True, cls=DefaultFromContextObj)
@click.option("--input_axes", required=False, cls=DefaultFromContextObj)
@click.option("--output_format", required=False, cls=DefaultFromContextObj)
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
    cutout_subregion: str = ""
):
    if not project.exists():
        raise CMDPreconditionError(f"Could not find project file {project}.")
    if not raw_data.exists():
        raise CMDPreconditionError(f"Could not find raw data file {raw_data}")

    subprocess_args = [
        ilastik_exe,
        "--headless",
        "--project=" + str(project),
        "--raw_data=" + str(raw_data),
        "--output_filename_format=" + str(output_filename_format),
        "--output_format=" + output_format,
    ]

    if input_axes:
        subprocess_args.append("--input-axes=" + input_axes)

    return subprocess_args


if __name__ == "__main__":
    main()
