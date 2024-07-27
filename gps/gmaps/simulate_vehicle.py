import random
import os
import time

def update_gps_file():
    """Updates the gps.txt file with new latitude and longitude values."""
    if not os.path.isfile('gps.txt'):
        print("gps.txt file does not exist.")
        return

    with open('gps.txt', 'r') as file:
        line = file.readline().strip()
        if not line:
            print("gps.txt file is empty.")
            return
        
        lat, lon = line.split(',')
        lat = float(lat)
        lon = float(lon)

    # Generate a random number between 0 and 999
    random_number = random.randint(0, 999)
    increment = 0.0001 + (random_number / 100000)

    # Update latitude and longitude
    new_lat = round(lat + increment, 8)
    new_lon = round(lon + increment, 8)

    with open('gps.txt', 'w') as file:
        file.write(f"{new_lat},{new_lon}\n")

    print(f"Updated GPS coordinates: {new_lat}, {new_lon}")

def update_file_with_random_float(filename):
    """Updates the specified file with a random 2 or 3 decimal float value."""
    value = round(random.uniform(10.0, 999.99), 2)
    with open(filename, 'w') as file:
        file.write(f"{value}\n")
    print(f"Updated {filename} with value: {value}")

def update_battery_voltage():
    update_file_with_random_float('batteryVoltage.txt')

def update_battery_current():
    update_file_with_random_float('batteryCurrent.txt')

def update_total_joules_used():
    update_file_with_random_float('totalJoulesUsed.txt')

def update_last_calculated_gps_speed():
    update_file_with_random_float('lastCalculatedGPSspeed.txt')

if __name__ == '__main__':
    while True:
        update_gps_file()
        update_battery_voltage()
        update_battery_current()
        update_total_joules_used()
        update_last_calculated_gps_speed()
        time.sleep(1)  # Wait for 1 second before the next update
