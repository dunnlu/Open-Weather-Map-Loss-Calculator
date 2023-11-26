"""

Authors: Jayden Fong, Marc Belinga
Last Modified: November 10, 2023
    By: Jayden Fong

Description:
    This script loads weather data from a CSV file, extracts specific features, and retrieves data for a given time
    period with a specified step size.

Dependencies:
    - NumPy

Note:
    If num_timesteps and step size exceed the bounds of the csv data, only the available data given the parameters 
    will be output. 

"""

import numpy as np

#################
# INPUT:
    # feature: The feature to be retrieved
    # river_name: name of river file to extract data from
    # start_dt: unix epoch start date: str
    # num_timesteps: number of desired timesteps
    # step_size: length between step sizes in days --> will be multiplied by 24 to get the first entry for each day
# OUTPUT:
    # Result: one-column NumPy array corresponding to the chosen feature
#################

def retrieve_data(feature: str, river_name: str, start_dt: str, num_timesteps: int, step_size: int):
    # Load data from csv
    try:
        data = load_data(river_name)
    except FileNotFoundError:
        print(f"Error: CSV file '{river_name}' not found.")
        return None

    # Get starting row index
    try:
        row_index = get_start_index(start_dt, data)
    except IndexError:
        print(f"Error: Start date '{start_dt}' not found in the CSV file.")
        return None

    # Extract feature column
    try:
        feature_column = data[feature]
    except ValueError:
        print(f"Error: Feature '{feature}' not found in the CSV file.")
        return None

    # Get step size (history bulk contains hourly entries. Multiply by 24 to retrieve the first data for each day)
    step_size *= 24

    # Splice data for timeframe and steps
    result = feature_column[row_index : row_index + (num_timesteps + 1) * step_size : step_size]

    # Return data
    return result

#################
# INPUT:
    # filename: name of file to be
# OUTPUT:
    # data: NumPy array of CSV data
#################

def load_data(filename):
    try:
        # Definition for Open Weather Map History Bulk csv
        dtype = [
            ('dt', int),
            ('dt_iso', 'U29'),
            ('timezone', int),
            ('city_name', 'U10'),
            ('lat', float),
            ('lon', float),
            ('temp', float),
            ('feels_like', float),
            ('temp_min', float),
            ('temp_max', float),
            ('pressure', int),
            ('sea_level', 'U3'),
            ('grnd_level', int),
            ('humidity', float),
            ('wind_speed', int),
            ('wind_deg', 'U3'),
            ('rain_1h', int),
            ('rain_3h', 'U3'),
            ('snow_1h', 'U3'),
            ('clouds_all', int),
            ('weather_id', int),
            ('weather_main', 'U10'),
            ('weather_description', 'U255'),
            ('weather_icon', 'U4'),
        ]

        # Get/return data from file using dtype    
        data = np.genfromtxt(filename, delimiter=',', dtype=dtype, skip_header=True)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file '{filename}' not found.")

#################
# INPUT:
# start_dt: starting date
# data: NumPy array with CSV data
# OUTPUT:
# index: row index of the start date from CSV
#################

def get_start_index(start_dt, data):
    # Extract the first column from the data array
    date_column = data["dt"]

    # Find the index of the first matching integer value
    index = np.where(date_column == start_dt)[0]

    # Check if the search_value was found
    if index.size > 0:
        return index[0]
    else:
        raise IndexError("Start date not found in CSV file.")

# EXAMPLE USAGE
def main():
    feature_to_retrieve = "temp"  # Replace with the desired feature
    river_name = "history_bulk_example_csv.csv"  # Replace with the actual filename or provide it as a command-line argument
    start_date = 1593561600  # Replace with the desired start date
    num_timesteps_to_retrieve = 2
    step_size_value = 1

    result_data = retrieve_data(feature_to_retrieve, river_name, start_date, num_timesteps_to_retrieve, step_size_value)
    print(result_data)

if __name__ == "__main__":
    main()
