import requests
from bs4 import BeautifulSoup
import pdfkit

# 1. Récupérer le contenu HTML de la page Web
url = 'https://www.cheminsdevie.info/emission/1-samuel-1-21-2-25/'  # Remplacez par l'URL de la page Web que vous souhaitez télécharger
response = requests.get(url)
html_content = response.content

# 2. Utiliser BeautifulSoup pour analyser le contenu HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 3. Facultatif : Effectuer des modifications sur le contenu HTML si nécessaire
# Par exemple, vous pouvez supprimer certains éléments indésirables ou effectuer des modifications de mise en page

# 4. Enregistrer le contenu HTML modifié dans un fichier temporaire
temp_html_file = 'temp.html'
with open(temp_html_file, 'w', encoding='utf-8') as file:
    file.write(str(soup))

# 5. Utiliser PDFKit pour convertir le fichier HTML en PDF
output_pdf = 'output.pdf'  # Nom du fichier PDF de sortie
pdfkit.from_file(temp_html_file, output_pdf)

# 6. Supprimer le fichier HTML temporaire
import os
os.remove(temp_html_file)

print('Téléchargement terminé. Le fichier PDF a été enregistré sous', output_pdf)
