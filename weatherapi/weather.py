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