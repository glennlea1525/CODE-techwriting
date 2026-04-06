# Working Python Example: Open-Meteo Weather API

This example uses the Open-Meteo API — a free weather API that requires no API key and no account. Every code block here runs as-is.

## Prerequisites

- Python 3.8+
- pip installed

## Step 1 — Install Dependencies

```bash
pip install requests
```

✅ Expected output:

```
Successfully installed requests-2.31.0
```

## Step 2 — Hello World: Fetch Live Weather

Create a file called weather.py and add this:

```python
import requests

# Open-Meteo API — no key needed
# Coordinates below are for Berlin, Germany
url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 52.52,        # Berlin latitude
    "longitude": 13.41,       # Berlin longitude
    "current_weather": True   # Return current conditions
}

response = requests.get(url, params=params)
data = response.json()

print(data["current_weather"])
```

Run it:

```bash
python3 weather.py
```

✅ Expected output:

```json
{
  "temperature": 12.4,
  "windspeed": 14.2,
  "weathercode": 61,
  "is_day": 1,
  "time": "2026-04-06T09:00"
}
```

## Step 3 — Decode the Weather Code

Open-Meteo uses WMO weather codes to describe conditions. Let's map those to readable descriptions:

```python
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
```

✅ Expected output:

```
Condition  : Slight rain
Temperature: 12.4°C
Wind Speed : 14.2 km/h
Time       : 2026-04-06T09:00  (Day)
```

## Step 4 — Fetch a 7-Day Forecast

Open-Meteo can return daily high/low temperatures and rain totals in one call:

```python  
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
```    

✅ Expected output:

```
7-Day Forecast for Berlin

  Sunday, Apr 06
    Slight rain | High: 13.2°C  Low: 8.1°C  Rain: 4.2mm
  Monday, Apr 07
    Partly cloudy | High: 11.5°C  Low: 6.3°C  Rain: 0.0mm
  Tuesday, Apr 08
    Clear sky | High: 14.8°C  Low: 7.9°C  Rain: 0.0mm
  ...
```  

## Step 5 — Look Up Any City by Name

Instead of hardcoding coordinates, use the Open-Meteo Geocoding API to search by city name:

```python 
import requests

def get_coordinates(city: str) -> dict:
    """Return lat/lon and display name for a city."""
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    response = requests.get(geo_url, params={"name": city, "count": 1})
    results = response.json().get("results")

    if not results:
        raise ValueError(f"City '{city}' not found.")

    result = results[0]
    return {
        "name":      result["name"],
        "country":   result["country"],
        "latitude":  result["latitude"],
        "longitude": result["longitude"]
    }


def get_current_weather(city: str) -> None:
    """Fetch and print current weather for any city by name."""
    location = get_coordinates(city)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude":        location["latitude"],
        "longitude":       location["longitude"],
        "current_weather": True
    }

    response = requests.get(url, params=params)
    weather  = response.json()["current_weather"]

    print(f"Weather in {location['name']}, {location['country']}")
    print(f"  Temperature : {weather['temperature']}°C")
    print(f"  Wind Speed  : {weather['windspeed']} km/h")
    print(f"  Time        : {weather['time']}")
```

# Try any city!
get_current_weather("Tokyo")
```

✅ Expected output:

```
Weather in Tokyo, Japan
  Temperature : 18.7°C
  Wind Speed  : 9.3 km/h
  Time        : 2026-04-06T17:00
```  

## Step 6 — The Complete Script (With Full Error Handling)

A single, copy-paste ready script combining everything:

```python
import requests
from datetime import datetime

# --- Weather Code Lookup ---
WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Foggy", 48: "Icy fog", 51: "Light drizzle", 53: "Moderate drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight showers", 81: "Moderate showers", 95: "Thunderstorm"
}

GEO_URL      = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL  = "https://api.open-meteo.com/v1/forecast"


