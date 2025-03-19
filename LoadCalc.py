import requests

# WeatherAPI configuration
API_KEY = '67464963be984693b6374536240710'  # Replace with your WeatherAPI key
BASE_URL = "http://api.weatherapi.com/v1/current.json"

def fetch_city_climate(city):
    params = {
        'key': API_KEY,
        'q': city  # City name
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

# Error handling if city doesn't exist
    if 'error' in data:
        print(f"Error: {data['error']['message']} for city: {city}")
        return None, None

    location_data = data.get('location', {})
    fetched_city = location_data.get('name', '').lower()

    if fetched_city != city.lower():
        print(f"Error: Fetched data for '{fetched_city}', which does not match the input city '{city}'")
        return None, None

    temperature = data['current'].get('temp_c')
    humidity = data['current'].get('humidity')

    if temperature is None or humidity is None:
        print(f"Incomplete data for the city: {city}")
        return None, None

    return temperature, humidity

def sensible_heat_load(U_value, area, delta_temp):
    return U_value * area * delta_temp


def latent_heat_load(num_occupants, ventilation_rate, humidity_diff):
    return 0.215 * num_occupants * ventilation_rate * humidity_diff

def calculate_heat_load(city, area, U_value, num_occupants, ventilation_rate, indoor_temp):
    # Fetch the city climate data
    outdoor_temp, outdoor_humidity = fetch_city_climate(city)

    if outdoor_temp is None or outdoor_humidity is None:
        print("Could not retrieve climate data for the city.")
        return None

    # Calculate delta temperature (for sensible heat)
    delta_temp = indoor_temp - outdoor_temp

    # Sensible heat load calculation
    sensible_load = sensible_heat_load(U_value, area, delta_temp)

    # Latent heat load calculation (assumes a constant humidity difference for simplicity)
    latent_load = latent_heat_load(num_occupants, ventilation_rate, 10)

    # Total heat load
    total_heat_load = sensible_load + latent_load
    return sensible_load, latent_load, total_heat_load, outdoor_temp, outdoor_humidity


city = input("Enter City: ")
temperature, humidity = fetch_city_climate(city)

if temperature is None or humidity is None:
    print("Invalid city area terminated")

else:
    area = int(input("Enter area(sq m) = "))
    U_value = float(input("Enter U value = "))
    num_occupants = int(input("Enter occupants = "))
    ventilation_rate = int(input("Enter ventilation rate = "))
    indoor_temp = int(input("Enter Indoor Temp (C) = "))

    # Calculate heat load
    result = calculate_heat_load(city, area, U_value, num_occupants, ventilation_rate, indoor_temp)

    if result:
        sensible_load, latent_load, total_load, outdoor_temp, outdoor_humidity = result

        # Output Results
        print(f"\nCity: {city}")
        print(f"Temperature: {outdoor_temp} °C")
        print(f"Humidity: {outdoor_humidity}%")
        print(f"Sensible Heat Load: {sensible_load:.2f} W")
        print(f"Latent Heat Load: {latent_load:.2f} W")
        print(f"Total Heat Load: {total_load:.2f} W")
