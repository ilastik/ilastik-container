FROM python:3.8-slim

LABEL maintainer="team@ilastik.org"

ARG ilastik_version

# install bzip2 in order to unpack ilastik binary distribution
RUN apt-get update && apt-get install -y bzip2

ADD http://files.ilastik.org/ilastik-${ilastik_version}-Linux.tar.bz2 /
RUN mkdir /ilastik-release && \
    tar -xjvf ilastik-${ilastik_version}-Linux.tar.bz2 -C /ilastik-release --strip-components=1 && \
    rm ilastik-${ilastik_version}-Linux.tar.bz2

ENV ILASTIK_EXE /ilastik-release/run_ilastik.sh

# install requirements for run_ilastik.py
RUN pip install click pyyaml
COPY ./src/run_ilastik.py /usr/local/bin

ENTRYPOINT ["/usr/local/bin/run_ilastik.py"]
CMD ["--help"]
