from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Tüm origin'lere izin ver

def read_gps_file():
    """gps.txt dosyasını okuyup enlem ve boylamı döndürür."""
    if not os.path.isfile('gps.txt'):
        return None, None

    with open('gps.txt', 'r') as file:
        line = file.readline().strip()
        if not line:
            return None, None

        lat, lon = line.split(',')
        return float(lat), float(lon)

def calculate_energy_consumption(route):
    distance = 0
    elevation_gain = 0

    for leg in route['legs']:
        distance += leg['distance']['value']

        for step in leg['steps']:
            if 'elevation' in step:
                elevation_diff = step['elevation']['endLocation']['lng'] - step['elevation']['startLocation']['lng']
                if elevation_diff > 0:
                    elevation_gain += elevation_diff

    return distance * 0.001 + elevation_gain * 0.01

@app.route('/gps')
def gps_data():
    lat, lon = read_gps_file()
    if lat is None or lon is None:
        return jsonify({'error': 'GPS verisi bulunamadı'}), 404
    data = {'latitude': lat, 'longitude': lon}
    return jsonify(data)

@app.route('/calculateEnergyConsumption', methods=['POST'])
def calculate_energy():
    data = request.get_json()
    route = data.get('route')
    energy_consumption = calculate_energy_consumption(route)
    return jsonify({'energyConsumption': energy_consumption})

if __name__ == '__main__':
    app.run(debug=True)
