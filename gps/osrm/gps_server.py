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
    # OSRM API'sinden gelen rota verisine göre düzenlendi
    distance = route['distance']  # metre cinsinden
    
    # Yükseklik farkını hesaplamak için koordinatları kullanıyoruz
    coordinates = route['geometry']['coordinates']
    elevation_gain = sum(
        max(0, coordinates[i+1][2] - coordinates[i][2])
        for i in range(len(coordinates) - 1)
        if len(coordinates[i]) > 2 and len(coordinates[i+1]) > 2
    )
    
    # Basit bir enerji tüketimi formülü (gerçek dünyada daha karmaşık olabilir)
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
    try:
        energy_consumption = calculate_energy_consumption(route)
        return jsonify({'energyConsumption': energy_consumption})
    except Exception as e:
        return jsonify({'error': f'Enerji tüketimi hesaplanırken hata oluştu: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=False, threaded=True)
