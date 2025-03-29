import requests
from datetime import datetime
from ip_location import current_location, get_city_location
from weather import weekend_forecast, main as get_weather_forecast

# Dictionary of major US cities and their IATA codes
CITY_TO_IATA = {
    'Phoenix': 'PHX',
    'Dallas': 'DFW',
    'Seattle': 'SEA',
    'Los Angeles': 'LAX',
    'Chicago': 'ORD',
    'New York': 'JFK',
    'Miami': 'MIA',
    'San Francisco': 'SFO',
    'Las Vegas': 'LAS',
    'Denver': 'DEN',
    'Houston': 'IAH',
    'Atlanta': 'ATL'
}

def get_iata_code(city):
    """Get IATA code for a city, returns None if not found"""
    return CITY_TO_IATA.get(city)

def get_cool_cities():
    """Get list of cities from weekend_forecast"""
    # First get the weather forecast to populate weekend_forecast
    get_weather_forecast()
    
    # Extract city names from weekend_forecast
    return [city_data['city'] for city_data in weekend_forecast.get('cities', [])]

def get_flights(api_key):
    """
    Get flights between departure city and cool cities from weather forecast.
    Departure city is taken from current_location global variable.
    """
    base_url = "http://api.aviationstack.com/v1/flights"
    
    # First ensure we have current location
    get_city_location()
    
    # Get departure city from global variable
    dep_city = current_location.get('city')
    if not dep_city:
        dep_city = "Tucson"  # Default city
        print(f"Could not determine your city. Using {dep_city} as default.")
    
    # Get departure IATA code
    dep_iata = get_iata_code(dep_city)
    if not dep_iata:
        return {'error': f"Could not find airport code for {dep_city}"}
    
    # Get destination cities from weekend_forecast
    arr_cities = get_cool_cities()
    if not arr_cities:
        return {'error': "No destination cities found in weather forecast"}
    
    all_flights = []
    invalid_cities = []
    
    # Check flights for each arrival city
    for arr_city in arr_cities:
        arr_iata = get_iata_code(arr_city)
        if not arr_iata:
            invalid_cities.append(arr_city)
            continue
        
        # Parameters for the API request
        params = {
            'access_key': api_key,
            'dep_iata': dep_iata,
            'arr_iata': arr_iata
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'error' in data:
                print(f"Error fetching flights to {arr_city}: {data['error']['message']}")
                continue
                
            flights = []
            for flight in data.get('data', []):
                flight_info = {
                    'airline': flight.get('airline', {}).get('name'),
                    'flight_number': flight.get('flight', {}).get('number'),
                    'departure': {
                        'airport': flight.get('departure', {}).get('airport'),
                        'scheduled': flight.get('departure', {}).get('scheduled'),
                        'terminal': flight.get('departure', {}).get('terminal')
                    },
                    'arrival': {
                        'airport': flight.get('arrival', {}).get('airport'),
                        'scheduled': flight.get('arrival', {}).get('scheduled'),
                        'terminal': flight.get('arrival', {}).get('terminal')
                    },
                    'status': flight.get('flight_status'),
                    'arrival_city': arr_city,
                    # 'temperature': next((city_data['max_temp'] 
                    #                   for city_data in weekend_forecast['cities'] 
                    #                   if city_data['city'] == arr_city), None)
                }
                flights.append(flight_info)
            
            all_flights.extend(flights)
            
        except Exception as e:
            print(f"Error fetching flights to {arr_city}: {str(e)}")
            continue
    
    result = {
        'flights': all_flights,
        'dep_city': dep_city,
        'arr_cities': [city for city in arr_cities if city not in invalid_cities],
        'invalid_cities': invalid_cities,
        'forecast_dates': weekend_forecast.get('dates', [])
    }
    
    return result

def print_flights(result):
    """
    Print flights information in a formatted way
    """
    if 'error' in result:
        print(f"Error: {result['error']}")
        return
        
    if not result.get('flights'):
        print("No flights found for any route.")
        return
    
    if result.get('invalid_cities'):
        print("\nWarning: Could not find airport codes for these cities:")
        for city in result['invalid_cities']:
            print(f"- {city}")
    
    print(f"\nFlights from {result['dep_city']} to cities with cool weather:")
    print(f"Weekend dates: {' to '.join(result['forecast_dates'])}")
    print("-" * 80)
    
    # Group flights by arrival city
    for arr_city in result['arr_cities']:
        city_flights = [f for f in result['flights'] if f['arrival_city'] == arr_city]
        if city_flights:
            # print(f"\nDestination: {arr_city} (Forecast: {city_flights[0]['temperature']}°F)")
            print("-" * 40)
            
            for flight in city_flights:
                print(f"Airline: {flight['airline']}")
                print(f"Flight Number: {flight['flight_number']}")
                print(f"Departure: {flight['departure']['airport']}")
                print(f"         Terminal: {flight['departure']['terminal'] or 'N/A'}")
                print(f"         Time: {flight['departure']['scheduled']}")
                print(f"Arrival: {flight['arrival']['airport']}")
                print(f"         Terminal: {flight['arrival']['terminal'] or 'N/A'}")
                print(f"         Time: {flight['arrival']['scheduled']}")
                print(f"Status: {flight['status']}")
                print("-" * 40)

def main():
    api_key = "84a3ecef1d1c8c8da04ff1ec65eb53bf"
    
    print(f"Checking flights from your location to cities with cool weather...")
    result = get_flights(api_key)
    print_flights(result)

if __name__ == "__main__":
    main() 