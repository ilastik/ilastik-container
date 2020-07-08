"""
Small helper tool to run ilastik with a configuration file
"""
from pathlib import Path


class IlastikError(Exception):
    pass


class CMDPreconditionError(IlastikError):
    pass


def run_headless_pixel_classification(
    ilastik_exe: Path,
    project: Path,
    raw_data: Path,
    output_filename_format: str,
    input_axes: str = "",
    output_format: str = "hdf5",
):
    if not project.exists():
        raise CMDPreconditionError(f"Could not find project file {project}.")
    if not raw_data.exists():
        raise CMDPreconditionError(f"Could not find raw data file {raw_data}")

    subprocess_args = [
        ilastik_exe,
        "--headless",
        "--project=" + str(project),
        "--raw-data=" + str(raw_data),
        "--output_filename_format=" + str(output_filename_format),
        "--output_format=" + output_format,
    ]

    if input_axes:
        subprocess_args.append("--input-axes=" + input_axes)

    return subprocess_args


if __name__ == "__main__":
    pass
