#!/bin/bash -x
RUN_DIR=$(dirname $0)
DOCKER_FLAGS=$(cat ${RUN_DIR}/DOCKER_FLAGS)
DOCKER_REPO=$(cat ${RUN_DIR}/DOCKER_REPO)
NAME=$(cat ${RUN_DIR}/NAME)
VERSION=$(cat ${RUN_DIR}/VERSION)
CONTAINER=$(docker run ${DOCKER_FLAGS} --env-file /home/app/env ${DOCKER_REPO}/${NAME}:${VERSION})
for i in {1..5};
	do sleep 1
	echo sleeping for 5s while container starts $i
done
docker logs $CONTAINER 
docker stop $CONTAINER
