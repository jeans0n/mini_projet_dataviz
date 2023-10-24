# Import des modules nécessaires
import folium
import pandas as pd
import numpy as np
import geopandas as gpd
from generate_geodata import get_geodata

def init_map() -> folium.Map:
    """
    Initialise une carte folium.

    Returns:
        folium.Map: La carte folium initialisée.
    """
    return folium.Map(location=[37.0902, -95.7129], zoom_start=4.45, tiles=None)

def get_tooltip(fields, aliases) -> folium.GeoJsonTooltip:
    """
    Crée un tooltip pour la carte folium avec les champs et alias donnés.

    Args:
        fields (list): La liste des champs à afficher dans le tooltip.
        aliases (list): La liste des alias correspondant aux champs.

    Returns:
        folium.GeoJsonTooltip: Le tooltip créé.
    """
    tooltip = folium.GeoJsonTooltip(
        fields=fields,
        aliases=aliases,
        localize=True
    )
    return tooltip

def add_info(map, startUp_data, startups=False, relationships=False, success_count=False) -> folium.Map:
    """
    Ajoute des informations à la carte folium en fonction des paramètres donnés.

    Args:
        map (folium.Map): La carte à laquelle ajouter les informations.
        startUp_data (gpd.GeoDataFrame): Les données à utiliser pour l'ajout d'informations.
        startups (bool): Si True, ajoute le nombre total de startups par région.
        relationships (bool): Si True, ajoute la moyenne des relations par région.
        success_count (bool): Si True, ajoute le nombre de startups à succès par région.

    Returns:
        folium.Map: La carte avec les informations ajoutées.
    """
    
    fields = ['name']
    aliases = ['State: ']
    map_name = ''
    metric = 'startups'

    if startups:
        fields.append('startups')
        aliases.append('Total Startups: ')
        metric = 'startups'
        map_name = 'Start-up Density in US'
    if relationships:
        fields.append('average_relationships')
        aliases.append('Average Relationships: ')
        metric = 'average_relationships'
        map_name = "Average Relationships"
    if success_count:
        fields.append('success_count')
        aliases.append('Success Count: ')
        metric = 'success_ratio'
        map_name = "Start-up Success Ratio per Region"

    if (startups and (not success_count)) or relationships:
        values = np.log1p(startUp_data[metric])
    else:
        values = startUp_data[metric]

    colormap = folium.LinearColormap(colors=['white', 'blue'], vmin=min(values), vmax=max(values))

    tooltip = get_tooltip(fields, aliases)

    folium.GeoJson(
        startUp_data,
        name=map_name,
        style_function=lambda feature: {
            'fillColor': colormap(np.log1p(feature['properties'][metric])),
            'fillOpacity': 0.7,
            'color': 'black',
            'weight': 0.1,
        },
        tooltip=tooltip
    ).add_to(map)

    return map


def create_3maps_dict(startUp_data) -> dict[str, folium.Map]:
    """
    Crée un dictionnaire de cartes folium avec différentes informations.

    Args:
        startUp_data (gpd.GeoDataFrame): Les données à utiliser pour la création des cartes.

    Returns:
        dict[str, folium.Map]: Le dictionnaire de cartes folium créé.
    """
    maps = {}
    
    maps['startups'] = add_info(init_map(), startUp_data, startups=True)
    maps['relationships'] = add_info(init_map(), startUp_data, relationships=True)
    maps['success_ratio'] = add_info(init_map(), startUp_data, startups=True, success_count=True)
    
    return maps

if __name__ == "__main__":
    # Charger les données géographiques des start-ups
    startUp_data = get_geodata()
    
    # Créer les cartes de visualisation
    maps = create_3maps_dict(startUp_data)
    
    # Sauvegarder chaque carte dans un fichier HTML
    for key in maps:
        maps[key].save(f'{key}.html')
