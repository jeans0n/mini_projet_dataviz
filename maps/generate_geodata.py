import geopandas as gpd
import pandas as pd
from data.get_data import open_and_process_data

startUp_data = gpd.read_file("us-state-boundaries.geojson")


def update_geojson(geojson_path, data):
    # Charger les données GeoJSON
    startUp_data = gpd.read_file(geojson_path)
    
    # Compter le nombre d'entreprises par état
    entreprise_par_etat = data['name'].groupby(data['state_code']).count().reset_index()
    comptage_entreprises = dict(zip(entreprise_par_etat['state_code'], entreprise_par_etat['name']))
    
    for index, row in startUp_data.iterrows():
        try:
            comptage_entreprises[str(row['stusab'])]
        except:
            comptage_entreprises[str(row['stusab'])] = 0
    
    # Mettre à jour les données GeoJSON
    startUp_data['startups'] = startUp_data['stusab'].map(comptage_entreprises).fillna(0).astype(int)
    
    # Enregistrer le fichier GeoJSON mis à jour
    startUp_data.to_file("updated-us-state-boundaries.geojson", driver='GeoJSON')

# Exemple d'utilisation de la fonction


if __name__ == "__main__":
    geojson_path = "us-state-boundaries.geojson"
    file = "./data/startup_data.csv"
    df = open_and_process_data("../data/startup_data.csv")
    update_geojson(geojson_path, df)