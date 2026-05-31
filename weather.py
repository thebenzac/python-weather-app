import requests
import json
import sys

# Get city name from command line arguments
if len(sys.argv) < 2:
    print("Usage: python weather.py <city_name> [--days N] [--units metric/imperial]")
    sys.exit(1)

city = sys.argv[1]
units = "metric"  # default unit
days = 0  # 0 means just current weather, no forecast

# Parse optional arguments
for i in range(2, len(sys.argv)):
    if sys.argv[i] == "--days" and i + 1 < len(sys.argv):
        days = int(sys.argv[i + 1])
    if sys.argv[i] == "--units" and i + 1 < len(sys.argv):
        units = sys.argv[i + 1]

# Step 1: Get coordinates of the city using Open-Meteo geocoding
print("Looking up city...")

geo_url = "https://geocoding-api.open-meteo.com/v1/search"
geo_params = {
    "name": city,
    "count": 1,
    "language": "en",
    "format": "json"
}

geo_response = requests.get(geo_url, params=geo_params)
geo_data = geo_response.json()

if "results" not in geo_data or len(geo_data["results"]) == 0:
    print("City not found. Check the spelling and try again.")
    sys.exit(1)

result = geo_data["results"][0]
lat = result["latitude"]
lon = result["longitude"]
city_name = result["name"] + ", " + result.get("country_code", "")

print(f"Found: {city_name}")
print()

# Step 2: Get current weather from Open-Meteo API
weather_url = "https://api.open-meteo.com/v1/forecast"
weather_params = {
    "latitude": lat,
    "longitude": lon,
    "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m,pressure_msl,cloud_cover",
    "daily": "sunrise,sunset",
    "timezone": "auto"
}

weather_response = requests.get(weather_url, params=weather_params)
weather_data = weather_response.json()
current = weather_data["current"]

# Weather code mapping (WMO codes)
weather_codes = {
    0: ("Clear", "\u2600"),
    1: ("Mostly Clear", "\u26c5"),
    2: ("Partly Cloudy", "\u26c5"),
    3: ("Overcast", "\u2601"),
    45: ("Foggy", "\uf32b"),
    48: ("Depositing Rime Fog", "\uf32b"),
    51: ("Light Drizzle", "\uf327"),
    53: ("Moderate Drizzle", "\uf327"),
    55: ("Dense Drizzle", "\uf327"),
    56: ("Light Freezing Drizzle", "\uf327"),
    57: ("Dense Freezing Drizzle", "\uf327"),
    61: ("Slight Rain", "\uf327"),
    63: ("Moderate Rain", "\uf327"),
    65: ("Heavy Rain", "\uf327"),
    66: ("Light Freezing Rain", "\uf327"),
    67: ("Heavy Freezing Rain", "\uf327"),
    71: ("Slight Snow", "\uf328"),
    73: ("Moderate Snow", "\uf328"),
    75: ("Heavy Snow", "\uf328"),
    77: ("Snow Grains", "\uf328"),
    80: ("Slight Rain Showers", "\uf327"),
    81: ("Moderate Rain Showers", "\uf327"),
    82: ("Violent Rain Showers", "\uf327"),
    85: ("Slight Snow Showers", "\uf328"),
    86: ("Heavy Snow Showers", "\uf328"),
    95: ("Thunderstorm", "\u26c8"),
    96: ("Thunderstorm with Slight Hail", "\u26c8"),
    99: ("Thunderstorm with Heavy Hail", "\u26c8"),
}

# Get weather description and icon
code = current["weather_code"]
if code in weather_codes:
    weather_text = weather_codes[code][0]
    weather_icon = weather_codes[code][1]
else:
    weather_text = "Unknown"
    weather_icon = "?"

# Format temperature
if units == "imperial":
    temp = current["temperature_2m"] * 9 / 5 + 32
    feels = current["apparent_temperature"] * 9 / 5 + 32
    temp_str = f"{temp:.1f}F"
    feels_str = f"{feels:.1f}F"
else:
    temp_str = f"{current['temperature_2m']:.1f}C"
    feels_str = f"{current['apparent_temperature']:.1f}C"

# Format wind speed
if units == "imperial":
    wind_speed = current["wind_speed_10m"] * 0.6214
    wind_unit = "mph"
else:
    wind_speed = current["wind_speed_10m"]
    wind_unit = "km/h"

# Wind direction
wind_directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                   "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
wind_dir_idx = round(current["wind_direction_10m"] / 22.5) % 16
wind_dir = wind_directions[wind_dir_idx]

humidity = current["relative_humidity_2m"]
pressure = current["pressure_msl"]
clouds = current["cloud_cover"]

# Get sunrise/sunset from daily data
if "daily" in weather_data:
    sunrise = weather_data["daily"]["sunrise"][0][11:16]
    sunset = weather_data["daily"]["sunset"][0][11:16]
else:
    sunrise = "N/A"
    sunset = "N/A"

# Print current weather
print(weather_icon + "  " + city_name)
print("=" * (len(city_name) + 4))
print(weather_text)
print("Temp:     " + temp_str + "  (feels " + feels_str + ")")
print("Humidity: " + str(humidity) + "%")
print("Pressure: " + str(round(pressure)) + " hPa")
print("Wind:     " + f"{wind_speed:.1f}" + " " + wind_unit + " " + wind_dir)
print("Clouds:   " + str(clouds) + "%")
print("Sunrise:  " + sunrise)
print("Sunset:   " + sunset)
print()

# Step 3: Show forecast if user requested it
if days > 0:
    print(city_name + " - " + str(days) + "-Day Forecast")
    print()
    
    forecast_params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "weather_code,temperature_2m_max,temperature_2m_min",
        "timezone": "auto",
        "forecast_days": min(days, 7)
    }
    
    forecast_response = requests.get(weather_url, params=forecast_params)
    forecast_data = forecast_response.json()
    daily = forecast_data["daily"]
    
    for i in range(len(daily["time"])):
        day_code = daily["weather_code"][i]
        if day_code in weather_codes:
            day_icon = weather_codes[day_code][0]
            day_emoji = weather_codes[day_code][1]
        else:
            day_icon = "Unknown"
            day_emoji = "?"
        
        date = daily["time"][i]
        
        if units == "imperial":
            hi = daily["temperature_2m_max"][i] * 9 / 5 + 32
            lo = daily["temperature_2m_min"][i] * 9 / 5 + 32
            hi_str = f"{hi:.1f}F"
            lo_str = f"{lo:.1f}F"
        else:
            hi_str = f"{daily['temperature_2m_max'][i]:.1f}C"
            lo_str = f"{daily['temperature_2m_min'][i]:.1f}C"
        
        print(day_emoji + "  " + date)
        print("     " + day_icon)
        print("     " + lo_str + " / " + hi_str)
        print()
