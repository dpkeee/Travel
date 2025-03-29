from ip_location import get_city_location, current_city
from weather import main as get_weather_forecast

def main():
    # Get the user's city based on IP
    user_city = get_city_location()
    
    if not user_city:
        print("Could not determine your city. Using default city (Phoenix).")
        user_city = "Phoenix"
    
    print(f"Your current city: {user_city}")
    
    # Get weather forecast
    result = get_weather_forecast()
    
    # Display results
    if result['error']:
        print(result['error'])
    else:
        print(f"\nWeekend dates: {result['dates'][0]} to {result['dates'][1]}")
        print(f"\nCities within 1000 miles of {user_city} with temperatures below 100°F this weekend:")
        for city_data in result['cities']:
            print(f"{city_data['city']}: {city_data['max_temp']}°F (Distance: {city_data['distance']} miles)")

if __name__ == "__main__":
    main()
