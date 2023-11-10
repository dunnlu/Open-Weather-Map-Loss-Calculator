import pandas as pd
import logging
import requests

def call_onecall_timemachine(lat: str = '', lon: str = '', dt: str = '', units: str = '', appid: str = '', lang: str = '') -> pd.DataFrame:
    
    #make sure all required parameters are included
    if (lat == '' or lon == '' or dt == '' or appid == ''):
        print(f"Missing required parameters for call_onecall_timemachine() \n lat='{lat}', lon='{lon}', dt='{dt}', appid='{appid}'")
        
        #logging.log(logging.INFO, f"Missing required parameters for call_onecall_timemachine() \n lat='{lat}', lon='{lon}', dt='{dt}', appid='{appid}'")
        return None
    
    # API endpoint URL
    url = "https://api.openweathermap.org/data/3.0/onecall/timemachine?"

    #include all parameters that are provided in the URL
    url += f"&lat={lat}"
    url += f"&lon={lon}"
    url += f"&dt={dt}"
    if units != '':
        url += f"&units={units}"
    url += f"&appid={appid}"
    if lang != '':
        url += f"&lang={lang}"
   
    print(url)

    response = requests.get(url)

    # Check if the request was unsucessfu (status code != 200)
    if response.status_code != 200:
        print(f"API error! \n API parameters: lat='{lat}', lon='{lon}', dt='{dt}', appid='{appid}', units='{units}', lang='{lang}' \n API response: {response.status_code}, {response.text}")
        #logging.log(logging.INFO, f"API error! \n API parameters: lat='{lat}', lon='{lon}', dt='{dt}', appid='{appid}', units='{units}', lang='{lang}' \n API response: {response.status_code}, {response.text}")
        return None
    
    json_response = response.json()

    # Create a dictionary of all possible response fields
    # If the field is not present in the response, the value will be None (.get() returns None if the key is not present)
    data = {
    "lat": json_response.get("lat"),
    "lon": json_response.get("lon"),
    "timezone": json_response.get("timezone"),
    "timezone_offset": json_response.get("timezone_offset"),
    "dt": json_response["data"][0].get("dt"),
    "sunrise": json_response["data"][0].get("sunrise"),
    "sunset": json_response["data"][0].get("sunset"),
    "temp": json_response["data"][0].get("temp"),
    "feels_like": json_response["data"][0].get("feels_like"),
    "pressure": json_response["data"][0].get("pressure"),
    "humidity": json_response["data"][0].get("humidity"),
    "dew_point": json_response["data"][0].get("dew_point"),
    "uvi": json_response["data"][0].get("uvi"),
    "clouds": json_response["data"][0].get("clouds"),
    "visibility": json_response["data"][0].get("visibility"),
    "wind_speed": json_response["data"][0].get("wind_speed"),
    "wind_deg": json_response["data"][0].get("wind_deg"),
    "weather_id": json_response["data"][0]["weather"][0].get("id"),
    "weather_main": json_response["data"][0]["weather"][0].get("main"),
    "weather_description": json_response["data"][0]["weather"][0].get("description"),
    "weather_icon": json_response["data"][0]["weather"][0].get("icon")
    }
    # Create a DataFrame
    df = pd.DataFrame([data])
    return df


def make_list_of_unix_timestamps(unix_start: int, periods: int, freq: str = 'H', ) -> list:
    #create a list of timezone aware Datetime objects, with start time, number of periods, and frequency
    range = list(pd.date_range(start = str(pd.to_datetime(unix_start, unit='s', utc=True)), periods = periods, freq = 'H', tz='UTC'))
    
    #convert the list of Datetime objects to a list of unix timestamps
    unix_list_range = []
    for item in range:
        unix_list_range.append(int(item.timestamp()))
    return unix_list_range
