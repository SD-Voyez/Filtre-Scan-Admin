## Solution pour trier les données Conférences Techniques
### Méthode de scan choisie => Scans entrées / Scans sorties

#### Process : 
1. Indiquez les horaires des conférences à jour dans un fichier horaires-confs.csv
2. Télécharger le fichier des scans de la journée correspondant à la salle de conf. (ici pour l'exemple "export-audit.xlsx") => à DL depuis l'[Admin Scan](https://www.enerj-meeting.com)
3. Traiter le fichier à l'aide du script "1-Clean.py" => 2 fichiers seront créer, un reporting et un fichier "1-Export-propre.csv"
4. Lancer le deuxième script "2-Attribution-Conf.py" qui générera le fichier final "2-Export-attribution.csv"

------------
## Idée référente & solution imaginée
#### Schéma situationnel :
Modèle exemple :
[[Schema-config-visiteur-conf.png]]
#### Prompt utilisé :
Voici deux fichier cvs :
- 1 fichier "horaires-confs.csv" avec les horaires de plusieurs conférences qui ont eu le lieu le jour de l'événement.
- 1 fichier "1-Export-propre.csv" avec la liste des visiteurs ayant participés à ces conférences le jour de l'événement.

Dans le fichier "1-Export-propre.csv", nous avons les informations suivantes pour chaque visiteur :
- Ses informations personnelles
- Un champs "Date" qui indique les horaires d'entrés et de sortie à la salle de conférence, a considérer dans l'ordre. Ainsi la première date est son entré dans la salle de conférence, la suivante sa sortie de la salle, et ainsi de suite. 

On considère qu'un visiteur a assisté a une conférence s'il était présent pendant au moins 50% de cette même conférence.
S'il est rentré trop tard, ou sortie trop tot, nous ne le comptons pas comme présent.

L'objectif : 
- Tu devras créer un script .py (nommé "2-Attribution-Conf.py") qui générera un fichier csv (nommé 2-Export-attribution.csv).
- Ce fichier CSV devra comporter pour chaque conférences les visiteur présents, sous la fomre : Conférence, Nom, Prénom, Société, Fonction, Email, Code Postal / Ville
- Tu pourras également indiquer à la fin de ce CSV, ceux qui ont assisté à aucune conférence.

Est-ce que tu as besoin d'autres informations ?
Si non, tu peux commencer.

