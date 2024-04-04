#!/bin/bash

# Load JSON configuration file
config=$(cat config.json)

# Extracting values from JSON
sample_rate=$(echo "$config" | jq -r '.audio_settings.sample_rate')
file_type=$(echo "$config" | jq -r '.audio_settings.file_type')
channels=$(echo "$config" | jq -r '.audio_settings.channels')
rec_length=$(echo "$config" | jq -r '.audio_settings.rec_length')
device=$(echo "$config" | jq -r '.audio_settings.device')
target_path=$(echo "$config" | jq -r '.audio_settings.target_path')
rec_interval=$(echo "$config" | jq -r '.audio_settings.rec_interval')

# Extract days of the week and start/end times
days_of_week=$(echo "$config" | jq -r '.audio_operation.days_of_week[]')
start_times=($(echo "$config" | jq -r '.audio_operation | to_entries | map(select(.key | match("^start_time_[0-9]+$"))) | .[].value'))
end_times=($(echo "$config" | jq -r '.audio_operation | to_entries | map(select(.key | match("^end_time_[0-9]+$"))) | .[].value'))
numer_of_schedules=$(echo "$config" | jq -r '.audio_operation.numer_of_schedules')
start_time_0=$(echo "$config" | jq -r '.audio_operation.start_time_0')
end_time_0=$(echo "$config" | jq -r '.audio_operation.end_time_0')
start_time_1=$(echo "$config" | jq -r '.audio_operation.start_time_1')
end_time_1=$(echo "$config" | jq -r '.audio_operation.end_time_1')



# Check if any required parameter is null
if [[ -z $sample_rate || -z $file_type || -z $channels || -z $rec_length || -z $device || -z $target_path || -z $rec_interval ]]; then
    echo "Error: One or more parameters are null. Please check the configuration."
    exit 1
fi

# Check if current time falls within any of the specified time frames and days
current_time=$(date +"%H:%M:%S")
current_day=$(date +"%a")

echo "current time: $current_time"
echo "current day: $current_day"
echo "days_of_week: $days_of_week"
echo "start_times: $start_times"
echo "end_times: $end_times"


echo " numer_of_schedules: $numer_of_schedules"
echo "start_time_0 : $start_time_0"
echo "end_time_0: $end_time_0"
echo "start_time_1: $start_time_1"
echo "end_time_1: $end_time_1"



# Function to check if a given time is within a time frame
time_in_range() {
    local start=$1
    local end=$2
    local time=$3
    [[ "$time" > "$start" && "$time" < "$end" ]]
}

# Check if the current day and time are within the specified ranges
for i in "${!days_of_week[@]}"; do
    if [[ "${days_of_week[$i]}" == "$current_day" ]]; then
        if time_in_range "${start_times[$i]}" "${end_times[$i]}" "$current_time"; then
            # Generating the command
            command="arecord -t $file_type -r $sample_rate -d $rec_length -c $channels -f S16_LE --device=$device $target_path/${sample_rate}-${rec_length}.${file_type}"

            # Execute the command
            echo "Executing command: $command"
            #eval $command
            break # Exit the loop if a match is found
        fi
    fi
done

# Sleep for the specified rec_interval
sleep "$rec_interval"