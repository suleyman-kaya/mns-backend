from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from functools import lru_cache
import time
import simulate_vehicle

app = Flask(__name__)
CORS(app)

CACHE_DURATION = 1  # saniye cinsinden

@lru_cache(maxsize=1)
def read_file(filename, timestamp):
    if not os.path.isfile(filename):
        return None
    try:
        with open(filename, 'r') as file:
            content = file.readline().strip()
            return content if content else None
    except IOError:
        return None

def read_gps_file(timestamp):
    content = read_file('/home/suleymansbackend1/mysite/gps.txt', timestamp)
    if content:
        try:
            lat, lon = map(float, content.split(','))
            return lat, lon
        except ValueError:
            return None, None
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
    timestamp = int(time.time() / CACHE_DURATION)
    lat, lon = read_gps_file(timestamp)
    if lat is None or lon is None:
        return jsonify({'error': 'GPS verisi bulunamadı'}), 404
    simulate_vehicle.update_gps_file()
    return jsonify({'latitude': lat, 'longitude': lon})

@app.route('/calculateEnergyConsumption', methods=['POST'])
def calculate_energy():
    route = request.json.get('route')
    if not route:
        return jsonify({'error': 'Geçersiz rota verisi'}), 400
    energy_consumption = calculate_energy_consumption(route)
    return jsonify({'energyConsumption': energy_consumption})

def read_value_from_file(filename):
    timestamp = int(time.time() / CACHE_DURATION)
    value = read_file(filename, timestamp)
    if value is None:
        return jsonify({'error': f'{filename} verisi bulunamadı'}), 404
    try:
        return jsonify({'value': float(value)})
    except ValueError:
        return jsonify({'error': f'{filename} verisi geçersiz'}), 400

@app.route('/batteryVoltage')
def battery_voltage():
    simulate_vehicle.update_battery_voltage()
    return read_value_from_file('/home/suleymansbackend1/mysite/batteryVoltage.txt')

@app.route('/batteryCurrent')
def battery_current():
    simulate_vehicle.update_battery_current()
    return read_value_from_file('/home/suleymansbackend1/mysite/batteryCurrent.txt')

@app.route('/totalJoulesUsed')
def total_joules_used():
    simulate_vehicle.update_total_joules_used()
    return read_value_from_file('/home/suleymansbackend1/mysite/totalJoulesUsed.txt')

@app.route('/lastCalculatedGPSspeed')
def last_calculated_gps_speed():
    simulate_vehicle.update_last_calculated_gps_speed()
    return read_value_from_file('/home/suleymansbackend1/mysite/lastCalculatedGPSspeed.txt')


if __name__ == '__main__':
    # Flask'ı başlat
    app.run(debug=False, threaded=True)