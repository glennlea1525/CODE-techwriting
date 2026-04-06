import os
import requests
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("2b374d5ff6b493b86537d157a004d480")

# Base URL for the Current Weather endpoint
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Build the request — replace "Berlin" with any city you like
params = {
    "q": "Berlin",          # City name
    "appid": API_KEY,       # Your API key
    "units": "metric",      # Use "imperial" for Fahrenheit
    "lang": "en"            # Response language
}

response = requests.get(BASE_URL, params=params)
data = response.json()

print(data)