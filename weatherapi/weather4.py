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


# Try any city!
get_current_weather("London")