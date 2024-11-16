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
search_url = "https://www.apec.fr/candidat/recherche-emploi.html/emploi?typesConvention=143684&typesConvention=143685&typesConvention=143686&typesConvention=143687&typesConvention=143706&lieux=75&motsCles=statistique&page=0"

# Accès à la page
driver.get(search_url)
time.sleep(10)  # Attendre que la page se charge complètement

# Ouverture du fichier CSV en mode écriture pour sauvegarder les URLs au fur et à mesure
with open('urls_offres_apec.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["URL"])  # Écriture de l'en-tête du fichier CSV une fois au début

    # Fonction pour cliquer sur le bouton "Suivant"
    def cliquer_sur_suivant():
        try:
            # Attendre que le bouton "Suivant" soit cliquable
            bouton = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "li.page-item.next > a.page-link"))
            )
            bouton.click()
            time.sleep(5)  # Attendre un peu pour que les offres se chargent
            return True
        except Exception as e:
            print("Erreur ou plus de bouton 'Suivant' :", e)
            return False

    # Boucle pour récupérer les URLs de chaque page
    while True:
        # Attendre que les offres soient chargées
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".container-result > div > a"))
        )

        # Récupération des éléments contenant les liens vers les offres
        offre_elements = driver.find_elements(By.CSS_SELECTOR, ".container-result > div > a")
        
        # Extraire les URLs des offres et les ajouter au fichier CSV
        urls = [offre.get_attribute('href') for offre in offre_elements]
        for url in urls:
            writer.writerow([url])
        
        print(f"{len(urls)} URLs ont été extraites de la page actuelle.")
        
        # Tenter de cliquer sur "Suivant" pour charger la page suivante
        if not cliquer_sur_suivant():
            break  # Quitter la boucle si le bouton "Suivant" n'est plus disponible

print(f"{len(urls)} URLs ont été extraites et sauvegardées dans 'urls_offres_apec.csv'.")


