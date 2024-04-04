import datetime
import subprocess
import shutil

# Function to run heliocron report command and parse the output
def get_civil_dawn_dusk():
    heliocron_report = subprocess.check_output(["heliocron", "report"], text=True)
    lines = heliocron_report.split('\n')

    # Extract civil dawn and dusk times
    civil_dawn_line = [line for line in lines if "Civil dawn is at:" in line][0]
    civil_dusk_line = [line for line in lines if "Civil dusk is at:" in line][0]

    civil_dawn_time_str = civil_dawn_line.split(" ")[-2]  # Extracting time part
    civil_dusk_time_str = civil_dusk_line.split(" ")[-2]  # Extracting time part

    return civil_dawn_time_str, civil_dusk_time_str

# Define the location coordinates
latitude = 52.752845
longitude = -3.253449

# Get today's date
today = datetime.date.today()

# Get civil dawn and dusk times from heliocron report
civil_dawn_time, civil_dusk_time = get_civil_dawn_dusk()

print ("civil_dawn_time, civil_dusk_time ", civil_dawn_time, civil_dusk_time)
# Generate Witty Pi schedule
witty_pi_schedule = f"""
# Turn on Raspberry Pi at civil dusk, keep ON state for 5 minutes
BEGIN {today.year}-{today.month:02d}-{today.day:02d} {civil_dusk_time}
END {today.year}-{today.month:02d}-{today.day:02d} 23:59:59
ON M5

# Turn off Raspberry Pi at civil dawn, keep OFF state for 15 minutes
BEGIN {today.year}-{today.month:02d}-{today.day:02d} {civil_dawn_time}
END {today.year}-{today.month:02d}-{today.day:02d} 23:59:59
OFF M15
"""

# Specify the target path for the schedule file
target_path = '/home/pi/wittypi'

# Save the schedule to the target path
schedule_file_path = f'{target_path}schedule.wpi'

# Save the schedule to a file
with open('schedule_file_path', 'w') as file:
    file.write(witty_pi_schedule)

print(f"Witty Pi schedule generated and saved to {schedule_file_path}.")

# Move the schedule file to the target path
shutil.move('witty_pi_schedule.txt', schedule_file_path)

# Run the runschedule.sh script from the target path
subprocess.run(["bash", f"{target_path}runScript.sh"])