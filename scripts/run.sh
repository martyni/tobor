#!/bin/bash -x
RUN_DIR=$(dirname $0)
DOCKER_FLAGS=$(cat ${RUN_DIR}/DOCKER_FLAGS)
DOCKER_REPO=$(cat ${RUN_DIR}/DOCKER_REPO)
NAME=$(cat ${RUN_DIR}/NAME)
VERSION=$(cat ${RUN_DIR}/VERSION)
if [ -f /home/app/env ]; then 
    export TEST_CONTAINER=$(docker run ${DOCKER_FLAGS} --env-file /home/app/env -v ~/.ssh:/root/.ssh ${DOCKER_REPO}/${NAME}:${VERSION})
else
    cat <<EOT >env
MOD_USER_CHANNEL_ID=${MOD_USER_CHANNEL_ID}
MY_CHANNEL_ID=${MY_CHANNEL_ID}
TOBOR_ACCESS_TOKEN=${TOBOR_ACCESS_TOKEN}
TOBOR_CLIENT_ID=${TOBOR_CLIENT_ID}
TOBOR_REFRESH_TOKEN=${TOBOR_REFRESH_TOKEN}
TOBOR_USER_TOKEN=${TOBOR_USER_TOKEN}
EOT
    export TEST_CONTAINER=$(docker run ${DOCKER_FLAGS} --env-file env  ${DOCKER_REPO}/${NAME}:${VERSION})
fi
echo ${TEST_CONTAINER} >/tmp/${NAME}

for i in {1..10};
	do sleep 1
	echo sleeping for 10s while container starts $i
        docker logs ${TEST_CONTAINER}| grep "User id is" && break
done
