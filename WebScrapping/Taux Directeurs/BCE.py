from fredapi import Fred
import pandas as pd
import matplotlib.pyplot as plt

# Remplacez 'VOTRE_CLE_API' par votre clé API FRED personnelle
api_key = "7e359722e2bf36cce439f22cfe797ff5"
fred = Fred(api_key=api_key)

# Code FRED pour le taux des opérations principales de refinancement de la BCE

data = fred.get_series('ECBMRRFR', observation_start='1999-01-01')

# Conversion en DataFrame
df = pd.DataFrame(data, columns=["Taux des opérations principales de refinancement"])
df.index.name = "Date"

# Enregistrement dans un fichier CSV
csv_filename = "taux_refinancement_bce.csv"
df.to_csv(csv_filename, sep=";")
print(f"Données sauvegardées dans le fichier : {csv_filename}")

# Tracé du graphique
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["Taux des opérations principales de refinancement"], color="blue")
plt.title("Taux des opérations principales de refinancement de la BCE depuis 1999")
plt.xlabel("Année")
plt.ylabel("Taux (%)")
plt.grid(True)
plt.show()
