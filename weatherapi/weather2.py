import requests

# WMO Weather Interpretation Codes (subset)
WEATHER_CODES = {
    0:  "Clear sky",
    1:  "Mainly clear",
    2:  "Partly cloudy",
    3:  "Overcast",
    45: "Foggy",
    48: "Icy fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight showers",
    81: "Moderate showers",
    82: "Violent showers",
    95: "Thunderstorm",
    99: "Thunderstorm with hail"
}

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "current_weather": True
}

response = requests.get(url, params=params)
data = response.json()
weather = data["current_weather"]

code        = weather["weathercode"]
description = WEATHER_CODES.get(code, "Unknown condition")
day_or_night = "Day" if weather["is_day"] else "Night"

print(f"Condition  : {description}")
print(f"Temperature: {weather['temperature']}°C")
print(f"Wind Speed : {weather['windspeed']} km/h")
print(f"Time       : {weather['time']}  ({day_or_night})")