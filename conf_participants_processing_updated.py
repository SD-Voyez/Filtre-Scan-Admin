
import pandas as pd
from datetime import datetime, timedelta

# Charger les fichiers Excel
horaire_conf = pd.read_excel('horaires-confs.xlsx')
export1 = pd.read_excel('petit-audit.xlsx')

# Convertir les colonnes de date en datetime
horaire_conf['début'] = pd.to_datetime(horaire_conf['début'], format='%d/%m/%Y %Hh%M')
horaire_conf['fin'] = pd.to_datetime(horaire_conf['fin'], format='%d/%m/%Y %Hh%M')
export1['Date'] = pd.to_datetime(export1['Date'], format='%d/%m/%Y %Hh%M')

# Calculer la durée de chaque conférence
horaire_conf['durée'] = horaire_conf['fin'] - horaire_conf['début']

# Créer une liste pour chaque participant contenant des tuples (entrée, sortie)
participants_intervals = {}

for index, row in export1.iterrows():
    email = row['Email']
    date = row['Date']
    
    if email not in participants_intervals:
        participants_intervals[email] = [date]
    else:
        # Si la dernière date est une entrée, alors celle-ci est une sortie
        if len(participants_intervals[email]) % 2 != 0:
            participants_intervals[email].append(date)
        # Sinon, c'est une nouvelle entrée
        else:
            participants_intervals[email].append(date)

# Transformer la liste de dates en tuples (entrée, sortie)
for email, dates in participants_intervals.items():
    participants_intervals[email] = list(zip(dates[::2], dates[1::2]))

# Calculer la présence pour chaque participant et chaque conférence
resultats = []

for index, conf in horaire_conf.iterrows():
    conf_name = conf['Conférence']
    conf_debut = conf['début']
    conf_fin = conf['fin']
    conf_duree = conf['durée']
    
    for index, participant in export1.iterrows():
        email = participant['Email']
        intervals = participants_intervals.get(email, [])
        temps_presence = timedelta(0)
        
        for entree, sortie in intervals:
            # Calculer le temps de présence pendant la conférence
            temps_presence += max(min(sortie, conf_fin) - max(entree, conf_debut), timedelta(0))
        
        # Vérifier si le participant a assisté à au moins 50% de la conférence
        if temps_presence >= conf_duree * 0.5:
            # Ajouter les informations supplémentaires du participant
            resultats.append({
                'Conférence': conf_name,
                'Nom': participant['Nom'],
                'Prénom': participant['Prénom'],
                'Société': participant['Société'],
                'Email': email,
                'Code Postal / Ville': participant['Code Postal / Ville']
            })

# Convertir directement la liste en DataFrame avec les noms de colonnes spécifiés
resultats_df = pd.DataFrame(resultats)

# Exporter le DataFrame vers un fichier Excel sans l'index
resultats_df.to_excel('export_final.xlsx', index=False)
