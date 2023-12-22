import json
import re

# Load the config paramters from the JSON file
def read_json_config(json_path):
    with open(json_path, 'r') as json_file:
        return json.load(json_file)
    
####################################################################################################################

def update_motion_config(script_path, config_data, camera_id):
    with open(script_path, 'r') as script_file:
        script_lines = script_file.readlines()

    print (" ***************** Updating motion settings ***************** ")

    #List every motion configuration parameter and addionally specify the camera ID (videodevice) and exif_text (field for metadata storage)
    fields = list(config_data['motion'].keys()) + ['videodevice', "exif_text"]

    # For each line in the motion.config file
    for i, line in enumerate(script_lines):

        # Ignore lines starting with #
        if line.strip().startswith('#'):
            continue

        # For each field...
        for field_search in fields:

            # Search for the occurence of the field name, followed by one or more whitespaces
            pattern = fr'({field_search} )(\S+)'
            match = re.search(pattern, line)

            if match:

                # Obtain the field name
                field,_ = line.split(' ', 1)

                # This if condition stops the capture of field name mentions within the exif_text string
                # The exif_text field also includes a semicolon before the field name
                if field == field_search or field == f";{field_search}":

                    # Camera ID
                    if field_search == "videodevice":
                        # Extract the part after "videodevice"
                        _, existing_camera_id = line.split('videodevice', 1)
                        # Replace the existing camera ID with the new camera ID
                        new_line = line.replace(existing_camera_id, f' {camera_id}\n')
                        print(f"Updated videodevice line: {new_line.strip()}")
                        script_lines[i] = new_line

                    # Exif text
                    elif field_search == "exif_text":

                        fields_ignore = ["operation", "microphone event data"]

                        metadata =  dict((field, config_data[field]) for field in config_data if field not in fields_ignore)

                        # Replace the whole line to remove the semicolon
                        new_line = line.replace(line, f"exif_text \'{json.dumps(metadata)}\'\n")
                        print(f"Updated exif metadata configuration") 
                        script_lines[i] = new_line

                    # Remaining fields in the motion configuration settings
                    else:
                        print(f"Original line: {line.strip()}")
                        _, existing_value = line.split(field_search, 1)
                        # Replace the existing field value with the new field value
                        new_line = line.replace(existing_value, f" {config_data['motion'][field_search]}\n")
                        print(f"Updated line: {new_line.strip()}")
                        script_lines[i] = new_line

                else:
                    continue

    # Write the updated script content back to the file
    with open(script_path, 'w') as script_file:
        script_file.writelines(script_lines)

####################################################################################################################

if __name__ == "__main__":
    # Replace 'config.json' with the actual path to your JSON configuration file
    json_config_path = 'config.json'

    #Initialize camera ID if camera ID lookup fails 
    camera_id = '/dev/video0'

    # Replace with the actual path to your shell script file as needed
    motion_script_path = 'motion_scripts\motion.conf'

    # Read the JSON configuration file
    json_config = read_json_config(json_config_path)

    # Update motion settings in the shell script file
    update_motion_config(motion_script_path, json_config, camera_id)