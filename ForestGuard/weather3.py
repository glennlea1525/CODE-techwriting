import requests
from datetime import datetime

WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Foggy", 51: "Light drizzle", 61: "Slight rain", 63: "Moderate rain",
    65: "Heavy rain", 71: "Slight snow", 80: "Slight showers",
    95: "Thunderstorm"
}

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "daily": [
        "weathercode",          # Dominant condition for the day
        "temperature_2m_max",   # Daily high
        "temperature_2m_min",   # Daily low
        "precipitation_sum"     # Total rainfall in mm
    ],
    "timezone": "Europe/Berlin"
}

response = requests.get(url, params=params)
data = response.json()
daily = data["daily"]

print("7-Day Forecast for Berlin\n")
for i in range(len(daily["time"])):
    date  = datetime.strptime(daily["time"][i], "%Y-%m-%d").strftime("%A, %b %d")
    high  = daily["temperature_2m_max"][i]
    low   = daily["temperature_2m_min"][i]
    rain  = daily["precipitation_sum"][i]
    code  = daily["weathercode"][i]
    desc  = WEATHER_CODES.get(code, "Unknown")

    print(f"  {date}")
    print(f"    {desc} | High: {high}°C  Low: {low}°C  Rain: {rain}mm")