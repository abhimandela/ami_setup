#!/bin/bash
# file: beforeShutdown.sh
#
# This script will be executed after Witty Pi receives shutdown command (GPIO-4 gets pulled down).
# If you want to run your commands before turnning of your Raspberry Pi, you can place them here.
# Raspberry Pi will not shutdown until all commands here are executed.
#
# Remarks: please use absolute path of the command, or it can not be found (by root user).
# Remarks: you may append '&' at the end of command to avoid blocking the main daemon.sh.
#
#Kill pending processes and shutdown
sudo pkill motion
echo "Shutting down in 15 seconds...$(date)"
/usr/bin/sleep 15 
/usr/sbin/shutdown now
#Turn off Lights 
python /home/pi/scripts/control_OFF_lights.py
echo "Good Bye $(date)"
