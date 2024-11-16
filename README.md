# **AutoCVFetcher**  

## **Description**  
Un outil utilisant Python et l'API d'OpenAI pour automatisé la récupération d'offre d'emploi, puis :
Générer, télécharger et organiser les CV et les lettres de motivation personnalisés en fonction des offres d'emploi récupérer et d'un profil donné.
Les CV et lettres sont créés à partir de modèles personnalisés en LaTeX (Compilateur à choisir parmis les package python : PdfLaTeX, LuLaTeX ou XuLaTeX), organisés dans un répertoire spécifiques, et peuvent être générés en réponse à des offres d'emploi récupérées via web scraping ou des fichiers JSON.

### **Fonctionnalités principales**  
- Génération automatisée de CV et lettre basés sur des modèles.  
- Organisation par numérotation des fichiers téléchargés.  
- Prévention des doublons dans les téléchargements.  
- Personnalisation des éléments clés des CV et des lettres : titre, contenu, etc...  
- Intégration avec des outils externes tels que LaTeX ou les sites de l'APEC et de l'ANPE  (via scraping/API).  

---

## **Fichiers python du projet**  
Voici les fichiers python utilisées et leur fonction :  

| **Fichiers**             | **Description**                                                                                                                    |  
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------|  
| `get_URL_ANPE.py`        | On cherche (selon une liste de mot clés à définir) les offres d'emplois sur le site de l'ANPE qui correspondent à notre profil     |  
| `get_URL_APEC.py`        | On cherche (selon une liste de mot clés à définir) les offres d'emplois sur le site de l'APEC qui correspondent à notre profil     |  
| `prompt_openai.py`       | On génére les lettre de motivation et CV pour chaque offre et on les stockent dans un fichier resultats.json                       |  
| `to_cv.py`               | Les données dans resultats.json sont compilé une à une dans ce script                                                              |  
| `to_let_motiv.py`        | Les données dans resultats.json sont compilé une à une dans ce script                                                              |  
| `PDF_compress.py`        | Les données sont compressé au cas ou les images sont trop grosse                                                                   |  
| `enregistrer.py`         | Les offres qui ont été faites sont enregistré pour ne pas être regénérés lors d'une ré-execution du code                           |  

---

## **Installation**  
### **Pré-requis**  
- Python 3.8+  
- Git (facultatif si téléchargement manuel)  
- LaTeX (si utilisation de modèles .tex)  
- Bibliothèques Python (voir *requirements.txt*)  

### **Étapes d'installation**  
1. **Cloner le projet**  
   ```bash  
   git clone https://github.com/username/AutoCVFetcher.git  
   cd CVDownloader  
   ```  
2. **Créer un environnement virtuel**  
   ```bash  
   python -m venv env  
   source env/bin/activate  # Windows: .\env\Scripts\activate  
   ```  
3. **Installer les dépendances**  
   ```bash  
   pip install -r requirements.txt  
   ```  

---

## **Utilisation**  
1. **Configurer les données d'entrée**  
   - Ajoute les données JSON des offres d'emploi dans le dossier `input/`.  
   - Vérifie que les modèles de CV sont disponibles dans le dossier `templates/`.  

2. **Exécuter le script principal**  
   ```bash  
   python main.py  
   ```  

3. **Téléchargement des CV**  
   - Les CV seront sauvegardés dans des sous-dossiers organisés par entreprise.  
   - Le script vérifiera les doublons et les sautera automatiquement.  

---

## **Exemples d'exécution**  
### **Cas d'une offre JSON**  
```json  
{  
    "offer_id": "12345",  
    "company_name": "OpenAI",  
    "job_title": "Data Scientist",  
    "location": "Paris",  
    "description": "Analyse et modélisation de données pour des projets stratégiques."  
}  
```  
Commande :  
```bash  
python main.py --input input/job_offers.json  
```  

### **Sortie attendue**  
Le fichier `Data_Scientist_OpenAI.pdf` sera généré dans :  
```  
output/OpenAI/  
```

---

## **Dépendances principales**  
- **os** : Gestion des fichiers et répertoires.  
- **json** : Lecture et traitement des fichiers JSON.  
- **subprocess** : Appel à des processus externes (LaTeX).  
- **requests** : Interactions avec les API externes.  

---

## **Auteurs et contributeurs**  
Créé par **Lucas Mery**.  

Contributions, suggestions et retours sont les bienvenus ! 😊  
Contact : [email@example.com](mailto:email@example.com)  

---

Ajoute ce fichier en tant que `README.md` dans ton projet. Si tu veux y inclure plus de détails ou des exemples spécifiques, n'hésite pas à me le demander ! 🚀
