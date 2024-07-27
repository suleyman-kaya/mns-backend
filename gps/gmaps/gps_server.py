from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from functools import lru_cache
import time

app = Flask(__name__)
CORS(app)

GPS_FILE = 'gps.txt'
GPS_CACHE_DURATION = 1  # saniye cinsinden

@lru_cache(maxsize=1)
def read_gps_file(timestamp):
    """gps.txt dosyasını okuyup enlem ve boylamı döndürür."""
    if not os.path.isfile(GPS_FILE):
        return None, None
    
    try:
        with open(GPS_FILE, 'r') as file:
            line = file.readline().strip()
            if not line:
                return None, None
            lat, lon = map(float, line.split(','))
            return lat, lon
    except (ValueError, IOError):
        return None, None

def calculate_energy_consumption(route):
    distance = sum(leg['distance']['value'] for leg in route['legs'])
    elevation_gain = sum(
        max(0, step['elevation']['endLocation']['lng'] - step['elevation']['startLocation']['lng'])
        for leg in route['legs']
        for step in leg['steps']
        if 'elevation' in step
    )
    return distance * 0.001 + elevation_gain * 0.01

@app.route('/gps')
def gps_data():
    timestamp = int(time.time() / GPS_CACHE_DURATION)
    lat, lon = read_gps_file(timestamp)
    if lat is None or lon is None:
        return jsonify({'error': 'GPS verisi bulunamadı'}), 404
    return jsonify({'latitude': lat, 'longitude': lon})

@app.route('/calculateEnergyConsumption', methods=['POST'])
def calculate_energy():
    route = request.json.get('route')
    if not route:
        return jsonify({'error': 'Geçersiz rota verisi'}), 400
    energy_consumption = calculate_energy_consumption(route)
    return jsonify({'energyConsumption': energy_consumption})

# Yeni eklenen endpoint'ler
@app.route('/batteryVoltage')
def battery_voltage():
    return jsonify({'value': 123000})

@app.route('/batteryCurrent')
def battery_current():
    return jsonify({'value': 123000})

@app.route('/totalJoulesUsed')
def total_joules_used():
    return jsonify({'value': 123000})

@app.route('/lastCalculatedGPSspeed')
def last_calculated_gps_speed():
    return jsonify({'value': 123000})

if __name__ == '__main__':
    app.run(debug=False, threaded=True)
