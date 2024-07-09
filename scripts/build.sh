source $(git rev-parse --show-toplevel)/scripts/common.sh

NAME=$(cat ${RUN_DIR}/NAME)
VERSION=$(cat ${RUN_DIR}/VERSION)
BUILD_EXIT_FILE=/tmp/build_exit_code
BUILD_OUTPUT=/tmp/build_output
echo "old ${VERSION}"
LAST_DIGIT=$(echo ${VERSION} | awk -F '.' '{print $3}')
let "LAST_DIGIT=1+${LAST_DIGIT}"
VERSION=$(echo  ${VERSION} |awk -F '.' '{print $1 "." $2 "." }')${LAST_DIGIT}
echo "new ${VERSION}"
echo "${VERSION}"> $(git rev-parse --show-toplevel)/scripts/VERSION

if [[ $PIPELINE ]]; then
   #Capture docker exit status or fail with status 1 if build fails
   docker build -t $NAME:$VERSION . 2>&1 | tee $BUILD_OUTPUT && awk -F 'exit code: ' '/exit code/{print $2}' $BUILD_OUTPUT > $BUILD_EXIT_FILE || exit 1
else
   #Retain colour in docker build and capture exit status or fail with status 1 if build fails
   unbuffer docker build -t $NAME:$VERSION . 2>&1 | tee $BUILD_OUTPUT && awk -F 'exit code: ' '/exit code/{print $2}' $BUILD_OUTPUT > $BUILD_EXIT_FILE || exit 1
fi

echo docker -it run  $NAME:$VERSION
echo exiting $(cat ${BUILD_EXIT_FILE})
exit $(cat $BUILD_EXIT_FILE)
