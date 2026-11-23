select
    city,
    cast(observed_at as date) as observation_date,
    round(avg(temperature_c), 1) as avg_temperature_c,
    max(temperature_c) as max_temperature_c,
    min(temperature_c) as min_temperature_c,
    round(avg(humidity_pct), 0) as avg_humidity_pct,
    sum(precipitation_mm) as total_precipitation_mm,
    count(*) as hours_recorded
from {{ ref('stg_weather') }}
group by city, cast(observed_at as date)