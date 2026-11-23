import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
)

with conn, conn.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw_weather (
            city VARCHAR(50) NOT NULL,
            observed_at TIMESTAMP NOT NULL,
            temperature_2m NUMERIC(5,2),
            relative_humidity_2m INTEGER,
            precipitation NUMERIC(6,2),
            ingested_at TIMESTAMP DEFAULT NOW(),
            PRIMARY KEY (city, observed_at)
        );
    """)
    cur.execute("SELECT COUNT(*) FROM raw_weather;")
    print("Rows:", cur.fetchone()[0])

conn.close()