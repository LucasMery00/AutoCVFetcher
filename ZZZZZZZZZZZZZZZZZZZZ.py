import json
from openai import OpenAI

client = OpenAI(api_key="mettre_api_key_ici")

# Chargez les données à partir du fichier JSON
with open('test_offres.json', 'r', encoding='utf-8') as f:
    offres = json.load(f)

# Liste pour stocker les résultats
resultats = []

# Modèle de prompt
prompt_template = """
Mon profil :
Je suis jeune diplomé d'un Master en mathématiques appliquées et statistiques, je cherche un emploi dans
la data ou les statistiques (data analyst/scientist, chargé d'étude...), j'ai effectué un stage au 
Groupement d’intérêt scientifique sur les cancers d’origine professionnelle dans le vaucluse et un autre
au Laboratoire des sciences du climat et de l’environnement dans lesquels j'ai gagné en experiences.
J'ai acquis au cours de mon parcours des compétences solides en R, SQL, et Python ainsi qu’en modélisation
statistique et machine learning.
Mes qualités sont :
+ Capacité à analyser un problème et à établir une méthodologie pour le résoudre
+ Dynamique, rigoureux, autonome et organisé
+ Travail en équipe
+ Esprit de synthèse et adaptabilité
Mes compétences sont :
+ Compétences rédactionnelles en français avec différents outils textuels (LATEX, Word)
+ Maitrise d’outils mathématiques (ACP, régressions, tests statistiques...)
+ Maitrise de logiciels et de langages variés (R, LateX, Python, SQL, QGIS...)
+ Data visualisation
+ Web scrapping via APIs
Je t'envoie un fichier .json contenant plusieurs clés (informations sur des offres d'emplois). À partir de ces clés et de mon profil, tu dois rédiger une lettre de motivation pour cette offre.

La lettre devra mentionner les sujets suivants :
- la/les missions de l'offre adapté à mon profil
- dire que je suis titulaire d'un Master en math appli stat
- parler de certaines compétence et qualités adapté à l'offre

La lettre commence par : "Madame, Monsieur," et se termine par : 

"Je serais ravi de pouvoir échanger avec vous sur cette opportunité et sur la manière dont je pourrais contribuer à vos objectifs. Je vous remercie pour l’attention que vous porterez à ma candidature et reste à votre disposition pour toute information complémentaire.

Dans l’attente de votre réponse, je vous prie d’agréer, Madame, Monsieur, l’expression de mes salutations distinguées."

Sauter des lignes entre les paragraphes et respecter les consignes suivantes :
1. La lettre doit : contenir entre 1500 et 2000 caractères, être sans aucune fautes de français, avoir une rédaction parfaite et les phrases doivent avoir du sens et être logique, ne pas contenir des informations inventer sur mes compétences.
2. Rédiger au masculin (donc enlever les ·e et les H/F).
3. Éviter toute répétition et ne pas inclure d'éléments qui ne figurent pas dans l'offre ou mon profil.
4. Me donner le destinataire de cette lettre (Nom de l'entreprise et l'adresse ou la ville si possible) dans [destinataire]
5. Me donner l'objet de la lettre structuré ainsi : "Candidature au poste... au sein de ..." dans [objet].
6. Compléter la partie [cv1] (en se basant sur l'offre) pour cette phrase d'introduction CV : "Titulaire d’un Master en mathématiques appliquées aux statistiques, je suis rigoureux, organisé et doté d’un esprit analytique. Passionné par le domaine de la data et des statistiques, je souhaite apporter mes compétences et connaissances à [cv1]."

Réponds en JSON structuré comme suit (sans aucune répétition de clé et sans guillemets dans les contenus) :

{
    "url": "...",
    "contenue_lettre": "...",
    "cv1": "...",
    "objet": "...",
    "destinataire": "..."
}
"""

for offre in offres:
    prompt = prompt_template + f"\n\nVoici les détails de l'offre : {offre}"
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}]
    )

    # Récupérer la réponse et enlever les balises ```json et ```
    response_text = completion.choices[0].message.content.strip()
    if response_text.startswith("```json"):
        response_text = response_text[7:]  # Retire le ```json au début
    if response_text.endswith("```"):
        response_text = response_text[:-3]  # Retire le ``` à la fin
    
    # Vérifier si la réponse est vide
    if response_text:
        try:
            result_data = json.loads(response_text)  # Convertit en dictionnaire
            
            # Ajouter à la liste des résultats
            resultats.append(result_data)
        
        except json.JSONDecodeError as e:
            print(f"Erreur de conversion en JSON pour l'offre {offre['url']}: {e}")
            print("Réponse brute de l'API:", response_text)  # Affiche la réponse pour inspection
    else:
        print(f"Aucune réponse reçue pour l'offre {offre['url']}")



# Sauvegarder les résultats dans un fichier JSON
with open('resultats.json', 'w', encoding='utf-8') as f:
    json.dump(resultats, f, ensure_ascii=False, indent=4)



