
import pandas as pd

def merge_data(export_file, audit_file, output_file):
    # Charger les fichiers Excel
    export_df = pd.read_excel(export_file)
    audit_df = pd.read_excel(audit_file)

    # Sélectionner les colonnes pertinentes pour la fusion
    audit_df_relevant = audit_df[['Email', 'Nom', 'Prénom', 'Société', 'Fonction', 'Code Postal / Ville']]

    # Fusionner les données en se basant sur l'Email
    merged_df = pd.merge(export_df, audit_df_relevant, on='Email', how='left')

    # Enlever les doublons au cas où un visiteur est présent plusieurs fois dans une même conférence
    merged_df.drop_duplicates(subset=['Email', 'Conférence'], inplace=True)

    # Écrire le résultat dans un nouveau fichier Excel
    merged_df.to_excel(output_file, index=False)

    print(f'Data merged successfully into {output_file}')

if __name__ == "__main__":
    # Définir les chemins des fichiers
    export_path = 'Exports/export.xlsx'
    audit_path = 'Exports/petit-audit.xlsx'
    output_path = 'Exports/export-detail.xlsx'
    
    # Appel de la fonction de fusion
    merge_data(export_path, audit_path, output_path)
