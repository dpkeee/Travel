import requests
from datetime import datetime

def get_flights(api_key, dep_city="Phoenix", arr_city="Dallas"):
    """
    Get flights between two cities using Aviationstack API
    """
    base_url = "http://api.aviationstack.com/v1/flights"
    
    # Parameters for the API request
    params = {
        'access_key': api_key,
        'dep_iata': 'PHX',  # Phoenix Sky Harbor International Airport
        'arr_iata': 'DFW',  # Dallas/Fort Worth International Airport
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'error' in data:
            return {'error': data['error']['message']}
            
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
                'status': flight.get('flight_status')
            }
            flights.append(flight_info)
            
        return {'flights': flights}
        
    except requests.exceptions.RequestException as e:
        return {'error': f"API request failed: {str(e)}"}
    except Exception as e:
        return {'error': f"An error occurred: {str(e)}"}

def print_flights(result):
    """
    Print flights information in a formatted way
    """
    if 'error' in result:
        print(f"Error: {result['error']}")
        return
        
    if not result['flights']:
        print("No flights found for this route.")
        return
        
    print("\nFlights from Phoenix to Dallas:")
    print("-" * 80)
    
    for flight in result['flights']:
        print(f"Airline: {flight['airline']}")
        print(f"Flight Number: {flight['flight_number']}")
        print(f"Departure: {flight['departure']['airport']}")
        print(f"         Terminal: {flight['departure']['terminal'] or 'N/A'}")
        print(f"         Time: {flight['departure']['scheduled']}")
        print(f"Arrival: {flight['arrival']['airport']}")
        print(f"         Terminal: {flight['arrival']['terminal'] or 'N/A'}")
        print(f"         Time: {flight['arrival']['scheduled']}")
        print(f"Status: {flight['status']}")
        print("-" * 80)

def main():
    api_key = "84a3ecef1d1c8c8da04ff1ec65eb53bf"  # Your API key
    
    print("Checking flights between Phoenix and Dallas...")
    result = get_flights(api_key)
    print_flights(result)

if __name__ == "__main__":
    main() 