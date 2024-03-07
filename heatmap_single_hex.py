#%%
from h3 import h3 
import folium 
import colorcet as cc
import pandas as pd

# Function to generate hexagon for each row
def generate_hex(lat, lng, res):
    
    # Generates a hexagon hash.
    hex = h3.geo_to_h3(lat, lng, res)
    
    # Returns a list of the vertices of the hexagon.
    return hex

def get_gradient(number, step = 1):
    # Set number to a integer
    number = int(number*100)
    
    # Create a color map from blue to red
    gradient = cc.CET_L8[28:228:2]
    # Map the number to the color
    color = gradient[int(number*step)]
    
    
    return color



# Read in the data
df = pd.read_excel("00_DATA/GeneticDistances.xlsx")

# Change the name of the third column
df.rename(columns={df.columns[2]: "Year_BP"}, inplace=True)

# Generate hexagons for each population id.
df["h3.hex"] = df.apply(
    lambda row: generate_hex(row["Lat"], row["Long"], 4), axis = 1
    )


# Generate basemap
map = folium.Map(location = [50.1, 14.1], tiles = "Cartodb dark_matter", zoom_start = 4)



# Parent hex as key, value as a list with g_dist and neighbours
hexagons_dict = {} 

for index, row in df.iterrows():
    
    # Get hex_id
    id = row["h3.hex"]
    
    # Get the neighbours
    neighbors = h3.k_ring_distances(id, 3)
    
    # Get the value
    g_dist = row["Dist"]
    
    # Append to hexagons_dict and hexagons_value
    hexagons_dict[id] = [neighbors, g_dist]
    

# To generate smooth color gradient between parents, we need to store the
# neighbours that have been painted and their gradient value.
# If the old gradient is less than the new one, we update the value.
colored_hex = {}

# Plot the hexagons    
for parent, items in hexagons_dict.items():
    
    # Store the hexagon and the gradient value
    colored_hex[parent] = items[1]
    
    # Get the parent color
    p_col = get_gradient(items[1])
    
    # Plot the parent
    folium.Polygon(
        locations = h3.h3_to_geo_boundary(parent, geo_json = False),
        color=p_col,
        weight=0,
        fill_color=p_col,
        fill_opacity=0.4,
        fill=True
    ).add_to(map)
    
    for idx, neighbour in enumerate(items[0][1:]):
        
        if idx == 0:
            step = 0.95
            
        elif idx == 1:
            step = 0.90
            
        else:
            step = 0.85
        
        # If the neighbour has been painted, we check if the new gradient is
        # greater than the old one. If so, we update the value.
        paint = True
        
        for hex_hash in neighbour:            
            if hex_hash in colored_hex:
                if colored_hex[hex_hash] > items[1]*step:
                    paint = False
                else:
                    paint = True
                    colored_hex[hex_hash] = items[1]*step
        
            if paint:    
                # Get color for neighbor
                n_col = get_gradient(items[1], step = step)

                # Plot the neighbours
                
                folium.Polygon(
                    locations = h3.h3_to_geo_boundary(hex_hash, geo_json = False),
                    color=n_col,
                    weight=0,
                    fill_color=n_col,
                    fill_opacity=0.4,
                    fill=True
                ).add_to(map)

# Plot the map
map


# %%
