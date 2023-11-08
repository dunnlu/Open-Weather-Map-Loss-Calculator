# Open-Weather-Map-Loss-Calculator
Calculator to show the loss between OpenWeatherMap's One Call API and Historical Bulk Data
  
## Three Locations Selected:
### 1:  SF SNOQUALMIE RIVER AB ALICE CREEK NEAR GARCIA, WA
Historical Data Purchased By:   Jayden  
Lat:  47.4  
Long:  -121.5  
  
### 2: JOHN DAY RIVER AT SERVICE CREEK, OR
Historical Data Purchased By:  Jayden  
Lat:  44.2  
Long: -119.6  
  
### 3: ROGUE RIVER AT DODGE BRIDGE, NEAR EAGLE POINT, OR
Historical Data Purchased By:  Jayden  
Lat:  42.7  
Long:  -122.6  
  
## One Call API Loader
### Input: 
Feature: str, lat: str, lon: str, start date: unix epoch: str, number of timesteps: int, time between timesteps: in days: int, api key: str
### Output: 
Numpy Array correlating with the feature
### Tutorial:
To use the loader include the following:
```bash
#Import loader
import one_call_api_loader.py as ocal

#Example Call
data = ocal.load_data('temp','47.4','-121.4','1643803200',10,1,{api_key})
```


  
## Historical Bulk Data Loader
### Input: 
Feature: str, lat: str, lon: str, start date: unix epoch: str, number of timesteps: int, time between timesteps: in days: int
### Output: 
Numpy Array correlating with the feature
  
## Loss Calculator
### Input: 
Feature, start date, number of timesteps, time between timesteps
### Output: 
Mean Absolute Error between the two APIs at all three locations

