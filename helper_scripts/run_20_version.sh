#!/bin/bash

if [[ $1 == "" || $2 == "" || $3 == "" ]]; then
  echo "Usage: ./run_impacted.sh <granularity: methods or classes> <github repository> <starting commit SHA>"
  exit
fi

# Variable to keep track of whether we want method-level or class-level impacted analysis
# so the MVN_COMMAND is adjusted accordingly
GRANULARITY=$1

# Get repository as second argument and then split by '/'. e.g. apache/commons-codec -> apache + commons-codec
REPO=$2
AUTHOR=$(echo $REPO | cut -d '/' -f 1)
PROJECT=$(echo $REPO | cut -d '/' -f 2)
REPO_URL="https://github.com/"${REPO}

# Global declaration, assigned in if-else conditions
MVN_COMMAND=""

# Current dir of the script
SCRIPT_DIR=$(pwd)/

echo ${SCRIPT_DIR}

# The project we want to do evaluation on
PROJECT_DIR=${SCRIPT_DIR}/repos/

# Logs dir should be in the directory of the script
# It will hold the dependency file, impacted-class/method and changed-class/method files.
# Also a 'commit' file to keep hold of SHA
LOGS_DIR=${SCRIPT_DIR}/logs/${AUTHOR}/${PROJECT}

# Inserting the pom text for STARTS
PLUGIN='<plugin>\n<groupId>edu.illinois</groupId>\n<artifactId>starts-maven-plugin</artifactId>\n<version>1.4-SNAPSHOT</version>\n</plugin>'

# The base commit to start doing analysis
# This should be the latest commit of the number of commits to do analysis on
# so that with `git rev-list --reverse`, we can get the oldest commit.
START_COMMIT=$3


# Check for the input and adjust MVN_COMMAND and LOGS_DIR accordingly.
if [ "$GRANULARITY" = "methods" ]
then
  echo "Method-level Analysis"
  MVN_COMMAND="mvn starts:methods -DupdateMethodsChecksums=true -Drat.skip -Denforcer.skip"
  LOGS_DIR=${LOGS_DIR}/methods
elif [ "$GRANULARITY" = "classes" ]
then
  echo "Class-level Analysis"
  MVN_COMMAND="mvn starts:impacted -DupdateImpactedChecksums=true -Drat.skip -Denforcer.skip"
  LOGS_DIR=${LOGS_DIR}/classes
else
  echo "Invalid input"
  exit
fi

# Make the logs dir and its subdirs
mkdir -p ${LOGS_DIR}
# Move to project dir
cd ${PROJECT_DIR}

# Clone into ./repos
git clone ${REPO_URL} ${PROJECT}

# Update PROJECT_DIR
PROJECT_DIR=${PROJECT_DIR}/${PROJECT}

# Move to the repo
cd ${PROJECT_DIR}

# Remove any previous .starts folder just in case.
rm -rf .starts/

# COUNTER will be used to make dir in order of the commits that are run. Will be helpful for 
# extract.py as well
COUNTER=0

# Main loop. You can adjust the number of versions to run STARTS on with --max-count=<n>
for commit in $(git rev-list --max-count=5 --abbrev-commit --reverse ${START_COMMIT});
do
    # Extract the relevant commit
    git checkout -f ${commit}

    # Double-check if checkout happened successfully
    COMMIT_ID=$(git rev-parse --short HEAD)
    if [ $COMMIT_ID != $commit ]; then
        echo $COMMIT_ID
        echo $commit
        echo "current commit not equal to expected sha"
        exit
    fi

    # Modify pom file to insert STARTS
    sed -i "/<\/plugins>/i\\$PLUGIN" pom.xml

    # Make sub dir in logs/classes or logs/methods. We keep the commit as a seperate file
    # called "commit" inside ${LOGS_DIR}/${COUNTER}
    mkdir -p ${LOGS_DIR}/${COUNTER}
    

    # For class-level, the starts:impacted will not find the changed-classes if we don't generate
    # a starting deps.zlc file. So we execute this before starting the main loop. For method level
    # we don't have this. We should unify the approaches later
    # if [[ "$GRANULARITY" = "classes" && $COUNTER == 0 ]]
    # then
    #   echo "we are here!"
    #   mvn starts:starts -Drat.skip -Dcheckstyle.skip -DskipTests=True
    #   mvn starts:impacted -Drat.skip | tee ${LOGS_DIR}/${COUNTER}/maven_log
    # else
      # Run STARTS
    ${MVN_COMMAND} | tee ${LOGS_DIR}/${COUNTER}/maven_log
    # fi
    
    # Copy STARTS result files into the logs
    cp .starts/* ${LOGS_DIR}/${COUNTER}
    
    # Create "commit" file in logs dir
    echo ${commit} > ${LOGS_DIR}/${COUNTER}/commit

    ((COUNTER++))
done