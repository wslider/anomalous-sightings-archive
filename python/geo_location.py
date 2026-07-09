import pandas as pd
import pygeohash as pgh 
import numpy as np

# latitude and logitude input 
# returns tuple with geohash_7, 6, 5 

def create_geohashes(latitude: float, longitude: float): 

    if pd.isna(latitude) or pd.isna(longitude):
        return (pd.NA, pd.NA, pd.NA)

    geohash_7 = pgh.encode(float(latitude), float(longitude), precision=7)
    return geohash_7, geohash_7[:6], geohash_7[:5]


# Calculate distance between two lat/lon points (used in proximity table)
# Function provided by Grok 4 

def haversine_distance(lat1, lon1, lat2, lon2, unit='km'):

    R = 6371.0  # Earth radius in kilometers
    
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2)
    lon2_rad = np.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    distance = R * c
    
    if unit == 'miles':
        return distance * 0.621371
    return distance

# add if name = main later 