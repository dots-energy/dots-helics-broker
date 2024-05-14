#!/bin/bash

# login first: docker login -u dotsenergyframework

VERSION=0.0.1
REPOSITORY="dotsenergyframework/helics-broker"

docker build -t ${REPOSITORY}:${VERSION} ../.

docker push ${REPOSITORY}:${VERSION}
