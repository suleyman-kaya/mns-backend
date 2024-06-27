from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from functools import lru_cache
import time
from energy_calculation import calculate_energy_consumption

app = FastAPI()

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dikkat: Prodüksiyonda spesifik originler belirtilmeli
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GPS_FILE = 'gps.txt'
GPS_CACHE_DURATION = 1  # saniye cinsinden

class Route(BaseModel):
    route: dict

@lru_cache(maxsize=1)
def read_gps_file(timestamp: int):
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
    except (ValueError, IOError) as e:
        print(f"Error reading GPS file: {str(e)}")
        return None, None

@app.get('/gps')
async def gps_data():
    timestamp = int(time.time() / GPS_CACHE_DURATION)
    lat, lon = read_gps_file(timestamp)
    if lat is None or lon is None:
        raise HTTPException(status_code=404, detail="GPS verisi bulunamadı")
    return {'latitude': lat, 'longitude': lon}

@app.post('/calculateEnergyConsumption')
async def calculate_energy(route: Route):
    print(f"Received route data: {route.dict()}")
    if not route.route:
        raise HTTPException(status_code=400, detail="Geçersiz rota verisi")
    try:
        energy_consumption = calculate_energy_consumption(route.route)
        print(f"Calculated energy consumption: {energy_consumption}")
        return {'energyConsumption': energy_consumption}
    except Exception as e:
        print(f"Error in calculate_energy: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="debug")