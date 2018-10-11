# ilastik-docker

ilastik docker images 

Right now there are two different flavours of recipes:

1) `from-source` that uses the current source tree and a conda environment in docker build.
  Based on [continuum's miniconda image](https://hub.docker.com/r/continuumio/miniconda/).
  Image size currently `3.05GB`.

2) `from-binary` that uses a minimal base image and a binary release of ilastik.
