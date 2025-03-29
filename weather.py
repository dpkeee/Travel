import requests
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import json

# Add global variable at the top
weekend_forecast = {
    'dates': [],
    'cities': []
}

def get_city_coordinates(city_name):
    geolocator = Nominatim(user_agent="my_weather_app")
    location = geolocator.geocode(city_name)
    if location:
        return (location.latitude, location.longitude)
    return None

def get_cities_in_range(center_coords, radius_miles):
    # This is a simplified list of major US cities
    major_cities = [
        "Los Angeles", "Las Vegas", "Salt Lake City", "Denver",
        "Albuquerque", "San Diego", "El Paso", "San Antonio",
        "Houston", "Dallas", "Oklahoma City", "Kansas City"
    ]
    
    cities_in_range = []
    for city in major_cities:
        coords = get_city_coordinates(city)
        if coords:
            distance = geodesic(center_coords, coords).miles
            if distance <= radius_miles:
                cities_in_range.append((city, coords, distance))
    
    return cities_in_range

def get_weekend_weather(lat, lon):
    # Get forecast from Open-Meteo
    url = (f"https://api.open-meteo.com/v1/forecast?"
           f"latitude={lat}&longitude={lon}"
           f"&temperature_unit=fahrenheit"
           f"&daily=temperature_2m_max"
           f"&timezone=America/Phoenix")
    
    response = requests.get(url)
    data = response.json()
    
    # Find next weekend's dates
    today = datetime.now()
    saturday = today + timedelta(days=(5 - today.weekday() + 1))
    sunday = saturday + timedelta(days=1)
    weekend_dates = [saturday.strftime('%Y-%m-%d'), sunday.strftime('%Y-%m-%d')]
    
    # Get weekend temperatures
    daily_dates = data['daily']['time']
    daily_temps = data['daily']['temperature_2m_max']
    
    weekend_temps = []
    weekend_found_dates = []
    for date, temp in zip(daily_dates, daily_temps):
        if date in weekend_dates:
            weekend_temps.append(temp)
            weekend_found_dates.append(date)
    
    return (max(weekend_temps), weekend_found_dates) if weekend_temps else (None, [])

def main():
    origin_coords = get_city_coordinates("Phoenix, Arizona")
    
    if not origin_coords:
        return {
            'error': "Could not find coordinates for Origin city",
            'dates': [],
            'cities': []
        }
    
    print("Finding cities within 1000 miles of Origin...")
    nearby_cities = get_cities_in_range(origin_coords, 1000)
    
    print("\nChecking weekend temperatures...")
    cool_cities = []
    weekend_dates = []
    
    for city, coords, distance in nearby_cities:
        try:
            max_temp, dates = get_weekend_weather(coords[0], coords[1])
            if max_temp and max_temp < 100:
                cool_cities.append({
                    'city': city,
                    'distance': round(distance, 1),
                    'max_temp': round(max_temp, 1)
                })
                if not weekend_dates:
                    weekend_dates = dates
        except Exception as e:
            continue
    
    # Store and return results
    result = {
        'dates': weekend_dates,
        'cities': sorted(cool_cities, key=lambda x: x['distance']),
        'error': None,
        'origin': "Phoenix, Arizona"  # Added origin city to result
    }
    
    global weekend_forecast
    weekend_forecast = result
    return result

if __name__ == "__main__":
    result = main()
    if result['error']:
        print(result['error'])
    else:
        print(f"\nWeekend dates: {result['dates'][0]} to {result['dates'][1]}")
        print(f"\nCities within 1000 miles of Origin with temperatures below 100°F this weekend:")
        for city_data in result['cities']:
            print(f"{city_data['city']}: {city_data['max_temp']}°F (Distance: {city_data['distance']} miles)")
