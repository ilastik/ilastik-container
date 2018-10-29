#!/bin/bash

ILASTIK_DOCKER_IMAGE_VERSION=${ILASTIK_DOCKER_IMAGE_VERSION:-1.3.2b3}
CONTAINER_NAME="ilastik-from-binary_${ILASTIK_DOCKER_IMAGE_VERSION}.sif"

source scriptVars.sh

buildContainer(){
    rm -f $CONTAINER_NAME
    singularity build $CONTAINER_NAME docker://ilastik/ilastik-from-binary:$ILASTIK_DOCKER_IMAGE_VERSION
}

if [ -f $CONTAINER_NAME ]; then
    ANSWER="$(politeSetValue "There is already a built container at $CONTAINER_NAME. Should we use it?" y n)"
    if [ $ANSWER = n ]; then
        buildContainer
    fi
else
    buildContainer
fi

singularity shell --pwd /ilastik-release $CONTAINER_NAME
