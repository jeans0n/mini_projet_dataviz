import pandas as pd

def open_and_process_data(file_path: str) -> pd.DataFrame:
    """
    Charge des données à partir d'un fichier CSV, effectue une série de pré-traitements,
    puis retourne un DataFrame pandas.
    
    Args:
        file_path (str): Le chemin du fichier CSV à charger.
    
    Returns:
        pd.DataFrame: Le DataFrame pandas prétraité.
    """
    
    # Charger les données à partir du fichier CSV
    df = pd.read_csv(file_path)
    
    # Création de la colonne 'Sector' à partir des colonnes individuelles du secteur
    sectors = ['is_software', 'is_web', 'is_mobile', 'is_enterprise', 'is_advertising', 'is_gamesvideo', 'is_ecommerce', 'is_biotech', 'is_consulting', 'is_othercategory']
    df['Sector'] = df[sectors].idxmax(axis=1)
    
    # Mappage pour renommer les secteurs
    sector_mapping = {
        'is_software': 'software',
        'is_web': 'web',
        'is_mobile': 'mobile',
        'is_enterprise': 'enterprise',
        'is_advertising': 'advertising',
        'is_gamesvideo': 'gamesvideo',
        'is_ecommerce': 'ecommerce',
        'is_biotech': 'biotech',
        'is_consulting': 'consulting',
        'is_othercategory': 'othercategory'
    }
    
    # Renommer les secteurs en utilisant le mappage
    df['Sector'] = df['Sector'].replace(sector_mapping)
    
    # Suppression des colonnes non désirées
    columns_to_drop = [
        'Unnamed: 0',
        'zip_code', 
        'id', 
        'Unnamed: 6', 
        'labels', 
        'state_code.1', 
        'object_id', 
        'closed_at', 
        'age_last_milestone_year', 
        'first_funding_at', 
        'last_funding_at', 
        'age_first_milestone_year',
        'is_CA',
        'is_NY',
        'is_MA',
        'is_TX',
        'is_otherstate'
    ]
    
    # Suppression des colonnes individuelles du secteur et des autres colonnes non désirées
    df = df.drop(columns=columns_to_drop + sectors, axis=1)
    
    return df



if __name__ == "__main__":
    file_path = "./data/startup_data.csv"
    processed_data = open_and_process_data(file_path)
    print(processed_data.columns)
    print(processed_data.head())
