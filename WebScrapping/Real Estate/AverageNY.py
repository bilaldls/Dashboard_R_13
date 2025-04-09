#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import re

def nettoyer_prix(texte):
    """
    Convertit une chaîne représentant un prix (ex : "11 300 €")
    en nombre flottant.
    """
    if isinstance(texte, str):
        texte = texte.replace("€", "").strip()
        texte = texte.replace(" ", "")
        texte = texte.replace(",", ".")
        try:
            return float(texte)
        except ValueError:
            return None
    return texte

# Charger le CSV de New York.
# On suppose que le CSV contient au moins deux colonnes :
#   - "date" au format "YYYY-MM-DD"
#   - "prix" qui contient le prix du mois correspondant (ex : "3000 €")
df = pd.read_csv("NY.csv", delimiter=",", encoding="utf-8")

# Convertir la colonne "date" en datetime.
df["date"] = pd.to_datetime(df["observation_date"], format="%Y-%m-%d")

# Nettoyer la colonne "prix" (si nécessaire)
df["prix"] = df["NYXRSA"].apply(nettoyer_prix)

# Créer une colonne indiquant le trimestre sous le format "Tn AAAA"
df["Trimestre"] = df["date"].apply(lambda d: f"T{d.quarter} {d.year}")

# Grouper par trimestre et calculer la moyenne des prix
ny_trimestre = df.groupby("Trimestre")["prix"].mean().reset_index()

# Renommer la colonne pour clarifier qu'il s'agit des moyennes pour NY
ny_trimestre = ny_trimestre.rename(columns={"prix": "Prix_moyen_NY"})

# Sauvegarder le résultat dans un nouveau CSV
ny_trimestre.to_csv("NY_moyenne_prix.csv", index=False, sep=";")
print("Fichier 'NY_moyenne_prix.csv' généré avec succès.")
