cdef double _calculate_energy_consumption(dict route):
    cdef double distance = 0.0
    cdef double elevation_gain = 0.0
    cdef double start_elevation, end_elevation

    for leg in route['legs']:
        distance += leg['distance']['value']
        for step in leg['steps']:
            if 'elevation' in step:
                start_elevation = step['elevation']['startLocation']['lng']
                end_elevation = step['elevation']['endLocation']['lng']
                if end_elevation > start_elevation:
                    elevation_gain += end_elevation - start_elevation

    return distance * 0.001 + elevation_gain * 0.01

def calculate_energy_consumption(route):
    return _calculate_energy_consumption(route)