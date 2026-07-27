# 🛸 Anomalous Sightings Archive 🗺️

This project investigates potential correlations between Bigfoot and UFO (UAP) sightings across the United States from 1950 to 2014.  
The primary goal is to determine whether there is a meaningful relationship in the **time** and/or **location** of these anomalous phenomena, or if any clusters exist.  
Secondary goals include identifying shared environmental conditions (season, weather, KP index, etc.) and providing practical insights for independent investigators.

---

## How to Use

1. Clone this repository  
2. Create and activate a virtual environment:

   **macOS / Linux**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   **Windows (PowerShell)**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Open `notebooks/anomalous_sightings_analysis.ipynb` in Jupyter Notebook or JupyterLab and run the cells.

> All key charts and maps are saved in the `plots/` directory (see below).

---

## Example Output

Key visualizations from the current analysis:

| Visualization | File |
|---------------|------|
| Histogram of temperatures at UAP & Bigfoot sightings | [`plots/bigfoot_uap_temperatures_histogram.png`](plots/bigfoot_uap_temperatures_histogram.png) |
| Cloud cover distribution across all reports | [`plots/cloud_cover_distribution_all_reports_bar.png`](plots/cloud_cover_distribution_all_reports_bar.png) |
| KP Index distribution (Historical vs Bigfoot vs UAP) | [`plots/kp_index_distribution_all_reports_bar_v2.png`](plots/kp_index_distribution_all_reports_bar_v2.png) |
| Choropleth maps (sightings & proximity per million population) | `plots/` |
| Cluster / density / proximity maps | `plots/` |

Archived plots from earlier versions (2010–2014 UAP subset) are available in `plots/archive/`.

---

## Data Sources

- **UAP / UFO reports**: `data/raw/uap_original_dataset.csv` (NUFORC, originally from Kaggle – currently unavailable)
- **UAP + weather (2010–2014)**: `data/processed/sighting_with_weather_v2.csv`
- **US population by state**: [Kaggle – US Population by State](https://www.kaggle.com/datasets/rolfhendriks/us-population-by-state-comprehensive-data)
- **Bigfoot reports**: [BFRO Database on Kaggle](https://www.kaggle.com/datasets/thedevastator/unlocking-mysteries-of-bigfoot-through-sightings?select=bfro_reports.csv)

---

## Project Workflow

### Tools & Environment
- **Version Control**: GitHub  
- **IDE**: VS Code  
- **Primary Development**: Jupyter Notebooks  
- **Main Notebook**: `notebooks/anomalous_sightings_analysis.ipynb`  
- **Modular Python scripts** (`python/`):
  - Weather API integration (Open-Meteo)
  - KP Index fetching & CSV generation
  - Geohash generation + haversine distance
  - Proximity table computation

### Step-by-step Process

1. **Data Ingestion**  
   Load Bigfoot (BFRO), UAP (NUFORC), US Census population data, and generate `kp_index.csv`.

2. **Data Cleaning** (Pandas)  
   Standard cleaning, normalization, and merging of the two Bigfoot datasets into `combined_bigfoot.csv`.

3. **Data Enrichment** (Pandas)  
   - Add solar KP / AP Index  
   - Historical weather (2010–2014 UAP) via `weather_api.py` (Open-Meteo)  
   - Create proximity table by merging on `geohash_7`  
   - Reorder columns to match the ERD

4. **Relational Database** (SQLite)  
   Tables:
   - `bigfoot_reports` (PK: `bf_id`)
   - `bigfoot_weather`
   - `uap_reports` (PK: `uap_id`)
   - `us_uap_2011_weather`
   - `states` (PK: `state_code`)
   - `proximity` (composite PK: `bf_id` + `uap_id`)
   - `kp_index` (PK: `datetime`)

   ![Entity Relationship Diagram](images/anomalous_sightings_archive_erd_d7.png) 

5. **Analysis**  
   SQL queries against the SQLite database to generate insights.

6. **Visualizations**  
   - Charts: Matplotlib + Seaborn  
   - Maps: GeoPandas + Folium  

7. **Front-End & Stretch Goals**  
   - Interactive Streamlit dashboard  
   - User sighting submission form

---

## API Use

**Current – Open-Meteo**  
This project uses the free [Open-Meteo](https://open-meteo.com/) Historical Weather API.  
No API key is required.

The weather enrichment logic lives in `python/weather_api.py`.

**Legacy (Previous Version – Not Required)**  
Older notebooks used WeatherAPI.com.  
If you want to re-run those archived notebooks:
1. Get a free key at [https://www.weatherapi.com/](https://www.weatherapi.com/)
2. Store it in a `.env` file:
   ```
   WX_API_KEY=your_key_here
   ```

---

## AI Assistance

### Archived Notebooks (`notebooks/archive/`)
- Weather API request parsing for 2010–2014 UAP data (Grok 4)
- UAP state choropleth map creation (Grok 4)

### Main Notebook (`notebooks/anomalous_sightings_analysis.ipynb`)
- `state_to_code` dictionary generation (Grok 4)
- Handling of `24:00` datetime edge cases (Grok 4)
- Primary key setup in SQLite (Grok 4)
- Weather API loop + checkpoints (Open-Meteo) (Grok 4)
- Cloud cover CTE (`CASE` statement) (Grok 4)
- Grouped bar chart of cloud cover distribution (Grok 4)

### Python Modules (`python/`)
- `kp_index.py` – datetime parsing (Grok 4)
- `geo_location.py` – `create_geohashes` + `haversine_distance` (Grok 4)
- `weather_api.py` – error handling + vectorized weather condition classification (Grok 4)

### README.md
- Example Output Section with Links to Plots (Grok 4)
- Typo and Spellchecking (Grok 4)

---

## Author

**William Slider** – Data Analyst

---

## License

MIT License