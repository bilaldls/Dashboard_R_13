#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd

# URL du site contenant le graphique
url = "https://fred.stlouisfed.org/series/NYSTHPI"  # Remplacez par l'URL réelle

# Envoi d'une requête GET pour récupérer la page
response = requests.get(url)
if response.status_code != 200:
    print("Erreur lors de la récupération de la page, code:", response.status_code)
    exit(1)

# Analyse du contenu HTML avec BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

chart_div = soup.find("div", {"id": "fred-chart"})
if chart_div:
    print("Graphique trouvé dans la balise avec id 'fred-chart'")
else:
    print("Graphique non trouvé sous 'fred-chart'. Essayez avec un autre identifiant, par exemple 'interactive-chart'.")

# Recherche du bloc <script> susceptible de contenir les données du graphique
# Ici, l'exemple cherche une variable JavaScript nommée "chartData"
script_data = None
for script in soup.find_all("script"):
    # Vérifier que le contenu du script est accessible et qu'il contient la chaîne recherchée
    if script.string and "FredGraph" in script.string:
        script_data = script.string
        break

if script_data is None:
    print("Aucune donnée de graphique trouvée dans les scripts de la page.")
    exit(1)

# Utilisation d'une expression régulière pour extraire le JSON
# Dans cet exemple, on suppose que les données sont définies de cette manière :
# var chartData = { ... };
pattern = re.compile(r"var\s+chartData\s*=\s*(\{.*?\});", re.DOTALL)
match = pattern.search(script_data)
if not match:
    print("Impossible d'extraire les données du graphique à l'aide de l'expression régulière.")
    exit(1)

json_text = match.group(1)

# Chargement des données JSON
try:
    data = json.loads(json_text)
except json.JSONDecodeError as e:
    print("Erreur lors du décodage des données JSON :", e)
    exit(1)

# Affichage du contenu complet des données (pour inspection)
print("Données extraites :", data)

# Supposons que les données du graphique soient stockées dans une clé nommée "data"
if "data" in data:
    df = pd.DataFrame(data["data"])
    print("Aperçu des données sous forme de DataFrame :")
    print(df.head())
    
    # Sauvegarde dans un fichier CSV pour exploitation ultérieure
    df.to_csv("graph_NY.csv", index=False)
    print("Les données du graphique ont été sauvegardées dans 'graph_NY.csv'")
else:
    print("La structure des données ne correspond pas à l'attendu ('data' introuvable).")