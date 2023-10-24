import geopandas as gpd
import pandas as pd
from get_data import open_and_process_data
import numpy as np

def get_geodata() : 
    return gpd.read_file("updated-us-state-boundaries.geojson")

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
    
    # Filter the dataframe for successful startups
    successful_startups = df[df['status'] == 'acquired']
    # Count the number of successful startups for each state
    success_counts = successful_startups['state_code'].value_counts()

    # Group data by state code and calculate average relationships
    average_relationships = df.groupby('state_code')['relationships'].mean().reset_index()
    average_relationships_dict = dict(zip(average_relationships['state_code'], average_relationships['relationships']))



    # Convert the resulting Series to a dictionary
    success_dict = success_counts.to_dict()

    # Mettre à jour les données GeoJSON
    startUp_data['startups'] = startUp_data['stusab'].map(comptage_entreprises).fillna(0).astype(int)
    startUp_data['success_count'] = startUp_data['stusab'].map(success_dict).fillna(0).astype(int)
    startUp_data['average_relationships'] = startUp_data['stusab'].map(average_relationships_dict).fillna(0)
     # Calculer le ratio de succès pour chaque état
    startUp_data['success_ratio'] = np.divide(startUp_data['success_count'], startUp_data['startups'], out=np.zeros_like(startUp_data['success_count'], dtype=float), where=startUp_data['startups']!=0)


    # Enregistrer le fichier GeoJSON mis à jour
    startUp_data.to_file("updated-us-state-boundaries.geojson", driver='GeoJSON')



if __name__ == "__main__":
    geojson_path = "us-state-boundaries.geojson"
    file = "startup_data.csv"
    df = open_and_process_data("startup_data.csv")
    update_geojson(geojson_path, df)