import json
import subprocess
import os
import re

# Exemple de données de lettre de motivation
with open('resultats.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Créer le template LaTeX
template = r"""
\documentclass[11pt,a4paper,roman]{moderncv}   
\usepackage[rm]{roboto}
\usepackage[defaultsans]{lato}

\usepackage[french]{babel}
\usepackage[T1]{fontenc}
\moderncvstyle{classic}
\moderncvcolor{black}                          
\usepackage[utf8]{inputenc}
\usepackage[scale=0.80]{geometry}
\name{Lucas MERY}{}
\email{lucas.mery30@outlook.fr}
\phone[mobile]{+33 7 69 88 18 91}
\address{2 rue Parmentier, 91120 Palaiseau, France}
\begin{document}
\recipient{Destinataires :}{%(destinataire)s}
\date{\today}
\opening{\textbf{Objet : %(objet)s}}
\makelettertitle

%(contenue_lettre)s

\textbf{Lucas Mery}
\end{document}
"""

# Répertoire de sortie pour les PDF
output_dir = r"C:\Users\lucas\OneDrive\Bureau\test\lm_cv"
os.makedirs(output_dir, exist_ok=True)

# Compter le nombre de fichiers PDF existants pour définir le numéro de départ
pdf_count = len([f for f in os.listdir(output_dir) if f.endswith('lm.pdf')])

# Générer le document pour chaque lettre
for idx, item in enumerate(data, start=pdf_count + 1):
    # Remplacer les variables par les données réelles
    latex_code = template % item
    
    # Créer un nom de fichier unique avec le numéro séquentiel
    safe_title = re.sub(r'\W+', '_', item['url'].split('/')[-1]) # Limiter à 30 caractères pour la sécurité
    tex_filename = f"{idx}_{safe_title}_lm.tex"
    pdf_filename = f"{idx}_{safe_title}_lm.pdf"
    
    # Écrire le code LaTeX dans un fichier
    with open(tex_filename, "w", encoding="utf-8") as f:
        f.write(latex_code)
    
    # Compiler le fichier .tex en PDF
    subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_filename])
    
    # Déplacer le fichier PDF vers le dossier de sortie
    if os.path.exists(pdf_filename):
        os.rename(pdf_filename, os.path.join(output_dir, pdf_filename))
    
    # Supprimer les fichiers générés qui ne sont pas des PDF
    for ext in ['tex', 'aux', 'log', 'out']:
        aux_file = f'{idx}_{safe_title}_lm.{ext}'
        if os.path.exists(aux_file):
            os.remove(aux_file)

print("Génération de lettres de motivation terminée.")


