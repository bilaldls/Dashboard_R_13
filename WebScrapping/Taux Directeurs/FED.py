from fredapi import Fred
import pandas as pd
import matplotlib.pyplot as plt

# Remplace par ta propre clé API FRED
api_key = "7e359722e2bf36cce439f22cfe797ff5"
fred = Fred(api_key=api_key)

# Récupération des taux directeurs de la FED depuis 1995
data = fred.get_series('FEDFUNDS', observation_start='1995-01-01')

# Mise en forme dans un DataFrame
df = pd.DataFrame(data, columns=["FED Funds Rate"])
df.index.name = "Date"

# Enregistrement en fichier CSV
csv_filename = "fed_funds_rate.csv"
df.to_csv(csv_filename, sep=";")
print(f"Données sauvegardées dans le fichier : {csv_filename}")

# Tracer l'évolution du taux directeur
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["FED Funds Rate"], color="blue")
plt.title("Taux directeur de la FED (Federal Funds Rate) depuis 1995")
plt.xlabel("Année")
plt.ylabel("Taux (%)")
plt.grid(True)
plt.show()
