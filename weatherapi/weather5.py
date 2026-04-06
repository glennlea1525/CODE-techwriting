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