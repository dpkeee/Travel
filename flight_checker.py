import requests
from datetime import datetime
import json
import code
import os
from dotenv import load_dotenv
from ip_location import current_location, get_city_location
from weather import weekend_forecast, get_weather_forecast

# Load environment variables
load_dotenv()

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
    'Atlanta': 'ATL',
    'San Diego': 'SAN'
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

def get_flights(input_data):
    print('input_data', input_data)
    try:
        # Use global variables
        if not current_location.get('city'):
            return {'error': 'Current location not found'}
        
        if not weekend_forecast.get('cities') or not weekend_forecast.get('dates'):
            return {'error': 'Weather forecast data not found'}
        
        # Get data from global variables
        current_city = current_location['city']
        destinations = weekend_forecast['cities']
        date = weekend_forecast['dates']
        
        # Extract city names from destinations
        destination_cities = [city["city"] for city in destinations]
        
        if not current_city or not destination_cities:
            return {'error': 'Missing required data: current_city or destinations'}
            
    except Exception as e:
        print(f"Error accessing global variables: {str(e)}")
        return {'error': f'Error accessing global variables: {str(e)}'}

    # Get API key from environment variable
    api_key = os.getenv('AVIATIONSTACK_API_KEY')
    if not api_key:
        return {'error': 'API key not found in environment variables'}
        
    base_url = "http://api.aviationstack.com/v1/flights"
    
    # Get departure IATA code
    dep_iata = get_iata_code(current_city)
    if not dep_iata:
        return {'error': f"Could not find airport code for {current_city}"}
    
    if not destination_cities:
        return {'error': "No destination cities found in weather forecast"}
    
    all_flights = []
    invalid_cities = []
    
    # Check flights for each arrival city
    for arr_city in destination_cities:
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
            
            print(f"API Response for {arr_city}: {data}")  # Debug log
            
            if 'error' in data:
                print(f"Error fetching flights to {arr_city}: {data['error']['message']}")
                continue
            
            # Check if data exists and has flights
            if not data.get('data'):
                print(f"No flights found for {arr_city}")
                continue
                
            flights = []
            for flight in data.get('data', []):
                # Only include flights that have both departure and arrival info
                if flight.get('departure') and flight.get('arrival'):
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
                    }
                    flights.append(flight_info)
            
            if flights:
                print(f"Found {len(flights)} flights for {arr_city}")
                all_flights.extend(flights)
            else:
                print(f"No valid flights found for {arr_city}")
            
        except Exception as e:
            print(f"Error fetching flights to {arr_city}: {str(e)}")
            continue
    
    if not all_flights:
        return {'error': "No flights found for any route"}
    
    result = {
        'flights': all_flights,
        'dep_city': current_city,
        'arr_cities': [city for city in destination_cities if city not in invalid_cities],
        'invalid_cities': invalid_cities,
        'forecast_dates': date
    }
    
    print(f"Total flights found: {len(all_flights)}")
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
            print("-" * 40)
            print(f"Top 3 flights to {arr_city}:")
            # Only take first 3 flights
            for flight in city_flights[:3]:
                print(f"Airline: {flight['airline']}")
                # print(f"Flight Number: {flight['flight_number']}")
                # print(f"Departure: {flight['departure']['airport']}")
                # print(f"         Terminal: {flight['departure']['terminal'] or 'N/A'}")
                # print(f"         Time: {flight['departure']['scheduled']}")
                # print(f"Arrival: {flight['arrival']['airport']}")
                # print(f"         Terminal: {flight['arrival']['terminal'] or 'N/A'}")
                # print(f"         Time: {flight['arrival']['scheduled']}")
                # print(f"Status: {flight['status']}")
                print("-" * 40)
