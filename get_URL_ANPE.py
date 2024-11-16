from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import json

# Configuration du WebDriver avec ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL de la page principale des offres d'emploi
search_url = "https://candidat.francetravail.fr/offres/recherche"

# Accès à la page
driver.get(search_url)
time.sleep(30)  # Attendre que la page se charge complètement

def cliquer_sur_afficher_plus():
    try:
        # Attendre que le bouton soit visible et cliquable
        bouton = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#zoneAfficherPlus a.btn.btn-primary"))
        )
        bouton.click()
        time.sleep(2)  # Attendre un peu après chaque clic pour que les nouvelles offres se chargent
        return True
    except Exception as e:
        print("Erreur ou plus de bouton 'Afficher plus d'offres' :", e)
        return False

# Boucle pour cliquer sur le bouton jusqu'à ce qu'il n'y en ait plus
while cliquer_sur_afficher_plus():
    pass

# Récupération des éléments contenant les liens vers les offres
offre_elements = driver.find_elements(By.CSS_SELECTOR, "a.media.with-fav")

# Extraire les URLs des offres
urls = [offre.get_attribute('href') for offre in offre_elements]

# Exporter les URLs vers un fichier CSV
with open('urls_offres.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["URL"])
    for url in urls:
        writer.writerow([url])

print(f"{len(urls)} URLs ont été extraites et sauvegardées dans 'urls_offres.csv'.")

###########################################
################################### 2éme partie : on stock tous les descrp d'offre dans un .json
###########################################

# Chemin vers le fichier CSV contenant les URLs des offres
csv_file_path = 'urls_offres.csv'

# Liste pour stocker les données des offres
offres_data = []

# Lecture des URLs depuis le fichier CSV
with open(csv_file_path, mode='r') as file:
    reader = csv.DictReader(file)
    urls = [row['URL'] for row in reader]

# Parcours de chaque URL pour extraire les détails de l'offre
for url in urls:
    driver.get(url)
    
    try:
        # Attendre que le titre de l'offre soit présent avant de continuer (max 25 secondes)
        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1#labelPopinDetailsOffre span[itemprop='title']")))

        # Titre de l'offre
        titre = driver.find_element(By.CSS_SELECTOR, "h1#labelPopinDetailsOffre span[itemprop='title']").text

        # Description de l'offre
        description = driver.find_element(By.CSS_SELECTOR, "div[itemprop='description']").text

        # Nom de l'entreprise (gérer les absences)
        try:
            entreprise = driver.find_element(By.CSS_SELECTOR, "div.media h3.t4.title").text
        except:
            entreprise = ""
        
        # Emplacement de l'entreprise
        try:
            emplacement_poste = driver.find_element(By.CSS_SELECTOR, "span[itemprop='name']").text
        except:
            emplacement_poste = ""

        # Description de l'entreprise
        description_entreprise = driver.find_element(By.CSS_SELECTOR, "div.media-body p").text

        # Stocker les données sous forme de dictionnaire
        offre_info = {
            "url": url,
            "titre": titre,
            "description": description,
            "entreprise": entreprise,
            "emplacement_poste": emplacement_poste,
            "description_entreprise": description_entreprise
        }

        offres_data.append(offre_info)
        print(f"Informations extraites pour l'offre : {titre}")

    except Exception as e:
        print(f"Erreur lors de l'extraction de l'offre {url}: {e}")

# Exporter les données extraites au format JSON
json_file_path = 'offres_data.json'
with open(json_file_path, mode='w', encoding='utf-8') as json_file:
    json.dump(offres_data, json_file, ensure_ascii=False, indent=4)

print(f"Les données des offres ont été sauvegardées dans '{json_file_path}'.")

# Fermer le navigateur
driver.quit()

###########################################
################################### 3éme partie : on filtre pour n'avoir que les offres data/stat
###########################################

import json

# Charger les données à partir du fichier JSON contenant toutes les offres
with open('offres_data.json', 'r', encoding='utf-8') as f:
    offres = json.load(f)

# Définir les mots-clés à rechercher
mots_cles = ["data", "données", "BDD", "statistique"]

# Filtrer les offres contenant un des mots-clés dans le titre ou la description
offres_filtrees = [
    offre for offre in offres
    if any(mot in offre['titre'].lower() or mot in offre['description'].lower() for mot in mots_cles)
]

# Sauvegarder les résultats dans un nouveau fichier JSON
with open('offres_filtrees.json', 'w', encoding='utf-8') as f:
    json.dump(offres_filtrees, f, ensure_ascii=False, indent=4)

print(f"{len(offres_filtrees)} offres d'emploi trouvées contenant les mots-clés.")

###########################################
################################### 4éme partie : on retire les offres déja traités
###########################################


# Chemin de ton fichier JSON
file_path_offres_filtrees = "offres_filtrees.json"

# Liste des terminaisons d'URL à exclure
exclusions = [
    "183CZMX", "6818745", "5874723", "7053270", "6202478", "6114084", 
    "183RYHM", "6603033", "183TFQB", "183HKJW", "5717245", "6199508"
]

# Charger les données JSON
with open(file_path_offres_filtrees, "r", encoding="utf-8") as f:
    data = json.load(f)

# Filtrer les données
filtered_data = [
    item for item in data 
    if not any(item.get("url", "").endswith(exclusion) for exclusion in exclusions)
]

# Écraser le fichier d'origine avec les données filtrées
with open(file_path_offres_filtrees, "w", encoding="utf-8") as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=4)

print(f"{len(filtered_data)} offres d'emploi aprés soustraction.")


