import geopandas as gpd
import pandas as pd
from get_data import open_and_process_data
import numpy as np

def get_geodata() -> gpd.GeoDataFrame:
    """
    Charge les données géographiques des frontières des États américains à partir d'un fichier GeoJSON,
    puis retourne un GeoDataFrame geopandas.
    
    Returns:
        gpd.GeoDataFrame: Le GeoDataFrame geopandas contenant les données géographiques des frontières des États américains.
    """
    
    # Charger les données géographiques des frontières des États américains à partir du fichier GeoJSON
    geo_data = gpd.read_file("updated-us-state-boundaries.geojson")
    
    return geo_data

def update_geojson(geojson_path: str, data: pd.DataFrame) -> None:
    """
    Met à jour un fichier GeoJSON avec des données supplémentaires sur les startups.

    Args:
        geojson_path (str): Le chemin d'accès au fichier GeoJSON à mettre à jour.
        data (pd.DataFrame): Le DataFrame contenant les données sur les startups.
    
    Returns:
        None
    """
    
    startUp_data = gpd.read_file(geojson_path)
    
    # --- Ajout du nombre de start-up par region ---
    #
    # Compter le nombre d'entreprises par état
    entreprise_par_etat = data['name'].groupby(data['state_code']).count().reset_index()
    comptage_entreprises = dict(zip(entreprise_par_etat['state_code'], entreprise_par_etat['name']))
    
    for index, row in startUp_data.iterrows():
        try:
            comptage_entreprises[str(row['stusab'])]
        except KeyError:
            comptage_entreprises[str(row['stusab'])] = 0 #si un etat ne possède pas de startup
    
    # Mettre à jour les données GeoJSON
    startUp_data['startups'] = startUp_data['stusab'].map(comptage_entreprises).fillna(0).astype(int)

    # --- Ajout du nombre de start-up a succes par region ---
    #
    # Filtrer les startups réussies
    successful_startups = data[data['status'] == 'acquired']
    
    # Compter le nombre de startups réussies par état
    success_counts = successful_startups['state_code'].value_counts()

    # Convertir la série résultante en un dictionnaire
    success_dict = success_counts.to_dict()

    # Mettre à jour les données GeoJSON
    startUp_data['success_count'] = startUp_data['stusab'].map(success_dict).fillna(0).astype(int)


    # --- Ajout de la relation moyenne par region ---
    #
    # Regrouper les données par code d'état et calculer les relations moyennes
    average_relationships = data.groupby('state_code')['relationships'].mean().reset_index()
    average_relationships_dict = dict(zip(average_relationships['state_code'], average_relationships['relationships']))

    # Mettre à jour les données GeoJSON
    startUp_data['average_relationships'] = startUp_data['stusab'].map(average_relationships_dict).fillna(0)

    # --- Ajout du ratio nb de succès/nb de startups par etat ---
    #
    # Calculer le ratio de succès pour chaque état
    startUp_data['success_ratio'] = np.divide(
        startUp_data['success_count'],
        startUp_data['startups'],
        out=np.zeros_like(startUp_data['success_count'], dtype=float), # on initialise tout les ratios a 0 puis on les calcule si possible
        where=startUp_data['startups'] != 0 # si il n'y a pas de start up on ne calcule pas le ratio
    )

    # Enregistrer le fichier GeoJSON mis à jour
    startUp_data.to_file("updated-us-state-boundaries.geojson", driver='GeoJSON')



if __name__ == "__main__":
    geojson_path = "us-state-boundaries.geojson"
    file = "startup_data.csv"
    df = open_and_process_data("startup_data.csv")
    update_geojson(geojson_path, df)
