#!/bin/bash

# Function to convert the string time to Unix timestamp
function string_to_timestamp() {
    date -d "$1" +"%s"
}

# Current timestamp
current_timestamp=$(date +"%s")



# check control worker healthy
file_time=$(cat ./healthcheck.txt)
file_timestamp=$(string_to_timestamp "$file_time")
duration=$((current_timestamp - file_timestamp))
if [[ $duration -gt 60 ]]
then
    exit 1
fi

exit 0
