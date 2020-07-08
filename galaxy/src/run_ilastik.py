def run_headless_pixel_classification(
    testdir,
    *,
    num_distributed_workers: int = 0,
    project: Path,
    raw_data: Path,
    output_filename_format: str,
    input_axes: str = "",
    output_format: str = "hdf5",
    ignore_training_axistags: bool = False,
):
    assert project.exists()
    assert raw_data.parent.exists()

    ilastik_dot_py = Path(__file__).parent.parent.parent.parent / "ilastik.py"
    subprocess_args = [
        "python",
        str(ilastik_dot_py),
        "--headless",
        "--project=" + str(project),
        "--raw-data=" + str(raw_data),
        "--output_filename_format=" + str(output_filename_format),
        "--output_format=" + output_format,
    ]

    if input_axes:
        subprocess_args.append("--input-axes=" + input_axes)

    if ignore_training_axistags:
        subprocess_args.append("--ignore_training_axistags")

    if num_distributed_workers:
        os.environ["OMPI_ALLOW_RUN_AS_ROOT"] = "1"
        os.environ["OMPI_ALLOW_RUN_AS_ROOT_CONFIRM"] = "1"
        subprocess_args = ["mpiexec", "-n", str(num_distributed_workers)] + subprocess_args + ["--distributed"]

    result = testdir.run(*subprocess_args)
    if result.ret != 0:
        raise FailedHeadlessExecutionException(
            "===STDOUT===\n\n" + result.stdout.str() + "\n\n===STDERR===\n\n" + result.stderr.str()
        )
