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
import taglib
import os
#from datetime import datetime, timedelta
import pytz
from timezonefinder import TimezoneFinder

# ===========================================================================================================================

### Import metadata variables including system configuration ###
with open("config.json", 'r') as file:
        json_config = json.load(file)

# ===========================================================================================================================

### Set up directory and file name/path ###

## Make directory to store files based on date

# Get date and time
date_and_time = datetime.datetime.now()

# Make directory path name (use directory specified by user as the one where they want the audio files to be stored)
# Match year_month_day format
path_to_file_storage = str(json_config["microphone"]["directory saved"] + "%s_%s_%s" % (date_and_time.year, date_and_time.month, date_and_time.day)) # e.g. '/media/bird-pi/PiImages/BIRD/raw_audio/2023_2_8'
# Create directory with this name
Path(path_to_file_storage).mkdir(exist_ok=True) # If exists already, then doesn't throw an error

## Make name for file to store in this directory

# Match LID_x__SID_x__HID_x__year_month_day__hour_minute_second format
file_to_store = str(json_config["base ids"]['location ID'] + "__" + json_config["base ids"]['System ID'] + "__" + json_config["base ids"]['Hardware ID'] + "__%s_%s_%s__%s_%s_%s" % (date_and_time.year, date_and_time.month, date_and_time.day, date_and_time.hour, date_and_time.minute, date_and_time.second))

# Obtain the number of files already within the directory
files = os.listdir(path_to_file_storage)

# Filter the files to include only those with a .wav extension
wav_files = [file for file in files if file.endswith('.wav')]

# Get the number of .wav files
order_number = len(wav_files) + 1

## Combine directory and file names into 1 path
full_path = path_to_file_storage + "/" + file_to_store + "__order_" + order_number + "." +  json_config["microphone"]["File extension"] # '/media/bird-pi/PiImages/BIRD/raw_audio/2023_2_8/LID_test__SID_test__HID_test__2023_2_8__17_42_7.wav'

##############

#Deleted record section

##############


### Metadata collection ###
# Get the current date and time
current_date = datetime.datetime.now()

# Get the current UTC time
current_utc_time = datetime.datetime.utcnow()

# Calculate the hour difference
hour_difference = str((current_date - current_utc_time).total_seconds() / 3600)[:-2]
if len(hour_difference) == 1:
    hour_difference = "0" + hour_difference

# format the time
formatted_date = current_date.strftime("%Y-%m-%dT%H:%M:%S")

# Define a function that determines if deployment is in daylight saving time at the location and datetime
def is_dst(latitude, longitude, dt):
    # Get the timezone name for the given latitude and longitude
    timezone_finder = TimezoneFinder()
    timezone_name = timezone_finder.timezone_at(lat=latitude, lng=longitude)

    # Get the timezone object for the determined timezone name
    timezone = pytz.timezone(timezone_name)

    # Localize the datetime to the specified timezone
    localized_dt = timezone.localize(dt)

    # Check if the datetime is in daylight saving time
    return localized_dt.dst() != timedelta(0)

# Obtain the daved latitude and longitude of the deployment
latitude = json_config["location"]["lat"]
longitude = json_config["location"]["lon"]

# 1 if in daylight saving time, 0 if not
dst = is_dst(latitude, longitude, current_date)

# Define function to obtain file size
def get_file_size_kb(file_path):
    # Get the size of the file in bytes
    file_size_bytes = os.path.getsize(file_path)

    # Convert bytes to kilobytes
    file_size_kb = file_size_bytes / 1024

    return file_size_kb

#Obtain file size
file_size_kb = 12

# obtain IDs
location_id = json_config["base ids"]["location id"]
system_id = json_config["base ids"]["system id"]
hardware_id = json_config["base ids"]["hardware id"]

# Note recording type
audio_type = "audible"

# Generate parent event ID
parentEventID = f"{system_id}__{audio_type}__start_time__end_time"

# Obtain datetime with underscore seperator
id_datetime = current_date.strftime("%Y_%m_%d__%H_%M_%S")

# Generate event ID
eventID = f"{system_id}__{audio_type}__{id_datetime}__{order_number}"

#Save metadata as dictionary using same heirarchical structure as the config dictionary
metadata = {
     
      "event IDs": {
         "parentEventID": "sys000001__%Y_%m_%d__19_37_48__06_37_48",
         "eventID": "sys000001__%Y_%m_%d__%H_%M_%S__motion__%q"
      },

    "date fields": {
        "eventDate": f"{formatted_date}-{hour_difference}00",
        "daylight saving time": dst,
        "recording period start time": None,
        "recording period end time": None
        },

    "file characteristics":{
         "file size (KB)": file_size_kb,
         "file path": full_path,
         "file_type": audio_type
        }
   }

# Update the config dictionary
json_config["microphone event data"].update(metadata)

with open("test.json", 'w') as json_file:
    json.dump(json_config, json_file)

# ## Additionally, create a json file with the same name as the file
# # Define the new file name with a JSON extension
# new_file_name = path_to_file_storage + "/" + file_to_store + "__order_" + order_number + ".json"

# # Define the subfolder name
# subfolder = "audio/json_scripts"

# # Create subfolder
# if not os.path.exists(subfolder):
#     os.makedirs(subfolder)

# # Create the new JSON file in the subfolder
# new_file_path = os.path.join(subfolder, os.path.basename(new_file_name))

# # Save metadata
# with open(new_file_path, 'w') as file:
#     json.dump(metadata, file, indent=4)