from ip_location import get_city_location
from weather import get_weather_forecast
from flight_checker import get_flights
import google.generativeai as genai

def main():
    genai.configure(api_key='AIzaSyBv1k0vjAOT_jqZmRiV1n9OVLnMrSOz5_o')
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    system_prompt = '''You are an travel agent which helps in getting flight details for cool destination from my origin. Respond with EXACTLY ONE of these formats:
1. FUNCTION_CALL: python_function_name|input
2. FINAL_ANSWER: [flight_data]

where python_function_name is one of the following:
1. get_city_location() - It gets the IP address from the system and returns the current city & state based on ip address
2. get_weather_forecast() - It takes current city & state and returns the date and destinations near the city & state 
3. get_flights() - It takes date, current city, destinations and returns flight details
DO NOT include multiple responses. Give ONE response at a time.'''

    # Current query  
    query = "Give me the flight details for cool destinations from my current location"

    # Initialize variables
    iteration = 0
    max_iterations = 3
    last_response = None
    iteration_response = []

    while iteration < max_iterations:
        print(f"\n--- Iteration {iteration + 1} ---")
        if last_response == None:
            current_query = query
        else:
            current_query = current_query + "\n\n" + " ".join(iteration_response)
            current_query = current_query + "  What should I do next?"

        # Get model's response
        prompt = f"{system_prompt}\n\nQuery: {current_query}"
        response = model.generate_content(contents=prompt)

        response_text = response.text.strip()
        print(f"LLM Response: {response_text}")

        if response_text.startswith("FUNCTION_CALL:"):
            response_text = response.text.strip()
            _, function_info = response_text.split(":", 1)
            func_name, params = [x.strip() for x in function_info.split("|", 1)]
            iteration_result = function_caller(func_name, params)
            
            last_response = iteration_result
            iteration_response.append(f"In the {iteration + 1} iteration you called {func_name} with {params} parameters, and the function returned {iteration_result}.")

        elif response_text.startswith("FINAL_ANSWER:"):
            print("\n=== Agent Execution Complete ===")
            # Return the last_response which should contain the flight data
            return last_response

        #print(f"  Result of iteration {iteration}: {last_response}")
        iteration += 1
        print('iteration_response....', iteration)
    
    # If we reach max iterations without getting FINAL_ANSWER, return the last result
    return last_response

def function_caller(func_name, params):
    """Simple function caller that maps function names to actual functions"""
    function_map = {
        "get_city_location": get_city_location,
        "get_weather_forecast": get_weather_forecast,
        "get_flights": get_flights
    }

    if func_name in function_map:
        return function_map[func_name](params)
    else:
        return f"Function {func_name} not found"
    
if __name__ == "__main__":
    main()
