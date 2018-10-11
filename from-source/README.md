ilastik docker container build by creating a ilastik development environment inside a conda docker container.


## build

* specify `<dockerhub_user>`
* specify `<version>`, e.g. `0.0.1a1`


```bash
docker build -t <dockerhub_user>/ilastik-from-source:<version> .
```

## run

```bash
command="\
    source ~/.bashrc && conda activate ilastik && python ilastik.py --headless \
    --project=... \
    "
docker run -it --rm <dockerhub_user>/ilastik-docker-from-source:<version> /bin/bash -c $command
    
```


## Todos:

* find out why one has to `source ~/.bashrc` for it to work
