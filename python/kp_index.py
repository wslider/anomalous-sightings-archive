import requests
import pandas as pd
from io import StringIO
from datetime import datetime
from pathlib import Path

def update_kp_data():
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    url = f"https://kp.gfz.de/kpdata?startdate=1932-01-01&enddate={today}&format=kp2"
    
    print(f"Downloading Kp data up to {today}...")

    response = requests.get(url)
    response.raise_for_status()

    df = pd.read_csv(
        StringIO(response.text),
        sep=r'\s+',
        header=None,
        names=[
            'year', 'month', 'day', 
            'hour_start', 'hour_end',
            'decimal_day_start', 'decimal_day_end',
            'kp', 'ap', 'flag'
        ]
    )

    df['datetime'] = pd.to_datetime(
        df[['year', 'month', 'day']].astype(str).agg('-'.join, axis=1) + ' ' +
        df['hour_start'].astype(str).str.replace('.0', ':00', regex=False)
    )

    output_path = Path("../data/processed/kp_index.csv")
    df.to_csv(output_path, index=False)

    print(df.head())

    return df


if __name__ == "__main__":
    update_kp_data()

# AI USE: Grok assistance in parsing datetime column