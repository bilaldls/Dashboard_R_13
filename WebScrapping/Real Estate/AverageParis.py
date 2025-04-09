#!/usr/bin/env python
# -*- coding: utf-8 -*-

import camelot
import pandas as pd
import re

def nettoyer_prix(texte):
    """
    Convertit une chaîne représentant un prix (ex : "11 300 €")
    en nombre flottant. Supprime le symbole euro, les espaces et
    remplace la virgule par le point si nécessaire.
    """
    # On supprime le symbole euro et les espaces
    texte = texte.replace("€", "").strip()
    texte = texte.replace(" ", "")
    texte = texte.replace(",", ".")
    try:
        return float(texte)
    except ValueError:
        return None

# Extraction des tableaux du PDF (toutes les pages)
# Le paramètre flavor peut être "stream" ou "lattice" selon le PDF.
tables = camelot.read_pdf("HistoriquedesprixaumappartementsanciensParispararrdt.pdf",
                           pages="all",
                           flavor="stream")

# Concaténation de tous les tableaux extraits en un seul DataFrame
dfs = [table.df for table in tables]
data = pd.concat(dfs, ignore_index=True)

print(dfs[0].head())


# Prépare la liste qui contiendra le trimestre et sa moyenne de prix
resultats = []

# Parcours de chaque ligne du DataFrame fusionné
for index, row in data.iterrows():
    premiere_cellule = row[0].strip()
    # On cherche les lignes commençant par "T" suivi d'un chiffre (T1 à T4) et d'une année
    if re.match(r'^T[1-4]\s+\d{4}$', premiere_cellule):
        trimestre = premiere_cellule
        prix_liste = []
        # Parcours des autres colonnes (qui devraient contenir les prix)
        for cell in row[1:]:
            if isinstance(cell, str) and cell.strip() != "":
                prix_val = nettoyer_prix(cell)
                if prix_val is not None:
                    prix_liste.append(prix_val)
        if prix_liste:
            moyenne = sum(prix_liste) / len(prix_liste)
            resultats.append({"Trimestre": trimestre, "Prix_moyen": moyenne})

# Création du DataFrame avec les résultats
df_resultats = pd.DataFrame(resultats)

# Sauvegarde dans un fichier CSV (séparateur point-virgule)
df_resultats.to_csv("moyenne_prix_par_trimestre.csv", index=False, sep=";")

print("Fichier CSV généré avec succès: moyenne_prix_par_trimestre.csv")
