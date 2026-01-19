#!/bin/bash -x
RUN_DIR=$(dirname $0)
DOCKER_FLAGS=$(cat ${RUN_DIR}/DOCKER_FLAGS)
DOCKER_REPO=$(cat ${RUN_DIR}/DOCKER_REPO)
NAME=$(cat ${RUN_DIR}/NAME)
VERSION=$(cat ${RUN_DIR}/VERSION)
export TEST_CONTAINER=$(docker run ${DOCKER_FLAGS} --env-file /home/app/env -v ~/.ssh:/home/app/.ssh ${DOCKER_REPO}/${NAME}:${VERSION})
echo ${TEST_CONTAINER} >/tmp/${NAME}
for i in {1..10};
	do sleep 1
	echo sleeping for 10s while container starts $i
        docker logs ${TEST_CONTAINER}| grep "User id is" && break
done
