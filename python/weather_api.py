import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd

# Setup the Open-Meteo API client with cache and retry (do this once)
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


def get_weather_for_hour(lat: float, lon: float, date_str: str, hour: int) -> dict:
    """
    Fetch weather for a specific date + hour at a location.
    Returns a dict with the weather variables (or None on error).
    """
    lat = round(float(lat), 2)
    lon = round(float(lon), 2)
    hour = int(hour) if pd.notna(hour) else 0
    if hour < 0 or hour > 23:
        hour = 0

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": str(date_str).strip(),
        "end_date": str(date_str).strip(),
        "hourly": [
            "temperature_2m",
            "dew_point_2m",
            "cloud_cover",
            "precipitation",
            "wind_speed_10m",
        ],
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
        "timezone": "auto",           # makes hour 0 = local midnight
    }

    try:
        responses = openmeteo.weather_api(
            url="https://archive-api.open-meteo.com/v1/archive",
            params=params
        )
        response = responses[0]
        hourly = response.Hourly()

        
        temp = hourly.Variables(0).ValuesAsNumpy()
        dew = hourly.Variables(1).ValuesAsNumpy()
        cloud = hourly.Variables(2).ValuesAsNumpy()
        precip = hourly.Variables(3).ValuesAsNumpy()
        wind = hourly.Variables(4).ValuesAsNumpy()

        return {
            "temperature_f": float(temp[hour]) if len(temp) > hour else None,
            "dew_point": float(dew[hour]) if len(dew) > hour else None,
            "cloud_cover": float(cloud[hour]) if len(cloud) > hour else None,
            "precip": float(precip[hour]) if len(precip) > hour else None,
            "wind_mph": float(wind[hour]) if len(wind) > hour else None,
        }

    except Exception as e:
        print(f"⚠️ Weather fetch failed for {lat}, {lon} on {date_str} hour {hour}: {e}")
        return {
            "temperature_f": None,
            "dew_point": None,
            "cloud_cover": None,
            "precip": None,
            "wind_mph": None,
        }
    