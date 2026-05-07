import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("complete.csv", usecols=range(0, 11))
df.info()

df['datetime'] = pd.to_datetime(df['datetime'].astype(str), errors='coerce')

print("Datetime conversion summary:")
print(df['datetime'].describe())
print(f"\nMissing datetimes: {df['datetime'].isna().sum():,}")

# Drop rows that couldn't be parsed 
df = df.dropna(subset=['datetime']).copy()

# post-2010 sightings dataframe to insert weather data into
# Fix: Use a string or proper datetime for comparison
sighting_wx_df = df[df['datetime'] >= '2010-01-01'].copy()
sighting_wx_df['rounded_dt'] = sighting_wx_df['datetime'].dt.round('h')
sighting_wx_df['date_str'] = sighting_wx_df['rounded_dt'].dt.strftime('%Y-%m-%d')
sighting_wx_df['hour_str'] = sighting_wx_df['rounded_dt'].dt.strftime('%H') 

sighting_wx_df.head()


sighting_wx_df["hour_num"] = pd.to_numeric(sighting_wx_df['hour_str'])

plt.figure(figsize=(9,6))
plt.hist(sighting_wx_df['hour_num'].dropna(), 
         bins=27,                    
         color="#170141", 
         alpha=0.8)

plt.xlabel("Time of Day / Night (24 Hours)")
plt.ylabel("Number of Sightings")
plt.title("Sightings Peak at Around 10PM", fontsize=18, pad=18)

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()


# number of people awake vs sighting frequency (highest at 10pm)
    # is that only because people are still awake and it is dark? 

# cloudiness vs sighting frequency .. expected vs outliers 

# temperature and sightings 

# latitude and longitude of us sightings
    # population weighted us sightings
    # factor in cloud cover 
