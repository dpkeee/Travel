import requests
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import json
from ip_location import current_location, get_city_location

# Global variables
weekend_forecast = {
    'dates': [],
    'cities': []
}

# Constants
FALLBACK_CITY = "Tucson, Arizona"
MAJOR_CITIES = [
    "Los Angeles", "Las Vegas", "Salt Lake City", "Denver",
    "Albuquerque", "San Diego", "El Paso", "San Antonio",
    "Houston", "Dallas", "Oklahoma City", "Kansas City"
]

# Test data
TEST_CITIES = [
    {'city': 'San Diego'},
    {'city': 'Los Angeles'},
    {'city': 'Las Vegas'},
    {'city': 'Denver'}
]

def get_test_forecast_data():
    """Return test data for weekend_forecast when API fails"""
    today = datetime.now()
    saturday = today + timedelta(days=(5 - today.weekday() + 1))
    sunday = saturday + timedelta(days=1)
    
    return {
        'dates': [
            saturday.strftime('%Y-%m-%d'),
            sunday.strftime('%Y-%m-%d')
        ],
        'cities': TEST_CITIES,
        'error': None,
        'origin': FALLBACK_CITY
    }

def get_city_coordinates(city_name):
    """Get coordinates for a given city"""
    geolocator = Nominatim(user_agent="my_weather_app")
    location = geolocator.geocode(city_name)
    if location:
        return (location.latitude, location.longitude)
    return None

def get_cities_in_range(center_coords, radius_miles):
    """Get cities within specified radius"""
    cities_in_range = []
    for city in MAJOR_CITIES:
        coords = get_city_coordinates(city)
        if coords:
            distance = geodesic(center_coords, coords).miles
            if distance <= radius_miles:
                cities_in_range.append((city, coords, distance))
    return cities_in_range

def get_weekend_weather(lat, lon):
    """Get weekend weather forecast using National Weather Service API"""
    try:
        points_url = f"https://api.weather.gov/points/{lat},{lon}"
        points_response = requests.get(points_url, headers={
            'User-Agent': 'WeatherForecastApp/1.0 (your@email.com)'
        })
        points_response.raise_for_status()
        points_data = points_response.json()
        
        forecast_url = points_data['properties']['forecast']
        forecast_response = requests.get(forecast_url, headers={
            'User-Agent': 'WeatherForecastApp/1.0 (your@email.com)'
        })
        forecast_response.raise_for_status()
        data = forecast_response.json()
        
        today = datetime.now()
        saturday = today + timedelta(days=(5 - today.weekday() + 1))
        sunday = saturday + timedelta(days=1)
        weekend_dates = [saturday.strftime('%Y-%m-%d'), sunday.strftime('%Y-%m-%d')]
        
        weekend_temps = []
        weekend_found_dates = []
        
        for period in data['properties']['periods']:
            forecast_date = datetime.fromisoformat(period['startTime']).strftime('%Y-%m-%d')
            if forecast_date in weekend_dates:
                weekend_temps.append(period['temperature'])
                weekend_found_dates.append(forecast_date)
        
        return (max(weekend_temps), weekend_found_dates) if weekend_temps else (None, [])
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {str(e)}")
        return None, []
    except (KeyError, ValueError) as e:
        print(f"Error parsing weather data: {str(e)}")
        return None, []

def update_forecast_with_test_data():
    """Update global weekend_forecast with test data"""
    global weekend_forecast
    weekend_forecast.update(get_test_forecast_data())

def main():
    global weekend_forecast
    get_city_location()
    
    try:
        if (current_location.get('city') and 
            current_location.get('state')):
            origin_city = f"{current_location['city']}, {current_location['state']}"
        else:
            origin_city = FALLBACK_CITY
        
        origin_coords = get_city_coordinates(origin_city)
        
        if not origin_coords:
            print(f"Could not find coordinates for {origin_city}, using test data...")
            update_forecast_with_test_data()
            return weekend_forecast
        
        print(f"Finding cities within 1000 miles of {origin_city}...")
        nearby_cities = get_cities_in_range(origin_coords, 1000)
        
        print("\nChecking weekend temperatures...")
        cool_cities = []
        weekend_dates = []
        
        for city, coords, distance in nearby_cities:
            try:
                max_temp, dates = get_weekend_weather(coords[0], coords[1])
                if max_temp and max_temp < 100:
                    cool_cities.append({'city': city})
                    if not weekend_dates:
                        weekend_dates = dates
            except Exception as e:
                continue
        
        if not cool_cities or not weekend_dates:
            print("No weather data found, using test data...")
            update_forecast_with_test_data()
            return weekend_forecast
        
        weekend_forecast.update({
            'dates': weekend_dates,
            'cities': cool_cities,
            'error': None,
            'origin': origin_city
        })
        return weekend_forecast
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Using test data instead...")
        update_forecast_with_test_data()
        return weekend_forecast

if __name__ == "__main__":
    result = main()
    if result['error']:
        print(result['error'])
    else:
        print(f"\nWeekend dates: {result['dates'][0]} to {result['dates'][1]}")
        print(f"\nCities within 1000 miles of {result['origin']} with temperatures below 100°F this weekend:")
        for city_data in result['cities']:
            print(f"{city_data['city']}")
