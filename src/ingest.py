import requests

URL = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": -6.2,
    "longitude": 106.85,
    "hourly": "temperature_2m,relative_humidity_2m,precipitation",
    "timezone": "Asia/Jakarta",
    "forecast_days": 1,
}

response = requests.get(URL, params=params, timeout=30)
response.raise_for_status()
data = response.json()

print(list(data.keys()))
print(data["hourly"]["time"][:3])
print(data["hourly"]["temperature_2m"][:3])