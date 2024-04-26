# Function to convert date and time to timestamp in seconds
get_timestamp() 
{
    date -d "$1" +"%s"
}

# Find all image files
image_files=($(ls -1 /home/abhi/Downloads/*.{jpg,jpeg,png,gif} 2>/dev/null))

# Get the creation times of the first and last image
first_image_time=$(stat -c %Y "${image_files[0]}")
last_image_time=$(stat -c %Y "${image_files[-1]}")

# Iterate through image files and gather information
for image_path in "${image_files[@]}"; do
    # Get file information
    creation_time=$(stat -c %Y "$image_path")
    size=$(stat -c %s "$image_path")
    image_specs=$(file "$image_path")

    # Print information to CSV file
    echo "\"$image_path\",\"$(date -d @"$creation_time")\",\"$size\",\"$image_specs\"" >> image_info.csv
done

# Calculate the time difference in seconds
time_difference=$((last_image_time - first_image_time))

# Print the time difference and timestamps
echo "Time difference between the first and last image: ${time_difference} seconds"
echo "Timestamp of the first image: $(date -d @"${first_image_time}")"
echo "Timestamp of the last image: $(date -d @"${last_image_time}")"

