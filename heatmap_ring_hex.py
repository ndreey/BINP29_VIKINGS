#%%
from h3 import h3 
import folium 
import colorcet as cc
import pandas as pd
import shapely as shp
import geopandas as gpd



# Function to generate hexagons within hexagons.
def ripple_hex(lat, lng, init_res, n_ripples):
    
    # Generates a hexagon hash.
    for i in range(init_res, n_ripples):
        hex = h3.geo_to_h3(lat, lng, i)
        hex = h3.h3_to_children(hex, i+1)
        hex = h3.geo_to_h3(lat, lng, res)
    
    # Returns a list of the vertices of the hexagon.
    return h3.h3_to_geo_boundary(hex, geo_json = False)