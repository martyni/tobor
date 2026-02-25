#!/bin/bash -x
ORIGINAL_DIR=$(pwd)
ROOT_PROJECT_DIR=$(git rev-parse --show-toplevel)
OUTPUT_FILE=/tmp/output

if ![ command -v ssh ]; then
   sudo apt update -y && sudo apt install sshd -y
   sudo enable ssh
   sudo systemctl start sshd
   ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa <<<y >/dev/null 2>&1
   cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys
fi


cd $ROOT_PROJECT_DIR
source $(git rev-parse --show-toplevel)/scripts/common.sh
NAME=$(cat ${RUN_DIR}/NAME)
OLD_VERSION=$(cat ${RUN_DIR}/VERSION)

echo -e ${YELLOW}Running tests from  ${RUN_DIR}${NO_COLOUR}

python_install () {
  CURRENT_TEST=python_install
  echo -e ${YELLOW} Starting Python Install ${NO_COLOUR}
  pip install .[dev]
}

python_test () {
  CURRENT_TEST=Python
  echo -e ${YELLOW} Starting Python Test ${NO_COLOUR}
  pytest
}

linting_test () {
  CURRENT_TEST=Linting
  echo -e ${YELLOW} Starting Linting Test ${NO_COLOUR}
  pylint $(git ls-files '*.py')
}

build_test () {
  CURRENT_TEST=Build
  echo -e ${YELLOW} Starting Build Test ${NO_COLOUR} in $(pwd)
  ${RUN_DIR}/build.sh
}

all_tests_pass () {
  echo -e ${GREEN} All tests passed ${NO_COLOUR}
  cd $ORIGINAL_DIR
  
}

test_failed () {
  echo -e ${RED} ${CURRENT_TEST} test failed ${NO_COLOUR}
  cd $ORIGINAL_DIR
  exit 1
}

run_test () {
  CURRENT_TEST=Run
  echo -e ${YELLOW} Starting Run Test ${NO_COLOUR}
  ${RUN_DIR}/run.sh  
  export TEST_CONTAINER=$(cat /tmp/${NAME})
  CMD=$(echo "docker logs ${TEST_CONTAINER}")
  $CMD | grep "User id is" && all_tests_pass || test_failed 
}

stop_old_container () {
  echo -e ${YELLOW} Looking for $OLD_VERSION ${NO_COLOUR}
  OLD_CONTAINER=$(docker ps  | grep $OLD_VERSION| awk '{print $1}') 
  echo -e ${YELLOW} stopping container $OLD_CONTAINER ${NO_COLOUR}
  docker stop $OLD_CONTAINER
  echo -e ${GREEN} stopped container $OLD_CONTAINER ${NO_COLOUR}
}
python_install && python_test  && build_test && run_test && stop_old_container 
