# ilastik galaxy tool

## building the docker image

* supply `--build-arg ilastik_version=`, e.g. `1.3.3post3`
* image should be tagged with the same version as ilastik_version
* specify `<dockerhub_user>`

```bash
ILASTIK_VERSION=1.3.3post3
DOCKERHUB_USER=ilastik
docker build --build-arg ilastik_version=${ILASTIK_VERSION} -t ${DOCKERHUB_USER}/ilastik-galaxy:${ILASTIK_VERSION} .
```

## run

* in order to access project files and input data, locations of these files have to be mounted to the container.
  E.g. one could have all input data (including the project) in `/some/input/folder` and would therefore add `-v /some/input/folder:/input`.
  The docker container can read the contents of `/some/input/folder` in `/input`.
* A folder has to be added for the outputs as well: `-v /some/output/folder:/output`.

```bash
# define command line arguments
# try running the container without arguments to see the help
docker run --rm ilastik/ilastik-galaxy:1.3.3post3

# list the options for running pixel classification
docker run --rm ilastik/ilastik-galaxy:1.3.3post3 pixel_classification --help
```

```bash
options="\
    --config_file /input/jobconf.yaml \
    pixel_classification
"
```

example config (with all paths relative to the docker container mounts:

```yaml
raw_data: /input/2d_cells_apoptotic_1channel.png
output_filename_format: /output/ilastik-out-{nickname}-{result_type}
project: /input/2dcellsapo_1.3.2-Linux.ilp
```

```bash
# run the command in the ilastik docker container
docker run --rm \
    -v </absolute/path/to/input/folder>:/input \
    -v </absolute/path/to/output/folder>:/output \
    ilastik/ilastik-galaxy:<version> \
    ${options}
```

```bash
# for the example above:
# with the inputs on the host in /home/ilastik-user/input
# and the outputs on the host in /home/ilastik-user/output
docker run --rm -v /home/ilastik-user/input/:/input -v /home/ilastik-user/output/:/output ilastik/ilastik-galaxy:1.3.3post3 --config_file /input/jobconf.yaml pixel_classification


## building the galaxy tool

```bash
planemo tool_init \
--force \
--id 'ilastik-headless' \
--name 'ilastik' \
--container ilastik/ilastik-galaxy:1.3.3post3 \
--example_command 'pixel_classification --project 2dcellsapo_1.3.2-Linux.ilp --raw_data 2d_cells_apoptotic_1channel.png --output_filename_format 2d_cells_apoptotic_1channel-Probabilities.h5' \
--example_input 2dcellsapo_1.3.2-Linux.ilp \
--example_input 2d_cells_apoptotic_1channel.png \
--example_output 2d_cells_apoptotic_1channel-Probabilities.h5 \
--test_case \

```

