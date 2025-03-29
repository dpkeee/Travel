import requests
import json
import time

# Global variables to store location information
current_location = {
    'city': None,
    'state': None
}

def get_current_ip():
    """
    Get the current public IP address dynamically
    """
    try:
        # Using ipify API to get current IP
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        response.raise_for_status()
        return response.json()['ip']
    except Exception as e:
        print(f"Error getting IP address: {str(e)}")
        return None

def get_location_from_ip(ip_address=None):
    """
    Get location from IP address and store in global variable.
    If no IP provided, uses the client's IP.
    Returns tuple (city, state) and updates global current_location.
    """
    global current_location
    
    try:
        # If no IP provided, get current IP
        if not ip_address:
            ip_address = get_current_ip()
            if not ip_address:
                raise Exception("Could not determine IP address")

        # Construct the API URL
        url = f"http://ip-api.com/json/{ip_address}"
        
        # Make the request
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Check if the request was successful
        if data.get('status') == 'fail':
            current_location = {'city': None, 'state': None}
            return None, None
        
        # Extract city and state
        city = data.get('city')
        state = data.get('regionName')
        
        # Update global variable
        current_location.update({
            'city': city,
            'state': state
        })
        
        return city, state
        
    except Exception as e:
        print(f"Error getting location: {str(e)}")
        current_location = {'city': None, 'state': None}
        return None, None

def get_city_location(ip_address=None):
    """
    Get city and state for an IP address.
    Updates global current_location and returns tuple (city, state).
    If no IP provided, gets current IP automatically.
    """
    if not ip_address:
        ip_address = get_current_ip()
    return get_location_from_ip(ip_address)

def test_ip_location():
    """Test function to demonstrate usage"""
    # Test with dynamic IP
    print("\nTesting with current IP:")
    current_ip = get_current_ip()
    print(f"Current IP: {current_ip}")
    city, state = get_city_location()
    print(f"Your location - City: {city}, State: {state}")
    print(f"Global variable - City: {current_location['city']}, State: {current_location['state']}")
    
    # Test with specific IP
    test_ip = "8.8.8.8"
    print(f"\nTesting with specific IP ({test_ip}):")
    city, state = get_city_location(test_ip)
    print(f"Location - City: {city}, State: {state}")
    print(f"Global variable - City: {current_location['city']}, State: {current_location['state']}")

if __name__ == "__main__":
    print("IP Location Tester")
    print("=" * 50)
    test_ip_location() 