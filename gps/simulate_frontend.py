import requests
import time

def fetch_gps_data():
    """Fetches GPS data from the /gps endpoint and prints it."""
    try:
        response = requests.get('http://localhost:5000/gps')
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        print(f"Latitude: {data['latitude']}, Longitude: {data['longitude']}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching GPS data: {e}")

if __name__ == '__main__':
    while True:
        fetch_gps_data()
        time.sleep(1)  # Wait for 1 second before the next request
