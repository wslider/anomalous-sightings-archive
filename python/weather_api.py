import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd
from datetime import datetime

# Setup client 
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


def get_weather(lat, lon, date_str, hour=0, return_full_df=False):
    
    lat = round(float(lat), 2)
    lon = round(float(lon), 2)
    hour = int(hour) if pd.notna(hour) else 0
    if not (0 <= hour <= 23):
        hour = 0

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": str(date_str)[:10],
        "end_date": str(date_str)[:10],
        "hourly": ["temperature_2m", "dew_point_2m", "cloud_cover",
                   "precipitation", "wind_speed_10m"],
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
        "timezone": "auto",
    }

    try:
        responses = openmeteo.weather_api(
            "https://archive-api.open-meteo.com/v1/archive", params=params
        )
        response = responses[0]
        hourly = response.Hourly()

        temp = hourly.Variables(0).ValuesAsNumpy()
        dew = hourly.Variables(1).ValuesAsNumpy()
        cloud = hourly.Variables(2).ValuesAsNumpy()
        precip = hourly.Variables(3).ValuesAsNumpy()
        wind = hourly.Variables(4).ValuesAsNumpy()

        weather = {
            "temperature_f": round(float(temp[hour]), 1) if len(temp) > hour else None,
            "dew_point": round(float(dew[hour]), 1) if len(dew) > hour else None,
            "cloud_cover": round(float(cloud[hour]), 1) if len(cloud) > hour else None,
            "precip_in": round(float(precip[hour]), 2) if len(precip) > hour else None,
            "wind_mph": round(float(wind[hour]), 1) if len(wind) > hour else None,
        }

        if return_full_df:
            hourly_df = pd.DataFrame({
                "datetime": pd.date_range(
                    start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                    end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                    freq=pd.Timedelta(seconds=hourly.Interval()),
                    inclusive="left"
                ),
                "temperature_f": temp,
                "dew_point": dew,
                "cloud_cover": cloud,
                "precip_in": precip,
                "wind_mph": wind,
            })
            return weather, hourly_df

        return weather

    except Exception as e:
        print(f"Weather API error ({lat}, {lon}, {date_str} h{hour}): {e}")
        default = {k: None for k in ["temperature_f", "dew_point", "cloud_cover", "precip_in", "wind_mph"]}
        if return_full_df:
            return default, pd.DataFrame()
        return default

# vectorized weather condition classification

def classify_weather(df):
    
    df = df.copy()
    df['weather_conditions'] = 'unknown'

    precip = df['precip_in'] > 0.0
    cold = df['temperature_f'] <= 32

    df.loc[precip & cold, 'weather_conditions'] = 'snow'
    df.loc[precip & ~cold, 'weather_conditions'] = 'rain'

    no_precip = ~precip
    df.loc[no_precip & (df['cloud_cover'] < 25), 'weather_conditions'] = 'clear'
    df.loc[no_precip & (df['cloud_cover'] >= 25) & (df['cloud_cover'] < 75), 'weather_conditions'] = 'partly_cloudy'
    df.loc[no_precip & (df['cloud_cover'] >= 75), 'weather_conditions'] = 'cloudy'

    return df

if __name__ == "__main__":
    get_weather()

if __name__ == "__main__":
    classify_weather()

