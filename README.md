# Open-Weather-Map-Loss-Calculator
Calculator to show the loss between OpenWeatherMap's One Call API and Historical Bulk Data
  
## Three Locations Selected:
### 1:  
Historical Data Purchased By:   
Lat:  
Long:  
  
### 2:
Historical Data Purchased By:  
Lat:  
Long:  
  
### 3: 
Historical Data Purchased By:  
Lat:  
Long:  
  
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

