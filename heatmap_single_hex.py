#%%
from h3 import h3 
import folium 
import colorcet as cc
import pandas as pd
import numpy as np

# Function to generate hexagon for each row
def generate_hex(lat, lng, res):
    
    # Generates a hexagon hash.
    hex = h3.geo_to_h3(lat, lng, res)
    
    # Returns a list of the vertices of the hexagon.
    return hex

def get_gradient(number, transform = 1):
    # Set number to a integer
    number = int(number*100)
    
    # Create a color map from blue to red
    gradient = cc.CET_L8[28:228:2]
    # Map the number to the color
    color = gradient[int(number*transform)]
    
    
    return color



# Read in the data
df = pd.read_excel("00_DATA/GeneticDistances.xlsx")

# Change the name of the third column
df.rename(columns={df.columns[2]: "Year_BP"}, inplace=True)

# Generate hexagons for each population id.
df["h3.hex"] = df.apply(
    lambda row: generate_hex(row["Lat"], row["Long"], 6), axis = 1
    )

# Parent hex as key, value as a list with g_dist and neighbours
hexagons_dict = {} 
for index, row in df.iterrows():
    
    # Get hex_id
    id = row["h3.hex"]
    
    # Get the neighbours
    neighbors = h3.k_ring_distances(id, 13)
    
    # Get the value
    g_dist = row["Dist"]
    
    # Append to hexagons_dict and hexagons_value
    hexagons_dict[id] = [neighbors, g_dist]
    

# To generate smooth color gradient between parents, we need to store the
# neighbours that have been painted and their gradient value.
# If the old gradient is less than the new one, we update the value.
colored_hex = {}

# Step list of 0 to 1 in increments of 0.05
step_list = np.arange(0, 1.05, 0.05)[::-1]


##### Lets check which hexagorns are to be painted and not painted.
# Loop through the hexagon dictionary   
for hexagons in hexagons_dict.values():
    # Loop through the rings around the parent hexagon
    for idx, ring in enumerate(hexagons[0]):
        
        # Get the genetic distance of the parent hexagon
        g_value = hexagons[1]
        
        # Get the gradient step, the first ring is always the parent.
        step = step_list[idx]
        
        # If the hexagon has been painted, we check if the new gradient is
        # greater than the old one. If greater, we update the value.   
        for hex_hash in ring:            
            if hex_hash in colored_hex:
                if colored_hex[hex_hash] > g_value*step:
                    continue
            else:
                colored_hex[hex_hash] = g_value*step


# Generate basemap
map = folium.Map(location = [50.1, 14.1], 
                 tiles = "Cartodb dark_matter", 
                 zoom_start = 4,
                 max_bounds = True)

# Plot hexagons        
for hexa, gradient in colored_hex.items(): 
    # Get color for hexagon
    col = get_gradient(gradient)
    # Plot the neighbour                
    folium.Polygon(
        locations = h3.h3_to_geo_boundary(hexa, geo_json = False),
        stroke = False,
        color = col,
        weight = 0,
        fill_color=col,
        fill_opacity=0.9,
        fill=True
    ).add_to(map)

# Plot the map
map


# %%
