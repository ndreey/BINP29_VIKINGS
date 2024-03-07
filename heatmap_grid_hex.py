#%%
from h3 import h3 
import folium 
import colorcet as cc
import pandas as pd
import shapely as shp
import geopandas as gpd

# Function to generate hexagon for each row
def geo_hexring(lat, lng, res, ring_size):
    
    # Generates a hexagon hash.
    hex = h3.geo_to_h3(lat, lng, res)
    
    # Generates a ring of hexagons.
    ring = list(h3.k_ring(hex, ring_size))
    
    # Create a GeoDataFrame with hexagons and their vertices
    hex_geo = [shp.geometry.Polygon(h3.h3_to_geo_boundary(hexagon, geo_json= True)) for hexagon in ring]
    geo_df = gpd.GeoDataFrame({"Hex_ID": ring, "geometry": hex_geo})
    
    geo_df.crs = "EPSG:4326"
    
    return geo_df


# Read in the data
df = pd.read_excel("00_DATA/GeneticDistances.xlsx")

# Change the name of the third column
df.rename(columns={df.columns[2]: "Year_BP"}, inplace=True)

# Generate hexagon grid for the world
hexgrid = geo_hexring(50.1, 14.1, 14, 81)

# Generate basemap
map = folium.Map(location = [50.1, 14.1], tiles = "Cartodb dark_matter", zoom_start = 4)

# Plot the hexgrid on map
folium.GeoJson(hexgrid).add_to(map)

map

# %%
