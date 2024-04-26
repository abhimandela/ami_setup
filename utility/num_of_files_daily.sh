#!/bin/bash

# Replace 'your_image_folder_path' with the actual path to your image folder
image_folder="/media/abhi/T7"

# Check if the folder exists
if [ ! -d "$image_folder" ]; then
    echo "Error: Folder not found!"
    exit 1
fi

# Use find to get a list of image files and awk to extract the date part
find "$image_folder" -type f -iname "*.jpg" | awk -F'[-.]' '{print $2}' | cut -c 1-8 | sort | uniq -c
