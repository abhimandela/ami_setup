#Script to set configiration set in config.json 
import json
import toml
import re
import subprocess

# Load the config paramters from the JSON file
def read_json_config(json_path):
    with open(json_path, 'r') as json_file:
        return json.load(json_file)

# Update the Heliocron settings under the recommended config file 
def update_toml_config(toml_path, location_data):
    with open(toml_path, 'r') as toml_file:
        config = toml.load(toml_file)

    # Update location information
    #print ("Lat: ",location_data['location']['lat'])
    #print ("Lon: ",location_data['location']['lon'])
    config['latitude'] = location_data['location']['lat']
    config['longitude'] = location_data['location']['lon']

    # Write the updated TOML configuration back to the file
    with open(toml_path, 'w') as toml_file:
        toml.dump(config, toml_file)

# Run the command "ls -l /dev/v4l/by-id/" and get the first line
def get_camera_id():
    try:
        ls_output = subprocess.check_output(["ls", "/dev/v4l/by-id/"], text=True)
        camera_id = ls_output.split('\n')[0].split()[-1]
        print ("camera ID is: ",camera_id)
        return camera_id
    except subprocess.CalledProcessError as e:
        print(f"Error running 'ls' command: {e}, defaulting to /dev/video0")
        return '/dev/video0'

# Configure 'motion' software related paramters 
def update_motion_config(script_path, motion_data, camera_id):
    with open(script_path, 'r') as script_file:
        script_lines = script_file.readlines()

    #print (motion_data['motion'].items())

    # Update motion settings
    for key, value in motion_data['motion'].items():
        for i, line in enumerate(script_lines):
            
            # Ignore lines starting with #
            if line.strip().startswith('#'):
                continue

            # Case to update videodevice ID which is not set in the config.json file
            if 'videodevice' in line:
                print(f"Original videodevice line: {line.strip()}")
                
                # Extract the part after "videodevice"
                _, existing_camera_id = line.split('videodevice')
                
                # Replace the existing camera ID with the new camera ID
                new_line = line.replace(existing_camera_id, f' {camera_id}')
                
                print(f"Updated videodevice line: {new_line.strip()}") 
                break 

            # Using a regular expression to find lines containing the setting key and value
            pattern = fr'({key} )(\S+)'
            #print ("pattern: ",pattern)
            match = re.search(pattern, line)
            if match:
                original_value = match.group(2)
                print(f"Original line: {line.strip()}")
                # Replace the setting value while preserving the rest of the line
                new_line = line.replace(f"{key} {original_value}", f"{key} {value}")
                print(f"Updated line: {new_line.strip()}")
                script_lines[i] = new_line
                break

    # Write the updated script content back to the file
    with open(script_path, 'w') as script_file:
        script_file.writelines(script_lines)

# Update the camera config files with videodevice ID and other info
def update_camera_config(config_path, camera_id):
    # Read the content of the config file
    with open(config_path, 'r') as config_file:
        config_lines = config_file.readlines()

    #print ("config_path", config_path)
    print ("camera_id", camera_id)

    # Update the line containing "videodevice"
    for i, line in enumerate(config_lines):
        
        # Skip lines #, usually commented out lines
        if line.startswith('#'):
                continue
        
        if 'videodevice' in line:
                      
            # Split the line into parts separated by spaces
            parts = line.split()

            # Replace the part after "videodevice" with the camera_id value
            if len(parts) > 1:
                #print ("Length ", len(parts))
                #print ("Part[0] ",parts[0])
                #print ("Part[1] ",parts[1])
                parts[1] = camera_id

            # Join the parts back into a line
            new_line = ' '.join(parts)
            print ("new_line", new_line)

            # Update the list with the new line and add new line character to accommodate for join
            config_lines[i] = new_line + '\n'

            break  # Stop searching once the line is updated

    # Write the updated content back to the config file
    with open(config_path, 'w') as config_file:
        config_file.writelines(config_lines)

# Update camera settings along with the video device ID / Camera ID 
def update_camera_settings(script_path, camera_data, camera_id):
    with open(script_path, 'r') as script_file:
        script_lines = script_file.readlines()
    
    # Update camera settings
    for key, value in camera_data['camera'].items():
        for i, line in enumerate(script_lines):
            
            # Ignore lines starting with #
            if line.strip().startswith('#'):
                continue
            
            # Using a regular expression to find lines containing the setting key and value
            #pattern = fr'({key}=)(\S+)' # Only to replace the key and value 
            pattern = fr'(v4l2-ctl -d \S+ -c {key}=)(\S+)'
            match = re.search(pattern, line)

            if match:
                original_value = match.group(2)
                print(f"Original line: {line.strip()}")
                # Replace the setting value while preserving the rest of the line
                #new_line = line.replace(f"{key}={original_value}", f"{key}={value}")
                line = re.sub(fr'-d /dev/\S+', f'-d {camera_id}', line)
                line = line.replace(f"{key}={original_value}", f"{key}={value}")
                print(f"Updated line: {line.strip()}")
                script_lines[i] = line
                break

    # Write the updated script content back to the file
    with open(script_path, 'w') as script_file:
        script_file.writelines(script_lines)

if __name__ == "__main__":
    # Replace 'config.json' with the actual path to your JSON configuration file
    json_config_path = 'config.json'

    #Initialize camera ID if camera ID lookup fails 
    camera_id = '/dev/video0'
    camera_id = get_camera_id()

    print ("Camera ID after initialization", camera_id)

    # Heliocron settings script is located here: '~/.config/helicocron.toml' 
    toml_config_path = '/home/pi/.config/heliocron.toml'

    # Replace with the actual path to your shell script file as needed
    camera_script_path = '/home/pi/scripts/setCamera.sh'
    motion_script_path = '/etc/motion/motion.conf'
    camera_config_path = '/etc/motion/camera1.conf'
            
    # Read the JSON configuration file
    json_config = read_json_config(json_config_path)

    # Update location information in the TOML configuration file
    update_toml_config(toml_config_path, json_config)

    # Update camera settings in the shell script file
    update_camera_settings(camera_script_path, json_config, camera_id)

    # Update motion settings in the shell script file
    update_motion_config(motion_script_path, json_config, camera_id)

    #Update camera config files in the motion folder
    update_camera_config(camera_config_path, camera_id)

    print("Configuration files updated successfully.")
