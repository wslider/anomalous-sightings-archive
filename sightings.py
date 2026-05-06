import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("complete.csv", usecols=range(0, 11))
df.info()

#latitude is a str (with incorrect mixed values like dates) - remove dates and convert to float
df["latitude"] = pd.to_numeric(
    df["latitude"].astype(str).str.replace(r".*/.*", "", regex=True),
    errors="coerce"
)

# new column in df - rounded latitudes for lower 48 US states ("country" == us & "latitude" between 24 North and 50 North)
df["rounded_lat"] = df["latitude"].where((df["country"].str.lower() == "us") & (df["latitude"].between(24, 50))).round(0)

count = df["rounded_lat"].value_counts().sort_index()

mean_latitude = df["latitude"].where((df["country"].str.lower() == "us") & (df["latitude"].between(24, 50))).mean().round(2)

louisville_latitude = 38.25

# count occurances of sightings in us at rounded latitudes 

plt.figure(figsize=(10,6))

plt.bar(count.index, count.values, color="#170141",  alpha=0.8)

plt.xlabel("Latitude")
plt.ylabel("Number of Sightings")
plt.suptitle("What is the Average Latitude of UFO Sightings in The US?", fontsize=20)
plt.title("*Lower 48 States Included", fontsize=10, pad=20)


ax = plt.gca()
ax.axvline(
    mean_latitude, 
    linewidth = 1, 
    color = "#3a3b45"
)

ax.text(
    mean_latitude +0.2, 
    7000,
    f"← Average Latitude of Sightings\n   {mean_latitude}° N",
    color = "#3a3b45"
)

ax.axvline(
    louisville_latitude, 
    linewidth = 1, 
    color = "#006c0e"
)

ax.text(
    louisville_latitude -5.7, 
    7000,
    f"Latitude of Louisville, KY →\n{louisville_latitude}° N",
    color = "#006c0e",
)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# lowest and highest latitudes of lower 48 states (24 - 49)
plt.xlim(23, 50)

# allow space in y axis for ax.text labels
plt.ylim(0, 8000)

plt.tight_layout()
plt.show()






# ================== time of sightings ================================================

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

plt.tight_layout()
plt.show()


# number of people awake vs sighting frequency (highest at 10pm)
    # is that only because people are still awake and it is dark? 

# cloudiness vs sighting frequency .. expected vs outliers 

# temperature and sightings 

# latitude and longitude of us sightings
    # population weighted us sightings
    # factor in cloud cover 
