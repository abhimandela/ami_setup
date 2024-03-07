import json
import re

def read_json_config(json_path):
    with open(json_path, 'r') as json_file:
        return json.load(json_file)

def update_camera_settings(script_path, camera_data):
    with open(script_path, 'r') as script_file:
        script_lines = script_file.readlines()

    # Update camera settings
    for key, value in camera_data['camera'].items():
        for i, line in enumerate(script_lines):
            # Using a regular expression to find lines containing the setting key
            #print (re.search(fr'v4l2-ctl -d /dev/video0 -c {key}=\S+', line)," key: ", key," val: ", value)
            if re.search(fr'v4l2-ctl -d /dev/video0 -c {key}=\S+', line):
                # Replace the setting value while preserving the rest of the line
                script_lines[i] = re.sub(fr'({key}=)\S+', fr'\1{value}', line)
                break

    # Write the updated script content back to the file
    with open(script_path, 'w') as script_file:
        script_file.writelines(script_lines)

if __name__ == "__main__":
    # Replace 'config.json' with the actual path to your JSON configuration file
    json_config_path = 'config.json'

    # Replace '/home/pi/scripts/setCamera.sh' with the actual path to your shell script file
    script_path = '/home/abhi/Desktop/raspi/setCamera.sh'

    # Read the JSON configuration file
    json_config = read_json_config(json_config_path)

    # Update camera settings in the shell script file
    update_camera_settings(script_path, json_config)

    print("setCamera.sh script updated successfully.")
