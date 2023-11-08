
import pandas as pd

# Charger les fichiers Excel
# Remarque : Assurez-vous que les chemins des fichiers sont corrects.
export_final_df = pd.read_excel('Exports/export.xlsx')
export1_df = pd.read_excel('petit-audit.xlsx')

# Fusionner les DataFrames sur la colonne 'Email'
# On utilise 'left' join pour garder toutes les lignes de 'export_final_df' et enrichir avec 'export1_df'
merged_df = pd.merge(export_final_df, 
                     export1_df[['Email', 'Nom', 'Prénom', 'Société', 'Fonction', 'Code Postal / Ville']], 
                     on='Email', 
                     how='left')

# Exporter le DataFrame fusionné vers un fichier Excel sans l'index
merged_df.to_excel('Exports/export_with_details.xlsx', index=False)

# Remarque : Remplacez '/chemin/vers/' par les chemins réels où vos fichiers se trouvent.
