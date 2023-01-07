from PyTado.interface import Tado
from settings import TADO_USERNAME, TADO_PASSWORD
from datetime import datetime, timezone

def get_connection():
    return Tado(TADO_USERNAME, TADO_PASSWORD)

def get_now():
    return datetime.now().replace(tzinfo=timezone.utc).isoformat()

# Relevant methods
# getHomeState() -> obj of current home state
# getWeather() -> obj of current weather state
# getZones() -> list of zones with IDs
# getClimate(zoneId) -> obj of climate for a given zone

# Get current state of home in as a list in a standardised format
# of a dict with keys:
# - location
# - location_id
# - measurement_type
# - measurement_value_float
# - measurement_value_string
# - timestamp
def get_current_state():
    conn = get_connection()

    all_values = []

    # Get home state
    home_state_raw = conn.getHomeState()
    all_values.append({
        'location': 'Home',
        'location_id': 0,
        'measurement_type': 'HOME_STATE',
        'measurement_value_float': None,
        'measurement_value_string': home_state_raw['presence'],
        'timestamp': get_now()
    })

    # Get weather
    weather_raw = conn.getWeather()
    all_values.append({
        'location': 'Home',
        'location_id': 0,
        'measurement_type': 'WEATHER_TEMPERATURE',
        'measurement_value_float': weather_raw['outsideTemperature']['celsius'],
        'measurement_value_string': None,
        'timestamp': get_now()
    })

    all_values.append({
        'location': 'Home',
        'location_id': 0,
        'measurement_type': 'WEATHER_STATE',
        'measurement_value_float': None,
        'measurement_value_string': weather_raw['weatherState']['value'],
        'timestamp': get_now()
    })

    all_values.append({
        'location': 'Home',
        'location_id': 0,
        'measurement_type': 'WEATHER_SOLAR_INTENSITY',
        'measurement_value_float': weather_raw['solarIntensity']['percentage'],
        'measurement_value_string': None,
        'timestamp': get_now()
    })

    # Get zones
    zones = conn.getZones()

    # Get climate for each zone
    for zone in zones:
        zone_state = conn.getZoneState(zone=zone['id'])

        all_values.append({
            'location': zone['name'],
            'location_id': zone['id'],
            'measurement_type': 'ZONE_TEMPERATURE',
            'measurement_value_float': zone_state.current_temp,
            'measurement_value_string': None,
            'timestamp': zone_state.current_temp_timestamp
        })

        all_values.append({
            'location': zone['name'],
            'location_id': zone['id'],
            'measurement_type': 'ZONE_TEMPERATURE_TARGET',
            'measurement_value_float': zone_state.target_temp,
            'measurement_value_string': None,
            'timestamp': get_now()
        })

        all_values.append({
            'location': zone['name'],
            'location_id': zone['id'],
            'measurement_type': 'ZONE_HUMIDITY',
            'measurement_value_float': zone_state.current_humidity,
            'measurement_value_string': None,
            'timestamp': zone_state.current_humidity_timestamp
        })

    return all_values