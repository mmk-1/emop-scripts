#!/bin/bash

# This file is a higher-level script to run both method-level and class-level.  
# Then execute python script to create CSV file of the evaluation.

if [[ $1 == "" ]]; then
  echo "Usage: bash run_impacted.sh <csv file>"
  exit
fi

# GRANULARITY=$1

CSV_FILE=$1

{
read # Ignore first line (column header)
while IFS=, read -r REPO COMMIT
do
    echo $REPO
    bash run_20_version.sh methods $REPO $COMMIT
    bash run_20_version.sh classes $REPO $COMMIT
    python3 extract.py $REPO
done 
} < $CSV_FILE

