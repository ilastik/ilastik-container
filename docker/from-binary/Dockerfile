# build with --build-arg ilastik_binary=ilastik-1.3.2b3-Linux.tar.bz2 <dockerhub_user>/ilastik-from-source:<version> .
# run with tini: --init

FROM ubuntu:18.04

MAINTAINER ilastik Team <team@ilastik.org>

ARG ilastik_binary

ADD http://files.ilastik.org/$ilastik_binary /
RUN mkdir ilastik-release && \
    tar xjvf $ilastik_binary -C ilastik-release --strip-components=1 && \
    rm $ilastik_binary

WORKDIR "/ilastik-release"
