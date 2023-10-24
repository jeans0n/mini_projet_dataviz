# Importation des librairies nécessaires
import pandas as pd

# Définition de la fonction de prétraitement des données
def open_and_process_data(file_path) -> pd.DataFrame :
    # Chargement des données
    df = pd.read_csv(file_path)
    
    # Suppression des colonnes non désirées
    columns_to_drop = ['Unnamed: 0', 'zip_code', 'id', 'Unnamed: 6', 'labels', 'state_code.1', 'object_id', 'closed_at', 'age_last_milestone_year', 'first_funding_at', 'last_funding_at', 'age_first_milestone_year']
    df = df.drop(columns_to_drop, axis=1)

    # Création de la colonne 'state' à partir des colonnes existantes
    df['state'] = df[['is_CA', 'is_NY', 'is_MA', 'is_TX', 'is_otherstate']].idxmax(axis=1)
    df['state'] = df['state'].apply(lambda x: x[3:] if x != 'is_otherstate' else 'Other')

    # Suppression des colonnes d'état individuelles
    df = df.drop(['is_CA', 'is_NY', 'is_MA', 'is_TX', 'is_otherstate'], axis=1)

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

    # Suppression des colonnes individuelles du secteur
    df = df.drop(sectors, axis=1)
    
    # Retourner le DataFrame prétraité
    return df

# Test de la fonction de prétraitement des données
if __name__ == "__main__":
    file_path = "./data/startup_data.csv"
    processed_data = open_and_process_data(file_path)
    print(processed_data.columns)
    print(processed_data.head())
