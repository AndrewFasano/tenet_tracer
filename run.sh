#!/bin/bash

# Usage ./run.sh [arch] [copydir] [target] (args)
# usage message + validation handled by run.py

# Simple script to run with provided copydir mounted at same location in container

set -eu
copydir=$(realpath $2)

docker build -t tenet_tracer .

set -x
docker run --rm -v $copydir:$copydir tenet_tracer $1 $copydir ${@:3}
