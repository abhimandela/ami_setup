#!/usr/bin/env python3

"""Python script run by crontab at intervals within the targetted time for bird acoustic recording"""
 
__author__ = 'Grace Skinner'

# ===========================================================================================================================

### imports ###

from pathlib import Path # pathlib part of python standard library. Used to make new directories
import datetime # datetime part of python standard library. Used to get date and time 
import subprocess # Used to run bash arecord from python
#import birdconfig # Used to configure settings for bird recording. Access variables defined in birdconfig.py
import json # Used to configure settings for bird recording. Access variables defined in system_config.JSON

# To store metadata
import time
import taglib
import os

# ===========================================================================================================================

### Import metadata variables including system configuration ###
with open("parent_jsons/1_boot_start.json", 'r') as file:
        boot_metadata = json.load(file)

# ===========================================================================================================================

### Set up directory and file name/path ###

## Make directory to store files based on date

# Get date and time
date_and_time = datetime.datetime.now()

# Make directory path name (use directory specified by user as the one where they want the audio files to be stored)
# Match year_month_day format
path_to_file_storage = str(boot_metadata["Directory saved"] + "%s_%s_%s" % (date_and_time.year, date_and_time.month, date_and_time.day)) # e.g. '/media/bird-pi/PiImages/BIRD/raw_audio/2023_2_8'
# Create directory with this name
Path(path_to_file_storage).mkdir(exist_ok=True) # If exists already, then doesn't throw an error

## Make name for file to store in this directory

# Match LID_x__SID_x__HID_x__year_month_day__hour_minute_second format
file_to_store = str(boot_metadata['locationID'] + "__" + boot_metadata['System ID'] + "__" + boot_metadata['Hardware ID of Pi system'] + "__" + boot_metadata['Hardware ID of sensor'] + "__%s_%s_%s__%s_%s_%s" % (date_and_time.year, date_and_time.month, date_and_time.day, date_and_time.hour, date_and_time.minute, date_and_time.second))

# Obtain the number of files already within the directory
files = os.listdir(path_to_file_storage)

# Filter the files to include only those with a .wav extension
wav_files = [file for file in files if file.endswith('.wav')]

# Get the number of .wav files
order_number = len(wav_files) + 1

## Combine directory and file names into 1 path
full_path = path_to_file_storage + "/" + file_to_store + "__order_" + order_number + "." +  boot_metadata["File extension"] # '/media/bird-pi/PiImages/BIRD/raw_audio/2023_2_8/LID_test__SID_test__HID_test__2023_2_8__17_42_7.wav'

# ===========================================================================================================================

### Recording ###

## Process arguments - Make list of arecord function and arguments used by arecord

# For reference:
# (Can change these settings using the system_config.JSON file)
# -D plughw:dodoMic,0 is the recording Device - this may need to be done in set-up of each AMI? Can't use card number as it occasionally changes (usually 1). 
# -c 1 is the number of channels, here 1
# -d 60 is the duration, here 60 seconds 
# -r 24000 is the sampling rate, here 24000Hz (needs to be at least double the highest frequency bird call we want to sample)
# -f S32_LE is the format, here S32_LE
# -t wav is the file type to save, here wav file
# -V mono is the type, here mono (could also be stereo)
# -v is verbose 
# full_path specifies the file path to save the file to (as defined above) 

# Arguments set at default
#proc_args = ['arecord', '-D', 'plughw:dodoMic,0', '-c', '1', '-d', '60', '-r', '24000', '-f', 'S32_LE', '-t', 'wav', '-V', 'mono', '-v', full_path]

# Arguments read in from the system_config.JSON file (which can be altered)
proc_args = ['arecord', '-D', boot_metadata['Microphone brand name'], '-c', boot_metadata['Number of channels'], '-d', boot_metadata["Recording duration"], '-r', boot_metadata['Sampling frequency'], '-f', boot_metadata['Data format'], '-t', boot_metadata["File extension"], '-V', boot_metadata['Recording type'], '-v', full_path]

## Recording process - run the arecord function from Python
rec_proc = subprocess.Popen(proc_args)

# Verbose
# pid = process id
print("Start recording with arecord > rec_proc pid = " + str(rec_proc.pid))
print("Start recording with arecord > recording started")

# Make sure it waits for the recording to be complete before moving on
rec_proc.wait()

# Final verbose
print("Stop recording with arecord > Recording stopped") 

# ===========================================================================================================================

### Metadata collection ###
# Get the current date and time
current_date = datetime.datetime.now()

# Extract the year, month, and day
year = current_date.year
month = current_date.month
day = current_date.day

# Get the current UTC time
current_utc_time = datetime.datetime.utcnow()

# Calculate the hour difference
hour_difference = str((current_date - current_utc_time).total_seconds() / 3600)[:-2]
if len(hour_difference) == 1:
    hour_difference = "0" + hour_difference

# format the time
formatted_datetime = current_date.strftime("%Y-%m-%dT%H:%M:%S")

# Check if daylight saving time is currently in effect
is_dst = time.localtime().tm_isdst

# Obtain the file size
def get_file_size_kb(file_path):
    # Get the size of the file in bytes
    file_size_bytes = os.path.getsize(file_path)

    # Convert bytes to kilobytes
    file_size_kb = file_size_bytes / 1024

    return file_size_kb

file_size_kb = get_file_size_kb(full_path)

# Usage example
metadata = {
    "eventID": file_to_store,
    "eventDate": f"{formatted_datetime}-{hour_difference}00",
    "year": year,
    "month": month,
    "day": day,
    "type": "sound",
    "Daylight saving time": is_dst,
    "Recording period start date and time": None, # obtained from Witty pi??
    "Recording period end date and time": None, # obtained from Witty pi??
    "File size (KB)": file_size_kb,
    "Hardware ID of sensor": None # user input and obtained from database
}

# Update boot metadata
boot_metadata.update(metadata)

with taglib.File(path_to_file_storage, save_on_exit=True) as recording:
    #print(recording.tags)
    recording.tags["TITLE"] = json.dumps(metadata)
    print("Metadata added to recording")

## Additionally, create a json file with the same name as the file
# Define the new file name with a JSON extension
new_file_name = path_to_file_storage + "/" + file_to_store + "__order_" + order_number + ".json"

# Define the subfolder name
subfolder = "audio/json_scripts"

# Create subfolder
if not os.path.exists(subfolder):
    os.makedirs(subfolder)

# Create the new JSON file in the subfolder
new_file_path = os.path.join(subfolder, os.path.basename(new_file_name))

# Save metadata
with open(new_file_path, 'w') as file:
    json.dump(metadata, file, indent=4)