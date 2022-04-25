#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

docker run -ti --rm --net=host -p 5000:5000 -p 50001:50001 --privileged --name Eisenkoch-server eisenkoch-img
