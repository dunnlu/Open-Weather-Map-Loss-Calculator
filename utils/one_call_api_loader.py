import requests
import numpy as np
import pandas as pd

#################
# INPUT:
    # feature: The feature to be retrieved
    # lat: latitude of location
    # lon: longitude of location
    # dt: unix epoch timestep
    # api_key: OpenWeatherMap api_key --> must be subscribed to One Call API
# OUTPUT:
    # Feature's value at location and timestamp 
#################

def retrieve_data_from_timestep(feature: str, lat: str, lon: str, dt: str, api_key: str):
    # API endpoint URL
    url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={dt}&appid={api_key}"

    # Make the API request
    response = requests.get(url)


    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        assert(data['data'][0][feature])

        #Return data from the feature
        return data['data'][0][feature]
       

    else:
        # Print the error message if the request was not successful
        raise Exception(f"Error: {response.status_code}, {response.text}")


#################
# INPUT:
    # time: start date in unix epoch
    # num_timesteps: number of timesteps
    # step_size: step size in days
# OUTPUT:
    # Python array of dates in unix epoch --> daylight savings account for, leap years accounted for
#################

def date_range(time: int, num_timesteps: int, step_size: int):
    
    #Generate Pandas DateTimeIndex of Intended Range
    dates = pd.date_range(start=pd.to_datetime(time,unit='s'),periods=num_timesteps, freq=(str(step_size)+'D'))

    #Convert array of dates to int and remove nano seconds --> //10**9
    dates = dates.astype(np.int64)//10**9

    #Remove loss found by pandas.date_range() and convert to list of unix epoch times as ints
    actual_dates = []
    for i in dates:
        actual_dates.append(time + i - dates[0])

    return actual_dates

#################
# INPUT:
    # feature: The feature to be retrieved
    # lat: latitude of location
    # lon: longitude of location
    # start_dt: unix epoch start date: str
    # num_timesteps: number of desired timesteps
    # step_size: length between step sizes in days --> will be converted to seconds in the loader
    # api_key: OpenWeatherMap api_key --> must be subscribed to One Call API
# OUTPUT:
    # One-Column NumPy array corresponding to chosen feature
#################


def load_data(feature: str, lat: str, lon: str, start_dt: str, num_timesteps: int, step_size: int, api_key: str):

    #Temporary --> Prevent Accidentally Too much data to start having to pay for it
    assert(num_timesteps < 100)

    # Initialize Numpy array
        #Initial start point +1 for every timestep
    data = np.empty(num_timesteps)

    #Time int
    time = int(start_dt)

    dates  = date_range(time,num_timesteps,step_size)

    #Get all data
    for i in range(num_timesteps):
        data[i] = retrieve_data_from_timestep(feature, lat, lon, str(dates[i]), api_key)

    return data