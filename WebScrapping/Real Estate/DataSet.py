import pandas as pd
import re


# Lecture du CSV de Paris obtenu précédemment.
paris_df = pd.read_csv("moyenne_prix_par_trimestre.csv", delimiter=";", encoding="utf-8")

#Lecture du CSV de NY
ny_df = pd.read_csv("NY_moyenne_prix.csv")

# On fusionne les données sur la colonne "Trimestre".
# La jointure "outer" permet de conserver tous les trimestres présents dans l’un ou l’autre fichier.
merged = pd.merge(paris_df, ny_df, on="Trimestre", how="outer")

# Pour trier chronologiquement, nous allons extraire l'année et le numéro du trimestre.
def extraire_info(trimestre):
    """
    Extrait l'année et le numéro du trimestre depuis une chaîne du type "T3 2024".
    Renvoie un tuple (année, trimestre) permettant le tri.
    """
    match = re.match(r'^T([1-4])\s+(\d{4})$', str(trimestre).strip())
    if match:
        # Renvoie (année, numéro_du_trimestre)
        return int(match.group(2)), int(match.group(1))
    else:
        return None, None

# Créer deux colonnes d'aide pour le tri
merged["Annee"], merged["Trimestre_num"] = zip(*merged["Trimestre"].apply(extraire_info))

# Trier par année puis par trimestre
merged = merged.sort_values(by=["Annee", "Trimestre_num"], ascending=[True, True])

# Optionnel : on peut retirer les colonnes d'aide après le tri
merged = merged.drop(columns=["Annee", "Trimestre_num"])

# Exporter le fichier fusionné dans un CSV final
merged.to_csv("merged_paris_ny.csv", index=False, sep=";")
print("Fichier merged_paris_ny.csv généré avec succès.")
