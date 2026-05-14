# Anomolous Sightings Archive 🛸
 
This project explores a NUFORC ( National UFO Reporting Center ) Dataset previously found on Kaggle. The original CSV file can be found at data/complete.csv and contains almost 90K entries.  
 
## How to Use
1. Clone this repository.
2. Install the required Python packages:  
   pip install -r requirements.txt
3. Open `complete_analysis.ipynb` in Jupyter Notebook or JupyterLab.
 
## Example Output
The analysis focuses mainly on US sightings / reports and shows the following through charts found in 'plots/': 
- UFO sighting frequency peaks between 9:00 PM - 10:00 PM
- UFO sighting frequency peaks in the Summer and Early Fall Months
- Majority of sightings occur with Clear Skies
- Average Temperature at the Time of Sightings is ~ 57 F 
 
## Data Sources
- Original CSV File found at 'data/complete.csv'
- CSV file with additional columns for weather data from Weather API at 'data/sighting_with_weather_v2.csv'

## API Use
- Weather API: Visit "https://www.weatherapi.com/" to obtain a free key. Store your key in a .env file with the variable "WX_API_KEY". 
 
## Author
William Slider – Data Analyst
 
## License
MIT License
