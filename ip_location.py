import requests
import json
import time

# Modify the global variable to store both city and state
current_location = {
    'city': None,
    'state': None
}

def get_location_by_ip(ip_address=None):
    """
    Get location information for an IP address.
    If no IP is provided, it returns the location of the client's IP.
    """
    try:
        # Construct the API URL - using a different free IP geolocation API
        # as freegeoip.app seems to be unreliable
        if ip_address:
            url = f"http://ip-api.com/json/{ip_address}"
        else:
            url = "http://ip-api.com/json/"
        
        # Make the request
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Check if the request was successful
        if data.get('status') == 'fail':
            return {'error': f"Failed to get location: {data.get('message', 'Unknown error')}"}
        
        # Create a formatted result
        location_info = {
            'ip': ip_address or data.get('query'),
            'city': data.get('city', 'Unknown'),
            'region': data.get('regionName', 'Unknown'),
            'country': data.get('country', 'Unknown'),
            'latitude': data.get('lat', 0),
            'longitude': data.get('lon', 0),
            'timezone': data.get('timezone', 'Unknown'),
            'isp': data.get('isp', 'Unknown')
        }
        
        return location_info
    
    except requests.exceptions.Timeout:
        return {'error': "Request timed out"}
    except requests.exceptions.RequestException as e:
        return {'error': f"Failed to fetch location data: {str(e)}"}
    except (KeyError, json.JSONDecodeError) as e:
        return {'error': f"Failed to parse location data: {str(e)}"}

def print_location_info(location_info):
    """Print the location information in a formatted way"""
    if 'error' in location_info:
        print(f"Error: {location_info['error']}")
        return
    
    print("\nLocation Information:")
    print("-" * 50)
    print(f"IP Address: {location_info['ip']}")
    print(f"City: {location_info['city']}")
    print(f"Region: {location_info['region']}")
    print(f"Country: {location_info['country']}")
    print(f"Coordinates: {location_info['latitude']}, {location_info['longitude']}")
    print(f"Timezone: {location_info['timezone']}")
    print(f"ISP: {location_info['isp']}")

def test_ips():
    """Test function with various IP addresses"""
    test_cases = [
        None,           # Your current IP
        "8.8.8.8",     # Google DNS
        "1.1.1.1",     # Cloudflare DNS
        "17.253.144.10", # Apple
        "invalid.ip",   # Invalid IP to test error handling
        "192.168.1.1"  # Local IP to test error handling
    ]
    
    for ip in test_cases:
        print(f"\nTesting{'your current IP' if ip is None else f' IP: {ip}'}")
        location = get_location_by_ip(ip)
        print_location_info(location)
        time.sleep(1)  # Add delay to avoid rate limiting

def get_city_location(ip_address=None):
    """
    Get city and state for an IP address, store it in global variable and return it.
    If no IP is provided, it returns the location of the client's IP.
    Returns tuple (city, state) if successful, (None, None) if unsuccessful.
    """
    global current_location
    
    try:
        # Construct the API URL
        if ip_address:
            url = f"http://ip-api.com/json/{ip_address}"
        else:
            url = "http://ip-api.com/json/"
        
        # Make the request
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Check if the request was successful
        if data.get('status') == 'fail':
            current_location = {'city': None, 'state': None}
            return None, None
        
        # Store and return the city and state
        city = data.get('city', None)
        state = data.get('regionName', None)
        
        current_location = {
            'city': city,
            'state': state
        }
        
        return city, state
    
    except:
        current_location = {'city': None, 'state': None}
        return None, None

def main():
    # Example usage
    test_ips()

if __name__ == "__main__":
    print("IP Geolocation Tester")
    print("=" * 50)
    main() 