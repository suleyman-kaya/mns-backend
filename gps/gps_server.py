from flask import Flask, jsonify
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

@app.route('/gps')
def gps_data():
    lat, lon = read_gps_file()
    if lat is None or lon is None:
        return jsonify({'error': 'GPS verisi bulunamadı'}), 404
    data = {'latitude': lat, 'longitude': lon}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
