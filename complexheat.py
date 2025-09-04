import pandas as pd
import folium
from folium.plugins import HeatMap, FeatureGroupSubGroup
from folium import Map, Element, LayerControl

# Load your dataset 
df = pd.read_csv('/Users/thechez/Desktop/Avista_Analysis/Data/AvistaFinalMasterData.csv')

# Data cleaning and type enforcement
df['Zipcode'] = df['Zipcode'].astype(str).str.zfill(5)
df['Electric_Utility'] = df['Electric_Utility'].astype(str)
df['LATITUDE'] = pd.to_numeric(df['LATITUDE'], errors='coerce')
df['LONGITUDE'] = pd.to_numeric(df['LONGITUDE'], errors='coerce')

# Remove any rows with missing or invalid values
df = df.dropna(subset=['LATITUDE', 'LONGITUDE', 'Zipcode', 'Electric_Utility'])

# Group by ZIP and electric utility to count customer density
grouped = df.groupby(['Zipcode', 'Electric_Utility', 'LATITUDE', 'LONGITUDE']).size().reset_index(name='CustomerCount')

# Create a map centered around the average customer location
map_center = [grouped['LATITUDE'].mean(), grouped['LONGITUDE'].mean()]
heatmap = folium.Map(location=map_center, zoom_start=6)

# Prepare heatmap data with density weights
heat_data = grouped[['LATITUDE', 'LONGITUDE', 'CustomerCount']].values.tolist()

# Add heat layer to map
HeatMap(heat_data, radius=12, max_zoom=10).add_to(heatmap)

# Create a base FeatureGroup
base_group = folium.FeatureGroup(name="All Utilities").add_to(heatmap)

# Create subgroups for each utility
utilities = grouped['Electric_Utility'].unique()
for utility in utilities:
    subgroup = FeatureGroupSubGroup(base_group, name=utility)
    heatmap.add_child(subgroup)
    
    # Filter rows for this utility
    filtered = grouped[grouped['Electric_Utility'] == utility]
    for _, row in filtered.iterrows():
        folium.CircleMarker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            radius=6,
            color='red',
            fill=True,
            fill_opacity=0.7,
            popup=f"{row['Electric_Utility']}<br>ZIP: {row['Zipcode']}<br>Count: {row['CustomerCount']}"
        ).add_to(subgroup)

folium.LayerControl(collapsed=False).add_to(heatmap)

# Add floating HTML title inside the map
title_html = '''
     <div style="
         position: fixed; 
         top: 20px; left: 50%; 
         transform: translateX(-50%);
         z-index: 9999; 
         background-color: rgba(255, 255, 255, 0.85); 
         padding: 10px; 
         font-size: 20px; 
         font-weight: bold;
         font-family: Arial, sans-serif;
         border-radius: 5px;
         box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
     ">
         Electric Utility Customer Density by ZIP Code
     </div>
'''
heatmap.get_root().html.add_child(Element(title_html))

# Save your final map
heatmap.save('electric_utility_zip_heatmap.html')

