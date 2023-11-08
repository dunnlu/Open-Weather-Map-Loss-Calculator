import requests
import numpy as np


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

        #Return data from the feature
        return data['data'][0][feature]
       

    else:
        # Print the error message if the request was not successful
        raise Exception(f"Error: {response.status_code}, {response.text}")



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
    # Initialize Numpy array
        #Initial start point +1 for every timestep
    data = np.empty(num_timesteps)

    #Time int
    time = int(start_dt)

    #Get all data
    for i in range(0,num_timesteps):
        data[i] = retrieve_data_from_timestep(feature, lat, lon, str(time), api_key)
        time += step_size * 86400


    return data
