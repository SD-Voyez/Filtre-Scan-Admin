
import pandas as pd
from datetime import datetime, timedelta

def parse_date(date_str):
    return datetime.strptime(date_str, '%d/%m/%Y %Hh%M')

def was_present(start, end, times):
    presence = timedelta(0)
    half_duration = (end - start) / 2
    i = 0
    while i < len(times):
        arrival = times[i]
        departure = times[i + 1] if i + 1 < len(times) else end
        i += 2

        # Calcul de la durée de présence dans l'intervalle
        if arrival < end and departure > start:
            presence += min(departure, end) - max(arrival, start)

    return presence >= half_duration

# Lecture des fichiers CSV
horaires_confs = pd.read_csv('Exports/horaires-confs.csv', encoding='utf-8-sig')
export_propre = pd.read_csv('Exports/1-Export-propre.csv', encoding='utf-8-sig')

# Conversion des horaires des conférences
horaires_confs['début'] = horaires_confs['début'].apply(parse_date)
horaires_confs['fin'] = horaires_confs['fin'].apply(parse_date)

# Préparation des données des visiteurs
export_propre['Date'] = pd.to_datetime(export_propre['Date'])
visitors = export_propre.groupby(['Nom', 'Prénom', 'Société', 'Fonction', 'Email', 'Code Postal / Ville'])

# Analyse de la présence des visiteurs aux conférences
results = []
for name, group in visitors:
    times = group['Date'].tolist()
    attended = False

    for index, row in horaires_confs.iterrows():
        if was_present(row['début'], row['fin'], times):
            attended = True
            results.append([row['Conférence'], *name])

    if not attended:
        results.append(['Aucune conférence', *name])

# Création du dataframe final et export en CSV
final_df = pd.DataFrame(results, columns=['Conférence', 'Nom', 'Prénom', 'Société', 'Fonction', 'Email', 'Code Postal / Ville'])
final_df.to_csv('Exports/2-Export-attribution.csv', index=False, encoding='utf-8-sig')