#!/bin/bash

# Outputs all version and dates for a pyPi package, ADJUSTED TO BST
# for GMT, just use the first line:
#   curl -s https://pypi.org/pypi/tca-beam/json | jq -r '.releases | to_entries[] | .key + " " + (.value[0].upload_time)'
#

curl -s https://pypi.org/pypi/tca-beam/json | jq -r '.releases | to_entries[] | .key + " " + (.value[0].upload_time)' | while read -r line; do
    version=$(echo $line | cut -d' ' -f1)
    datetime=$(echo $line | cut -d' ' -f2)
    datetime_bst=$(date -u -v+1H -j -f "%Y-%m-%dT%H:%M:%S" "$datetime" +'%Y-%m-%dT%H:%M:%S')
    echo "$version $datetime_bst"
done
