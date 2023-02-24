#!/bin/bash

# shellcheck disable=SC2046
workDir=$(realpath -- $(dirname "$0"))

echo "${workDir}"

fundListFile="${workDir}/data/fund-list.csv"

python "${workDir}/tools/get-all-fund.py" "${fundListFile}"
