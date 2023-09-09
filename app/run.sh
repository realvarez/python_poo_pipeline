#!/bin/bash
app="poo_pypeline:1"
docker build -t ${app} .
docker run --rm -it --name pypeline --memory=1g -v "${PWD}\output":"/output/" ${app}
docker image rm ${app}
