import json
import subprocess
import os
import re

# Exemple de données de lettre de motivation
with open('resultats.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Créer le template LaTeX
template = r"""
\documentclass[9pt,a4paper]{extarticle}

\usepackage[a-1b]{pdfx}
\usepackage{accsupp}
\usepackage[margin=2cm]{geometry}
\usepackage[fixed]{fontawesome5}
\usepackage{ifxetex,ifluatex}
\usepackage{scrlfile}
\usepackage{xparse}

\newif\ifxetexorluatex
\ifxetex
  \xetexorluatextrue
\else
  \ifluatex
    \xetexorluatextrue
  \else
    \xetexorluatexfalse
  \fi
\fi

\newcommand{\cvItemMarker}{{\small\textbullet}}
\newcommand{\cvRatingMarker}{\faCircle}
\newcommand{\cvDateMarker}{\faCalendar[regular]}
\newcommand{\cvLocationMarker}{\faMapMarker}
\newcommand{\locationname}{Location}
\newcommand{\datename}{Date}

\newcommand{\cvtag}[1]{ \tikz[baseline]\node[anchor=base,draw=body!30,rounded corners,inner xsep=1ex,inner ysep =0.75ex,text height=1.5ex,text depth=.25ex]{#1};
}

\newcommand{\cvevent}[4]{
  {\large\color{emphasis}#1\par}
  \smallskip\normalsize
  \ifstrequal{#2}{}{}{
  \textbf{\color{accent}#2}\par
  \smallskip}
  \ifstrequal{#3}{}{}{
    {\small\makebox[0.5\linewidth][l]
      {\BeginAccSupp{method=pdfstringdef,ActualText={\datename:}}\cvDateMarker\EndAccSupp{}
      ~#3}
    }}
  \ifstrequal{#4}{}{}{
    {\small\makebox[0.5\linewidth][l]
      {\BeginAccSupp{method=pdfstringdef,ActualText={\locationname:}}\cvLocationMarker\EndAccSupp{}
        ~#4}
    }}\par
  \normalsize
}

\newcommand{\cvsectionfont}{\LARGE\bfseries}

\newcommand{\cvsection}[2][]{
  \nointerlineskip\bigskip
  \ifstrequal{#1}{}{}{\marginpar{\vspace*{\dimexpr1pt-\baselineskip}\raggedright\input{#1}}}
  {\color{heading}\cvsectionfont\MakeUppercase{#2}}\\[-1ex]
  {\color{headingrule}\rule{\linewidth}{2pt}\par}
}

\newcommand{\utffriendlydetokenize}[1]{
\scantokens{
  \catcode`\_=12
  \catcode`\&=12
  \catcode`\$=12
  \catcode`\#=12
  \catcode`\~=12
  {#1}
}
}

\newenvironment{fullwidth}{
  \begin{adjustwidth}{}{\dimexpr-\marginparwidth-\marginparsep\relax}}
  {\end{adjustwidth}}

\setlength{\parindent}{0pt}
\newcommand{\divider}{\textcolor{body!30}{\hdashrule{\linewidth}{0.62pt}{0.5ex}}}

\ifxetexorluatex
  \RequirePackage{fontspec}
\else
  \RequirePackage{cmap}
  \RequirePackage[utf8]{inputenc}
  \RequirePackage[T1]{fontenc}
  \input{glyphtounicode}
  \pdfglyphtounicode{f_f}{FB00}
  \pdfglyphtounicode{f_f_i}{FB03}
  \pdfglyphtounicode{f_f_l}{FB04}
  \pdfglyphtounicode{f_i}{FB01}
  \pdfgentounicode=1
\fi

\RequirePackage{tikz}
\RequirePackage[skins]{tcolorbox}
\RequirePackage[inline]{enumitem}
\setlist{leftmargin=*,labelsep=0.5em,nosep,itemsep=0.25\baselineskip,after=\vspace{0.25\baselineskip}}
\setlist[itemize]{label=\cvItemMarker}
\RequirePackage{graphicx}
\RequirePackage{trimclip}
\RequirePackage{dashrule}
\RequirePackage{multirow,tabularx}
\RequirePackage{changepage}

\thispagestyle{empty} 

\geometry{left=1cm,right=1cm,top=1cm,bottom=1cm,columnsep=0.75cm}

\usepackage{paracol}

\ifxetexorluatex
  \setmainfont{Roboto Slab}
  \setsansfont{Lato}
  \renewcommand{\familydefault}{\sfdefault}
\else
  \usepackage[rm]{roboto}
  \usepackage[defaultsans]{lato}
  \renewcommand{\familydefault}{\sfdefault}
\fi

\definecolor{SlateGrey}{HTML}{2E2E2E}
\definecolor{LightGrey}{HTML}{666666}
\definecolor{DarkPastelRed}{HTML}{450808}
\definecolor{PastelRed}{HTML}{8F0D0D}
\definecolor{GoldenEarth}{HTML}{E7D192}
\colorlet{name}{black}
\colorlet{tagline}{PastelRed}
\colorlet{heading}{DarkPastelRed}
\colorlet{headingrule}{GoldenEarth}
\colorlet{subheading}{PastelRed}
\colorlet{accent}{PastelRed}
\colorlet{emphasis}{SlateGrey}
\colorlet{body}{LightGrey}

\renewcommand{\cvsectionfont}{\LARGE\rmfamily\bfseries}
\renewcommand{\cvItemMarker}{{\small\textbullet}}
\renewcommand{\cvRatingMarker}{\faCircle}

\begin{document}

\hypersetup{hidelinks}

\begin{minipage}{0.62\linewidth}
    \raggedright
    {\Huge\rmfamily\bfseries{LUCAS MERY}\par}
    \smallskip
    {\large\bfseries\color{PastelRed}%(objet)s\par}
    \smallskip
    Titulaire d’un Master en mathématiques appliquées aux statistiques, je suis rigoureux, organisé et doté d’un esprit analytique. Passionné par le domaine de la data et des statistiques, je souhaite apporter mes compétences et connaissances à %(cv1)s.
\end{minipage}
\begin{minipage}{0.38\linewidth}
    \begin{center}
        \includegraphics[width=10em]{img_test/photoCV2.png}
    \end{center}
\end{minipage}


\columnratio{0.62}

\begin{paracol}{2}

\cvsection{EXPERIENCES PROFESSIONNELLES}

\cvevent{Datascientist/Statisticien}{\raisebox{-0.5em}{\includegraphics[width=3em]{img_test/giscope.PNG}} Groupement d’intérêt scientifique sur les cancers d’origine
professionnelle dans le vaucluse}{Avril - Sept 2024}{Avignon}
\begin{itemize}
\item Nettoyage et analyse rétrospective d'une base de données
\item Analyse des parcours professionnels de patients atteints de cancer hématologique et ayant travaillé dans l'agriculture ou des activités de nettoyage : statistiques descriptives, modèles de durées et analyses de séquence de ces parcours.
\end{itemize}

\divider

\cvevent{Data Analyst}{\raisebox{-0.35em}{\includegraphics[width=3.5em]{img_test/lsce.PNG}} Laboratoire des sciences du climat et de l’environnement}{Avril - Juin 2023}{Université Paris-Saclay}
\begin{itemize}
\item Étude de variables (permitivité diéléctrique...) liées à la saturation en eau du sol.
\item Recherche d’une correction en température afin de gagner en précision sur le modèle prédictif d’inondations (régression linéaire et quadratique...).
\item Utilisation de Bash sous Ubuntu
\end{itemize}

\divider

\cvevent{Stage de L3}{\raisebox{-0.3em}{\includegraphics[width=1.7em]{img_test/cea.PNG}} Commissariat à l’énergie atomique de Marcoule}{Mai - Juin 2022}{Marcoule}
\begin{itemize}
\item Réalisation d’un sondage sur l’utilisation des mathématiques au sein du CEA.
\item Mise en place d’un algorithme de reconnaissance textuelle pour les consultants en gestion.
\end{itemize}

\divider

\cvevent{Préparateur de commande}{\raisebox{-0.5em}{\includegraphics[width=1.3em]{img_test/CMS.PNG}} Société CM Solutions}{Depuis 2017, périodes de 1-2 mois}{Miribel 01700}

\cvsection{Formation}

\cvevent{Master de mathématiques appliquées statistiques mention AB}{\raisebox{-0.4em}{\includegraphics[width=1.5em]{img_test/amu.PNG}} Université d’Aix Marseille}{2022 - 2024}{}
\begin{itemize}
\item Statistiques exploratoires, données catégorielles, test statistiques (chi-2, anova, corrélation), modèles de durée, algorithmes de machine learning : ACP/K-means, CAH, régressions ANOVA/ANCOVA...
\item Logiciels et langages informatiques divers
\end{itemize}

\divider

\cvevent{L3 mathématiques générales et applications}{\raisebox{-0.6em}{\includegraphics[width=1.4em]{img_test/avi.PNG}} Université d’Avignon}{2020 - 2022}{}

\divider

\cvevent{Classes préparatoires aux grandes écoles MPSI-MP}{\raisebox{-0.5em}{\includegraphics[width=2.7em]{img_test/alzon.PNG}} Lycée Emmanuel d’Alzon - Nîmes}{2018 - 2020}{}

\switchcolumn

\cvsection{Informations personnelles}

\textcolor{PastelRed}{\faBirthdayCake}25/10/2000 (24 ans)

\textcolor{PastelRed}{\faCar}Permis B et véhicule personnel

\href{mailto:lucas.mery30@outlook.fr}{\textcolor{PastelRed}{\faAt}lucas.mery30@outlook.fr}

\href{tel:+33769881891}{\textcolor{PastelRed}{\faPhone}+33 7 69 88 18 91}

\textcolor{PastelRed}{\faMapMarker}2 rue Parmentier, 91120 Palaiseau, France 

\href{https://www.linkedin.com/in/lucas-mery-58256a257}{\textcolor{PastelRed}{\faLinkedin}Mon LinkedIn : linkedin.com/in/lucas-mery-58256a257}

\href{https://github.com/LucasMery00}{\textcolor{PastelRed}{\faGithub}Mon GitHub : github.com/LucasMery00}

\cvsection{Logiciels et langages de programmation}

\cvtag{R}\raisebox{-0.3ex}{\includegraphics[width=1.5em]{img_test/Rstud.PNG}}
\cvtag{Python}\raisebox{-0.6ex}{\includegraphics[width=1.3em]{img_test/python.PNG}}
\cvtag{SQL}\raisebox{-0.2ex}{\includegraphics[width=2em]{img_test/sql.PNG}}
\cvtag{SAS}\raisebox{-0.2ex}{\includegraphics[width=2.2em]{img_test/sas.PNG}}

\cvtag{QGIS}\includegraphics[width=2.4em]{img_test/qgis.PNG}
\cvtag{\LaTeX}\raisebox{-0.6ex}{\includegraphics[width=1.5em]{img_test/tex.PNG}}
\cvtag{Office 365}\raisebox{-0.6ex}{\includegraphics[width=1.5em]{img_test/365.PNG}}

\cvsection{Langues}

\includegraphics[width=2em]{img_test/anglais.PNG} \raisebox{0.3em}{\parbox[t]{12em}{\textbf{Anglais} : niveau C1 certifié par LanguageCert (87/100)}}

\medskip

\includegraphics[width=2em]{img_test/all.PNG} \raisebox{0.3em}{\textbf{Allemand} : débutant}

\cvsection{Compétences}

\begin{itemize}
    \item[\faThumbsUp] Compétences rédactionnelles en français avec différents outils textuels (\LaTeX, Word)
    \item[\faThumbsUp] Maitrise d’outils mathématiques (ACP, régressions, tests statistiques...)
    \item[\faThumbsUp] Maitrise de logiciels et de langages variés (R, LateX, Python, SQL, QGIS...)
    \item[\faThumbsUp] Data visualisation sur R
    \item[\faThumbsUp] Web scrapping  via APIs sur Python
\end{itemize}

\cvsection{QUALITÉS}

\begin{itemize}
    \item[\faPlus] Capacité à analyser un problème et à établir une méthodologie pour le résoudre
    \item[\faPlus] Dynamique, rigoureux, autonome et organisé
    \item[\faPlus] Travail en équipe
    \item[\faPlus] Esprit de synthèse et adaptabilité
\end{itemize}

\cvsection{CENTRES D'INTÉRÊT}

\begin{itemize}
    \item[\faMountain] Pratique de plusieurs sports de montagne : escalade, ski, randonnée, alpinisme, parapente\medskip
    \item[\faCloudSunRain] Énergie, Climat et Environnement (livres de J-M-Jancovici, Phillipe Bihouix..., conférences en ligne...)\medskip
    \item[\faCalculator] Vulgarisations et Actus Scientifique, vidéos en ligne, conférences, médias.
\end{itemize}

\end{paracol}

\cvsection{PROJETS RÉALISÉS}

\begin{itemize}
    \item[\faFolderOpen] Développement d’un système automatisé sur Python qui combine le web scraping pour extraire des données, l’API OpenAI pour générer du contenu pertinent, et LaTeX pour une mise en forme professionnelle des documents.
    \item[\faSearchPlus ] Travaux encadrés de recherche, rapport rendu à FEDOSOLI sur la clientèle en ostéopathie : Création et diffusion d'un questionnaire auprès d'un panel pour affiner le ciblage des patients, data visualisation sur les résultats du sondage
\end{itemize}

\end{document}
"""

# Répertoire de sortie pour les PDF
output_dir = r"C:\Users\lucas\OneDrive\Bureau\test\lm_cv"
os.makedirs(output_dir, exist_ok=True)

# Compter le nombre de fichiers PDF existants pour définir le numéro de départ
pdf_count = len([f for f in os.listdir(output_dir) if f.endswith('cv.pdf')])

# Générer le document pour chaque lettre
for idx, item in enumerate(data, start=pdf_count + 1):
    # Remplacer les variables par les données réelles
    latex_code = template % item
    
    # Créer un nom de fichier unique avec le numéro séquentiel
    safe_title = re.sub(r'\W+', '_', item['url'].split('/')[-1])  # Limiter à 30 caractères pour la sécurité
    tex_filename = f"{idx}_{safe_title}_cv.tex"
    pdf_filename = f"{idx}_{safe_title}_cv.pdf"
    
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
        aux_file = f'{idx}_{safe_title}_cv.{ext}'
        if os.path.exists(aux_file):
            os.remove(aux_file)
    
xmpi_filename = f'pdfa.xmpi'
if os.path.exists(xmpi_filename):
    os.remove(xmpi_filename)