import json
import csv
from datetime import datetime

# Chemin vers le fichier JSON et le fichier CSV de sortie
json_file = "test_offres.json"
csv_file = "POSTULATIONS.csv"

# Charger les données JSON
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Définir la date du jour
date_postule = datetime.now().strftime("%Y-%m-%d")

# Vérifier si le fichier CSV existe déjà pour éviter de dupliquer l'en-tête
try:
    with open(csv_file, "r", encoding="utf-8") as f:
        existing_file = True
except FileNotFoundError:
    existing_file = False

# Ouvrir le fichier CSV en mode "append"
with open(csv_file, "a", encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    
    # Écrire l'en-tête uniquement si le fichier est créé pour la première fois
    if not existing_file:
        writer.writerow(["ID URL", "Entreprise", "Lieu", "Titre du Poste", "Date de Candidature", "Réponse"])

    # Extraire et écrire les données pour chaque offre
    for offre in data:
        # Récupérer les 8 derniers caractères de l'URL
        id_url = offre.get("url")
        # Récupérer les autres champs
        entreprise = offre.get("entreprise", "")
        lieu = offre.get("emplacement_poste", "")
        titre_poste = offre.get("titre", "")
        
        # Écrire la ligne dans le CSV
        writer.writerow([id_url, entreprise, lieu, titre_poste, date_postule, ""])

print("Les données ont été ajoutées à", csv_file)
