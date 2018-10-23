# ocker build --no-cache -t <dockerhub_user>/ilastik-from-source:<version> .
FROM continuumio/miniconda3:latest

MAINTAINER ilastik Team <team@ilastik.org>

WORKDIR "/ilastik"
COPY ilastik.pth .

RUN conda update -y -c conda-forge conda && \
    conda create -y -n ilastik -c ilastik-forge -c conda-forge \
    ilastik-dependencies-no-solvers-no-gui && \
    conda remove -n ilastik -y ilastik-meta && \
    git clone https://github.com/ilastik/ilastik-meta && \
    cd ilastik-meta && \
    git submodule update --init --recursive && \
    rm -rf .git && \
    cd `conda info --root`/envs/ilastik && \
    ln -s /ilastik/ilastik-meta && \
    mv /ilastik/ilastik.pth ./lib/python3.6/site-packages/ilastik-meta.pth && \
    conda clean -tipsy

RUN echo "conda activate ilastik" >> ~/.bashrc

WORKDIR "/ilastik/ilastik-meta/ilastik"
