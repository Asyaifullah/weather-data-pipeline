import os
import requests
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

URL = "https://api.open-meteo.com/v1/forecast"
CITIES = {
    "Jakarta": (-6.20, 106.85),
    "Surabaya": (-7.25, 112.75),
    "Bandung": (-6.92, 107.61),
    "Medan": (3.59, 98.67),
    "Makassar": (-5.15, 119.43),
}


def fetch_city(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation",
        "timezone": "Asia/Jakarta",
        "forecast_days": 1,
    }
    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()["hourly"]


def main():
    rows = []
    for city, (lat, lon) in CITIES.items():
        h = fetch_city(lat, lon)
        for t, temp, hum, pre in zip(
            h["time"], h["temperature_2m"], h["relative_humidity_2m"], h["precipitation"]
        ):
            rows.append((city, t, temp, hum, pre))

    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )
    with conn, conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO raw_weather
                (city, observed_at, temperature_2m, relative_humidity_2m, precipitation)
            VALUES %s
            ON CONFLICT (city, observed_at) DO NOTHING
            """,
            rows,
        )
        cur.execute("SELECT COUNT(*) FROM raw_weather;")
        total = cur.fetchone()[0]
    conn.close()
    print(f"Fetched {len(rows)} rows, table now has {total} rows")


if __name__ == "__main__":
    main()