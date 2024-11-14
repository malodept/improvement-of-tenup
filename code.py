import json
import pandas as pd
import folium


# Paths of the json files 
file_paths = [
    "D:/malo/Documents/projets/tenup carte/tournois_p1.json",
    "D:/malo/Documents/projets/tenup carte/tournois_p2.json",
    "D:/malo/Documents/projets/tenup carte/tournois_p3.json",
    "D:/malo/Documents/projets/tenup carte/tournois_p4.json",
    "D:/malo/Documents/projets/tenup carte/tournois_p5.json",
    "D:/malo/Documents/projets/tenup carte/tournois_p6.json"
]

# List to save the dataframes
dataframes = []

# JSON files loading and add to the list
for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        df = pd.DataFrame(data)
        dataframes.append(df)

# Concatenate all the dataframes in 1
df_combined = pd.concat(dataframes, ignore_index=True)

#Save the dataframe
output_path = "D:/malo/Documents/projets/tenup carte/tournois.xlsx"
df_combined.to_excel(output_path, index=False)

# Filtrer for the tournaments containing geo coordonates
df_combined = df_combined[df_combined['installation'].apply(lambda x: 'lat' in x and 'lng' in x)]
# --- First Map: Tournaments only ---
tournaments_map = folium.Map(location=[48.8566, 2.3522], zoom_start=10)  # Centered on Paris

# Add tournament points to the map
for _, row in df_combined.iterrows():
    lat = row['installation']['lat']
    lng = row['installation']['lng']
    tournoi_id = row['id']
    nom_club = row['installation']['nom']
    
    # Create a link to the tournament page
    lien_tournoi = f"https://tenup.fft.fr/tournoi/{tournoi_id}"
    
    # Add a marker on the map with a clickable link
    popup = folium.Popup(f"<a href='{lien_tournoi}' target='_blank'>{nom_club}</a>", max_width=300)
    folium.Marker([lat, lng], popup=popup, tooltip=nom_club).add_to(tournaments_map)

# Save the tournaments map as an HTML file
tournaments_map_path = "D:/malo/Documents/projets/tenup carte/carte_tournois.html"
tournaments_map.save(tournaments_map_path)

# --- Second Map: Rail Network only ---
# Path to your rail network GeoJSON file
rail_network_path = "D:/malo/Documents/projets/tenup carte/hotosm_fra_railways_lines_geojson.geojson"

# Create a new map centered on Paris for the rail network
rail_map = folium.Map(location=[48.8566, 2.3522], zoom_start=10)

# Add rail network layer
try:
    folium.GeoJson(
        rail_network_path,
        name="Rail Network",
        style_function=lambda feature: {
            'color': 'blue',
            'weight': 2,
            'opacity': 0.6,
        }
    ).add_to(rail_map)
except FileNotFoundError:
    print(f"Warning: Rail network GeoJSON file not found at {rail_network_path}")

# Add tournament points to the map
for _, row in df_combined.iterrows():
    lat = row['installation']['lat']
    lng = row['installation']['lng']
    tournoi_id = row['id']
    nom_club = row['installation']['nom']
    
    # Create a link to the tournament page
    lien_tournoi = f"https://tenup.fft.fr/tournoi/{tournoi_id}"
    
    # Add a marker on the map with a clickable link
    popup = folium.Popup(f"<a href='{lien_tournoi}' target='_blank'>{nom_club}</a>", max_width=300)
    folium.Marker([lat, lng], popup=popup, tooltip=nom_club).add_to(rail_map)

# Save the rail network map as an HTML file
rail_map_path = "D:/malo/Documents/projets/tenup carte/carte_rail_network.html"
rail_map.save(rail_map_path)