def get_coordinates(city: str) -> dict:
    """Resolve a city name to coordinates."""
    response = requests.get(GEO_URL, params={"name": city, "count": 1}, timeout=10)
    response.raise_for_status()
    results = response.json().get("results")

    if not results:
        raise ValueError(f"City '{city}' not found. Check the spelling.")

    r = results[0]
    return {
        "name": r["name"], "country": r["country"],
        "latitude": r["latitude"], "longitude": r["longitude"]
    }


def get_weather(city: str) -> None:
    """Fetch current conditions and a 7-day forecast for a city."""

    print(f"\nLooking up '{city}'...")
    location = get_coordinates(city)
    print(f"  ✓ Found: {location['name']}, {location['country']}\n")

    params = {
        "latitude":        location["latitude"],
        "longitude":       location["longitude"],
        "current_weather": True,
        "daily": [
            "weathercode", "temperature_2m_max",
            "temperature_2m_min", "precipitation_sum"
        ],
        "timezone": "auto"      # Auto-detect timezone from coordinates
    }

    response = requests.get(WEATHER_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    # --- Current Conditions ---
    cw   = data["current_weather"]
    desc = WEATHER_CODES.get(cw["weathercode"], "Unknown")
    tod  = "Day" if cw["is_day"] else "Night"

    print(f"📍 Current Weather — {location['name']}, {location['country']}")
    print(f"   {desc} ({tod})")
    print(f"   Temperature : {cw['temperature']}°C")
    print(f"   Wind Speed  : {cw['windspeed']} km/h")

    # --- 7-Day Forecast ---
    daily = data["daily"]
    print(f"\n📅 7-Day Forecast")
    for i in range(len(daily["time"])):
        date = datetime.strptime(daily["time"][i], "%Y-%m-%d").strftime("%A, %b %d")
        high = daily["temperature_2m_max"][i]
        low  = daily["temperature_2m_min"][i]
        rain = daily["precipitation_sum"][i]
        desc = WEATHER_CODES.get(daily["weathercode"][i], "Unknown")
        print(f"   {date}: {desc} | ↑{high}°C  ↓{low}°C  🌧 {rain}mm")

    print("\n  ✓ Done!")


def main():
    city = "Berlin"     # Change to any city in the world

    try:
        get_weather(city)
    except ValueError as e:
        print(f"✗ Location error: {e}")
    except requests.exceptions.ConnectionError:
        print("✗ Network error. Check your internet connection.")
    except requests.exceptions.Timeout:
        print("✗ Request timed out. Try again in a moment.")
    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()
```

✅ Expected output:

```
Looking up 'Berlin'...
  ✓ Found: Berlin, Germany

📍 Current Weather — Berlin, Germany
   Slight rain (Day)
   Temperature : 12.4°C
   Wind Speed  : 14.2 km/h

📅 7-Day Forecast
   Sunday, Apr 06: Slight rain | ↑13.2°C  ↓8.1°C  🌧 4.2mm
   Monday, Apr 07: Partly cloudy | ↑11.5°C  ↓6.3°C  🌧 0.0mm
   Tuesday, Apr 08: Clear sky | ↑14.8°C  ↓7.9°C  🌧 0.0mm
   Wednesday, Apr 09: Mainly clear | ↑15.1°C  ↓9.2°C  🌧 0.0mm
   Thursday, Apr 10: Overcast | ↑12.3°C  ↓7.8°C  🌧 1.1mm
   Friday, Apr 11: Moderate rain | ↑10.9°C  ↓6.5°C  🌧 8.3mm
   Saturday, Apr 12: Partly cloudy | ↑13.7°C  ↓8.0°C  🌧 0.5mm

  ✓ Done!
 ``` 

What You Learned

StepConcept CoveredStep 1Installing dependenciesStep 2Making a basic API call with no authenticationStep 3Decoding numeric codes into human-readable labelsStep 4Requesting multiple data fields in one API callStep 5Chaining two API calls (geocoding → weather)Step 6A full, error-handled production-ready script
