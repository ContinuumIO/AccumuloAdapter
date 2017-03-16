#!/bin/bash

set -e

chmod +x docker-compose

# Ensure that relevant containers are not running before the build starts
docker ps -aq --filter="ancestor=quay.io/geodocker/accumulo" \
              --filter="ancestor=quay.io/geodocker/zookeeper" \
              --filter="ancestor=quay.io/geodocker/hdfs:0.1" | \
    xargs docker rm -fv || true
./docker-compose down || true

make -e build
make -e test
