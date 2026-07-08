# Anomolous Sightings Archive 🛸
 
This project explores a NUFORC ( National UFO Reporting Center ) Dataset previously found on Kaggle. The original CSV file can be found at data/uap_original_dataset.csv and contains almost 90K entries.  
 
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
- Original CSV File found at 'data/uap_original_dataset.csv'
- CSV file with additional columns for weather data from Weather API at 'data/sighting_with_weather_v2.csv'
- US population Data 'https://www.kaggle.com/datasets/rolfhendriks/us-population-by-state-comprehensive-data'

- Bigfoot Research Organization Database https://www.kaggle.com/datasets/thedevastator/unlocking-mysteries-of-bigfoot-through-sightings?select=bfro_reports.csv


## Workflow Overview  
**Anomalous Sightings Archive Project**

### Tools & Environment
- **Version Control**: GitHub
- **IDE**: VS Code
- **Primary Development**: Jupyter Notebooks (data wrangling, database creation, and visualizations)
- **Modular Python Scripts** (in `python/`):
    - Weather API integration
    - KP Index API fetching and CSV generation
    - Geohash generation from latitude/longitude
    - Proximity table computation and distance enrichment

### Project Workflow

1. **Data Ingestion**  
   Load original datasets into the `data/` directory:  
   - Bigfoot reports (2 BFRO datasets from Kaggle)  
   - UAP reports (NUFORC dataset from Kaggle)  
   - US Census 2010 state population data  
   - Generate `kp_index.csv` via dedicated API script

2. **Data Cleaning** (Pandas)  
   - Standard cleaning and normalization  
   - Merge the two Bigfoot datasets into `combined_bigfoot.csv`  
   - Save cleaned DataFrames as CSVs for backup and reproducibility

3. **Data Enrichment** (Pandas)  
   - Add solar KP Index and AP Index to relevant DataFrames  
   - Apply historical weather data (2010–2014 UAP reports) using `weather_api.py`  
     *(Full UAP dataset spans 1940–2014; Bigfoot data already contains weather)*  
   - Create proximity table by merging UAP and Bigfoot records on `geohash_7`  
   - Reorder columns to align with the Entity Relationship Diagram (ERD)

4. **Relational Database Creation** (SQLite)  
   Build the database with the following tables:  
   - `bigfoot_reports` (PK: `bf_id`)  
   - `uap_reports` (PK: `uap_id`)  
   - `states` (PK: `state_code`)  
   - `proximity` (composite PK: `bf_id` + `uap_id`)  
   - `kp_index` (PK: `datetime`)

5. **Analysis**  
   Execute SQL queries against the SQLite database to generate insights for visualization.

6. **Visualizations**  
   - Charts: Matplotlib + Seaborn  
   - Maps: GeoPandas + Folium

7. **Front-End & Stretch Goals**  
   - Interactive dashboard using **Streamlit** (primary option) or a static site  
   - User experience submission form (Python script / Streamlit page)


## API Use
- Weather API: Visit "https://www.weatherapi.com/" to obtain a free key. Store your key in a .env file with the variable "WX_API_KEY". 

## AI Use 
 
## Author
William Slider – Data Analyst
 
## License
MIT License
