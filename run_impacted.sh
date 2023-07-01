#!/bin/bash

# This file is a higher-level script to run both method-level and class-level.  
# Then execute python script to create CSV file of the evaluation.

bash run_20_version.sh methods
bash run_20_version.sh classes
python3 extract.py