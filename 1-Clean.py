import pandas as pd
from datetime import timedelta
import os

def clean_audit_data(file_path, exports_folder):
    # Lecture du fichier Excel
    df = pd.read_excel(file_path)

    # Convertir la colonne 'Date' au format datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y %Hh%M', errors='coerce')

    # Trier et nettoyer les données
    df_sorted = df.sort_values(by=['Email', 'Date'])
    df_cleaned = df_sorted.groupby('Email').apply(lambda x: x[~(x['Date'].diff() < timedelta(minutes=2))]).reset_index(drop=True)

    # Correction de la fonction pour s'assurer d'un nombre pair d'entrées
    def add_entry_if_needed(group):
        if len(group) % 2 != 0:
            last_entry = group.iloc[-1].copy()
            last_entry['Date'] = last_entry['Date'] + timedelta(minutes=30)
            return pd.DataFrame([last_entry])
        return pd.DataFrame()

    additional_entries = df_cleaned.groupby('Email').apply(add_entry_if_needed).reset_index(drop=True)
    df_final = pd.concat([df_cleaned, additional_entries]).sort_values(by=['Email', 'Date'])

    # Enregistrer le fichier nettoyé
    clean_file_path = os.path.join(exports_folder, '1-Export-propre.csv')
    df_final.to_csv(clean_file_path, index=False)

    # Création du reporting
    reporting_df = pd.DataFrame(columns=['Statut', 'Email', 'Date'])

    # Ajout des doublons supprimés
    duplicates = df_sorted[df_sorted.duplicated(subset=['Email', 'Date'], keep=False)].copy()
    duplicates['Statut'] = 'Supprimé'
    if not duplicates.empty:
        reporting_df = pd.concat([reporting_df, duplicates[['Statut', 'Email', 'Date']]], ignore_index=True)

    # Ajout des dates rajoutées
    if not additional_entries.empty:
        added_dates = additional_entries.copy()
        added_dates['Statut'] = 'Rajouté'
        reporting_df = pd.concat([reporting_df, added_dates[['Statut', 'Email', 'Date']]], ignore_index=True)

    # Enregistrer le reporting
    reporting_file_path = os.path.join(exports_folder, '1-reporting.csv')
    reporting_df.to_csv(reporting_file_path, index=False)

    return clean_file_path, reporting_file_path

# Exemple d'utilisation
file_path = 'Exports/export-audit.xlsx'  # Correction du chemin de fichier
exports_folder = 'Exports'
clean_file_path, reporting_file_path = clean_audit_data(file_path, exports_folder)
print(f'Fichier nettoyé enregistré à : {clean_file_path}')
print(f'Fichier de reporting enregistré à : {reporting_file_path}')
