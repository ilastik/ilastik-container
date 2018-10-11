ilastik docker container build by creating a ilastik development environment inside a conda docker container.


## build

* specify `<dockerhub_user>`
* specify `<version>`, e.g. `0.0.1a1`


```bash
docker build -t <dockerhub_user>/ilastik-from-source:<version> .
```

## run

* in order to access project files and input data, locations of these files have to be mounted to the container.
  E.g. one could have all input data (including the project) in `/some/input/folder` and would therefore add `-v /some/input/folder:/input`.
  The docker container can read the contents of `/some/input/folder` in `/input`.
* A folder has to be added for the outputs as well: `-v /some/output/folder:/output`.
* for some reason it is necessary to source the `.bashrc` local to the docker container prior to invocation of the command


An example invocation with a pixel classification project could look like the following:

```bash
command="\
    source ~/.bashrc && python ilastik.py --headless \
    --project=/input/<myproject.ilp> \
    --raw_data=/input/<file_to_process.png>
    --export_source=Probabilities \
    --output-format=hdf5 \
    --output_filename_format=/output/{nickname}_{result_type}.h5 \
"

docker run -it --rm <dockerhub_user>/ilastik-docker-from-source:<version> /bin/bash -c "$command"
    
```


## Todos:

* [ ] find out why one has to `source ~/.bashrc` for it to work
