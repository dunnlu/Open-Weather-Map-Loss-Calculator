import calculator_utils
import pandas as pd

#list where to accumulate individual (1 row) dataframes
df_list = []

#loop through timestamps generated by make_list_of_unix_timestamps
# this method gets a list of timezone aware Datetime objects
# and only then converts them to unix timestamps
# This should be more robust to anomalies like daylight savings time, leap years, etc.
# And overall lets pandas handle as much datetime manipulation as possible 
for timestamp in (calculator_utils.make_list_of_unix_timestamps(unix_start=1177632000, periods=100, freq='H')):
    #get a dataframe for each timestamp
    df = calculator_utils.call_onecall_timemachine(lat='47.4',
                                                     lon='-121.5',
                                                     dt=timestamp,
                                                     appid='')
    #append it to the list
    df_list.append(df)
#concatenate all the dataframes in the list into one big dataframe
big_df = pd.DataFrame()
big_df = pd.concat(df_list, ignore_index=True)
#save the big dataframe to a csv file
big_df.to_csv('big_df.csv')