import json
import subprocess
import time
from datetime import datetime

# Load JSON configuration file
with open('config.json', 'r') as f:
    config = json.load(f)

# Extracting values from JSON
sample_rate = config['audio_settings']['sample_rate']
file_type = config['audio_settings']['file_type']
channels = config['audio_settings']['channels']
rec_length = config['audio_settings']['rec_length']
device = config['audio_settings']['device']
target_path = config['audio_settings']['target_path']
rec_interval = config['audio_settings']['rec_interval']

# Extract days of the week and start/end times
days_of_week = config['audio_operation']['days_of_week']
start_times = config['audio_operation']['start_times']
end_times = config['audio_operation']['end_times']
number_of_schedules = len(start_times)  # Derive the number of schedules from start_times

print("sample_rate:", sample_rate)
print("file_type:", file_type)
print("channels:", channels)
print("rec_length:", rec_length)
print("device:", device)
print("target_path:", target_path)
print("rec_interval:", rec_interval)
print("days_of_week:", days_of_week)
print("start_times:", start_times)
print("end_times:", end_times)
print("number_of_schedules:", number_of_schedules)

# Function to check if a given time is within a time frame
def time_in_range(start, end, x):
    start_time = datetime.strptime(start, '%H:%M:%S')
    end_time = datetime.strptime(end, '%H:%M:%S')
    return start_time <= x < end_time


# Infinite loop to continuously check and execute the command
while True:
    current_time = datetime.now().strftime('%H:%M:%S')
    current_day = datetime.now().strftime('%a')
    current_date_time = datetime.now().strftime('%Y%m%d_%H%M%S')

    print("Current time:", current_time)
    print("Current day:", current_day)
    print("Current datetime:", current_date_time)
    

    # Check if the current day and time are within any of the specified time frames
    for i in range(number_of_schedules):
        if current_day in days_of_week:
            if time_in_range(start_times[i], end_times[i], datetime.strptime(current_time, '%H:%M:%S')):
                # Generating the command
                command = f"arecord -t {file_type} -r {sample_rate} -d {rec_length} -c {channels} -f S16_LE --device={device} {target_path}/{current_date_time}.{file_type}"
                print("Executing command:", command)
                #subprocess.run(command, shell=True)
                break  # Exit the loop if a match is found

    # Sleep for the specified rec_interval
    print("Sleeping for:", rec_interval)
    time.sleep(int(rec_interval))
    

