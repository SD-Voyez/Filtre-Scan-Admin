
import pandas as pd
from datetime import datetime, timedelta

# Charger les fichiers Excel
horaire_conf = pd.read_excel('horaire conf.xlsx')
export1 = pd.read_excel('export1.xlsx')

# Convertir les colonnes de date en datetime
horaire_conf['début'] = pd.to_datetime(horaire_conf['début'], format='%d/%m/%Y %Hh%M')
horaire_conf['fin'] = pd.to_datetime(horaire_conf['fin'], format='%d/%m/%Y %Hh%M')
export1['Date'] = pd.to_datetime(export1['Date'], format='%d/%m/%Y %Hh%M')

# Calculer la durée de chaque conférence
horaire_conf['durée'] = horaire_conf['fin'] - horaire_conf['début']

# Créer une liste pour chaque participant contenant des tuples (entrée, sortie)
participants_intervals = {}

for index, row in export1.iterrows():
    prenom = row['Prénom']
    date = row['Date']
    
    if prenom not in participants_intervals:
        participants_intervals[prenom] = [date]
    else:
        # Si la dernière date est une entrée, alors celle-ci est une sortie
        if len(participants_intervals[prenom]) % 2 != 0:
            participants_intervals[prenom].append(date)
        # Sinon, c'est une nouvelle entrée
        else:
            participants_intervals[prenom].append(date)

# Transformer la liste de dates en tuples (entrée, sortie)
for prenom, dates in participants_intervals.items():
    participants_intervals[prenom] = list(zip(dates[::2], dates[1::2]))

# Calculer la présence pour chaque participant et chaque conférence
resultats_50_correct = []

for index, conf in horaire_conf.iterrows():
    conf_name = conf['Conférence']
    conf_debut = conf['début']
    conf_fin = conf['fin']
    conf_duree = conf['durée']
    
    for participant, intervals in participants_intervals.items():
        temps_presence = timedelta(0)
        for entree, sortie in intervals:
            # Calculer le temps de présence pendant la conférence
            temps_presence += max(min(sortie, conf_fin) - max(entree, conf_debut), timedelta(0))
        
        # Vérifier si le participant a assisté à au moins 50% de la conférence
        if temps_presence >= conf_duree * 0.5:
            resultats_50_correct.append({'Conférence': conf_name, 'Nom': participant})

# Convertir les résultats en DataFrame
resultats_50_correct_df = pd.DataFrame(resultats_50_correct)

# Afficher tout le tableau des résultats
print(resultats_50_correct_df)
