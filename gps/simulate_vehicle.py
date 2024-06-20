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
    new_lat = round(lat - increment, 8)
    new_lon = round(lon - increment, 8)

    with open('gps.txt', 'w') as file:
        file.write(f"{new_lat},{new_lon}\n")

    print(f"Updated GPS coordinates: {new_lat}, {new_lon}")

if __name__ == '__main__':
    while True:
        update_gps_file()
        time.sleep(1)  # Wait for 1 second before the next update
