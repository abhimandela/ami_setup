# AMI Setup with Witty Pi L3V7 
This is the branch to modify AMI configurations to be used with the WittyPi L3V7 unit with 18650 battery holder and 18650 battery. 

WittyPi L3V7 https://www.uugear.com/product/witty-pi-4-l3v7/ can be used a single board solution that provides RTC, Watchdog and UPS functionalities intended for the AMI systems. This add on board to Raspberry Pi also provides capabilities to  schedule ON and OFF times with custom schedules.

AMI configuration files here have been adjusted to be used only with the WittyPi L3V7 and Raspberry Pi 4B with raspbian OS image version x.y.z.q (This contains the necessary software packages needed for Witty Pi L3V7). It is not tested and not guaranteed to work with other version of Witty Pi boards.

More information about Witty Pi in the user manual here: https://cdn-shop.adafruit.com/product-files/5705/WittyPi4L3V7_UserManual.pdf 

# Configuration Update Script

This script reads configuration settings from a JSON file and updates various configuration files accordingly.

Instructions to update AMI configurations:
1. Edit config.json to updated with appropriate values
2. Run the set_ami_config.py to set all necessary configurations 
3. Paths should be absolute, and eveything should work as long as the paths and values entered are correct
4. TODO: Include DATA validation 

## Usage 

1. Install the required dependencies by running:

   ```bash
   pip install -r requirements.txt

2. Set the configurations by running the set_ami_config.py as below:

* The script has to be run from the directory where config.json and this file are located
* Other files that are bring modified like the motion.conf and heliocron.toml must be present in respective paths
* From commandline that has Python3 enabled, run the command

   ```bash
   sudo python3 set_ami_config.py

* The above command prints a summary of changes done to script, make sure the changes intended are reflected correctly. 
* The script does not validate for correct input values that can be entered atleast not at this point 

This code aims to achieve the following:
1. Requirements file for installing necessary packages for the WittyPi functionality integration 
2. Ability to configure AMI systems with snapshot interval
3. Ability to set different camera settings available 
4. Ability to disable and enable motion detection 
5. Ability to set operating times using sunset and sunrise times from a given location 

The set_ami_config.py script does the following after reading the config.json file:
1. Update location in ~/.config/helicocron.toml
2. Update Camera ID by using the command "ls -dev/v4l/by-id/" in the following files and camera1.conf
3. Default videodevice to be used for capturing is "/dev/video0"
4. Update camera setttings in /home/pi/scripts/setCamera.sh 
5. Update motion configuration in /etc/motion/motion.conf

Configuration Files

    heliocron.toml: The script updates the latitude and longitude in the Heliocron TOML configuration file located at ~/.config/heliocron.toml.

    setCamera.sh: The script updates camera settings in the shell script located at /home/pi/scripts/setCamera.sh.

    motion.conf: The motion software configuration file located at /etc/motion/motion.conf is updated with motion-related settings.

    camera1.conf: The camera configuration file in the motion folder located at /etc/motion/camera1.conf is updated.

Note: Ensure that you have the necessary permissions to modify the specified configuration files. Running scripts as sudo ensures that there will be no failures due to previlege settings 

Dependencies

The script uses the following Python libraries:

    toml: A library for working with TOML configuration files.

Disclaimer

Make sure to back up your original configuration files before running this script to avoid any unintended changes.
