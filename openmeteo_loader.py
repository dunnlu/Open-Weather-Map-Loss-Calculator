import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

######################
# Latitude --> A string, the number
# Longitude --> A string, a string, the number
# Start_date --> A string, in ISO 8601 form, example: 2023-11-10
# End_date --> A string, in ISO 8601 form, example: 2023-11-24
# Timezone --> A string, the timezone --> see https://open-meteo.com/en/docs/historical-weather-api#hourly=&timezone=GMT to see a list of available timezones
    #                                           Just look at the list, and see how it is written. For example "America/Los_Angeles"
######################



def call_openmeteo_archive(lat: str = '', lon: str = '', start_dt: str = '',  end_dt: str = '',tz: str = 'GMT') -> pd.DataFrame:

    #make sure all required parameters are included
    if (lat == '' or lon == '' or start_dt == '' or end_dt == ''):
        print(f"Missing required parameters for call_openmeteo_archive() \n lat='{lat}', lon='{lon}', start_dt='{start_dt}', end_dt='{end_dt}'")
        
        #logging.log(logging.INFO, f"Missing required parameters for call_openmeteo_archive() \n lat='{lat}', lon='{lon}', dt='{dt}', appid='{appid}'")
        return None


    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)


    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": float(lat),
        "longitude": float(lon),
        "start_date": start_dt,
        "end_date": end_dt,
        "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", "precipitation", "rain", "snowfall", "snow_depth", "weather_code", "pressure_msl", "surface_pressure", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "et0_fao_evapotranspiration", "vapour_pressure_deficit", "wind_speed_10m", "wind_speed_100m", "wind_direction_10m", "wind_direction_100m", "wind_gusts_10m", "soil_temperature_0_to_7cm", "soil_temperature_7_to_28cm", "soil_temperature_28_to_100cm", "soil_temperature_100_to_255cm", "soil_moisture_0_to_7cm", "soil_moisture_7_to_28cm", "soil_moisture_28_to_100cm", "soil_moisture_100_to_255cm"],
        "timezone": tz
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(4).ValuesAsNumpy()
    hourly_rain = hourly.Variables(5).ValuesAsNumpy()
    hourly_snowfall = hourly.Variables(6).ValuesAsNumpy()
    hourly_snow_depth = hourly.Variables(7).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(8).ValuesAsNumpy()
    hourly_pressure_msl = hourly.Variables(9).ValuesAsNumpy()
    hourly_surface_pressure = hourly.Variables(10).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(11).ValuesAsNumpy()
    hourly_cloud_cover_low = hourly.Variables(12).ValuesAsNumpy()
    hourly_cloud_cover_mid = hourly.Variables(13).ValuesAsNumpy()
    hourly_cloud_cover_high = hourly.Variables(14).ValuesAsNumpy()
    hourly_et0_fao_evapotranspiration = hourly.Variables(15).ValuesAsNumpy()
    hourly_vapour_pressure_deficit = hourly.Variables(16).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(17).ValuesAsNumpy()
    hourly_wind_speed_100m = hourly.Variables(18).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(19).ValuesAsNumpy()
    hourly_wind_direction_100m = hourly.Variables(20).ValuesAsNumpy()
    hourly_wind_gusts_10m = hourly.Variables(21).ValuesAsNumpy()
    hourly_soil_temperature_0_to_7cm = hourly.Variables(22).ValuesAsNumpy()
    hourly_soil_temperature_7_to_28cm = hourly.Variables(23).ValuesAsNumpy()
    hourly_soil_temperature_28_to_100cm = hourly.Variables(24).ValuesAsNumpy()
    hourly_soil_temperature_100_to_255cm = hourly.Variables(25).ValuesAsNumpy()
    hourly_soil_moisture_0_to_7cm = hourly.Variables(26).ValuesAsNumpy()
    hourly_soil_moisture_7_to_28cm = hourly.Variables(27).ValuesAsNumpy()
    hourly_soil_moisture_28_to_100cm = hourly.Variables(28).ValuesAsNumpy()
    hourly_soil_moisture_100_to_255cm = hourly.Variables(29).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s"),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["dew_point_2m"] = hourly_dew_point_2m
    hourly_data["apparent_temperature"] = hourly_apparent_temperature
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["rain"] = hourly_rain
    hourly_data["snowfall"] = hourly_snowfall
    hourly_data["snow_depth"] = hourly_snow_depth
    hourly_data["weather_code"] = hourly_weather_code
    hourly_data["pressure_msl"] = hourly_pressure_msl
    hourly_data["surface_pressure"] = hourly_surface_pressure
    hourly_data["cloud_cover"] = hourly_cloud_cover
    hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
    hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
    hourly_data["cloud_cover_high"] = hourly_cloud_cover_high
    hourly_data["et0_fao_evapotranspiration"] = hourly_et0_fao_evapotranspiration
    hourly_data["vapour_pressure_deficit"] = hourly_vapour_pressure_deficit
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_speed_100m"] = hourly_wind_speed_100m
    hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
    hourly_data["wind_direction_100m"] = hourly_wind_direction_100m
    hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
    hourly_data["soil_temperature_0_to_7cm"] = hourly_soil_temperature_0_to_7cm
    hourly_data["soil_temperature_7_to_28cm"] = hourly_soil_temperature_7_to_28cm
    hourly_data["soil_temperature_28_to_100cm"] = hourly_soil_temperature_28_to_100cm
    hourly_data["soil_temperature_100_to_255cm"] = hourly_soil_temperature_100_to_255cm
    hourly_data["soil_moisture_0_to_7cm"] = hourly_soil_moisture_0_to_7cm
    hourly_data["soil_moisture_7_to_28cm"] = hourly_soil_moisture_7_to_28cm
    hourly_data["soil_moisture_28_to_100cm"] = hourly_soil_moisture_28_to_100cm
    hourly_data["soil_moisture_100_to_255cm"] = hourly_soil_moisture_100_to_255cm

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    return hourly_dataframe