import pandas as pd
import pygeohash as pgh

# latitude and logitude input 
# returns tuple with geohash_7, 6, 5 

def create_geohashes(latitude: float, longitude: float): 

    if pd.isna(latitude) or pd.isna(longitude):
        return (pd.NA, pd.NA, pd.NA)

    geohash_7 = pgh.encode(float(latitude), float(longitude), precision=7)
    return geohash_7, geohash_7[:6], geohash_7[:5]


