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
Location, start date, number of timesteps, time between timesteps, api key
### Output: 
Matrix with features corresponding to columns and timesteps corresponding to rows
  
## Historical Bulk Data Loader
### Input: 
Location, start date, number of timesteps, time between timesteps
### Output: 
Matrix with features corresponding to columns and timesteps corresponding to rows
  
## Loss Calculator
### Input: 
Feature, start date, number of timesteps, time between timesteps
### Output: 
Mean Absolute Error between the two APIs at all three locations

