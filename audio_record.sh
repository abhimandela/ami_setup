#!/bin/bash

# Load configuration file, make sure the values in the config.json file are valid as there is no data validatiom being done here..
config=$(cat config.json)
datetime=$(date +"%Y%m%d%T")

# Extracting audio setting values from Config file
sample_rate=$(echo "$config" | jq -r '.audio_settings.sample_rate')
file_type=$(echo "$config" | jq -r '.audio_settings.file_type')
channels=$(echo "$config" | jq -r '.audio_settings.channels')
rec_length=$(echo "$config" | jq -r '.audio_settings.rec_length')
device=$(echo "$config" | jq -r '.audio_settings.device')
target_path=$(echo "$config" | jq -r '.audio_settings.target_path')

# Check if any of the required parameters is null and throw an error
if [[ -z $sample_rate || -z $file_type || -z $channels || -z $rec_length || -z $device || -z $target_path ]]; then
    echo "Error: One or more parameters are null. Please check the configuration."
    exit 1
fi

# Generating the command
command="arecord -t $file_type -r $sample_rate -d $rec_length -c $channels -f S16_LE --device=$device $target_path/${datetime}.${file_type}"

# Execute the command
echo "Executing command: $command"
eval $command
