import os
import subprocess

def compresser_pdf_ghostscript(input_path, output_path):
    command = [
        r"C:\Program Files\gs\gs10.04.0\bin\gswin64c.exe",  # Chemin complet vers gswin64c.exe
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/printer",  # Changez ce paramètre pour ajuster la qualité de compression
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]
    subprocess.run(command, check=True)

def compresser_et_remplacer_pdfs(dossier):
    for fichier in os.listdir(dossier):
        if fichier.endswith("cv.pdf"):
            chemin_fichier = os.path.join(dossier, fichier)
            chemin_temp = os.path.join(dossier, "compressed_" + fichier)
            
            # Compresser et sauvegarder temporairement
            compresser_pdf_ghostscript(chemin_fichier, chemin_temp)
            
            # Remplacer le fichier original par la version compressée
            os.replace(chemin_temp, chemin_fichier)
            print(f"{fichier} compressé et remplacé.")

# Utilisation
dossier_pdf = r"C:\Users\lucas\OneDrive\Bureau\test\lm_cv"
compresser_et_remplacer_pdfs(dossier_pdf)
