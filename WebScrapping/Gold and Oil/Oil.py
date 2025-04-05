import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

# Définition du ticker du pétrole brut WTI sur Yahoo Finance
ticker = "CL=F"

# Récupération des données historiques
oil_data = yf.Ticker(ticker)
df = oil_data.history(period="10950d")  # Récupérer les données sur 30 ans
df.index = df.index.tz_localize(None)  # Supprimer la timezone pour éviter les erreurs Excel

# Vérifier si les données existent
if df.empty:
    print("Aucune donnée trouvée.")
else:
    # Appliquer la condition : si le prix est inférieur à 20$, remplacer par 20$
    df['Close'] = df['Close'].apply(lambda x: max(x, 20))
    # Calcul des rendements journaliers
    df['Daily Return'] = df['Close'].pct_change()

    # Extraire l'année de chaque ligne
    df['Year'] = df.index.year

    # Calcul de la volatilité pour chaque année (écart-type des rendements journaliers * sqrt(252))
    annual_volatility = df.groupby('Year')['Daily Return'].std() * np.sqrt(252)

    # Ajouter la volatilité annuelle dans une nouvelle colonne pour chaque ligne
    df['Annual Volatility'] = df['Year'].map(annual_volatility)

    # Convertir les valeurs en entier pour la colonne Close (optionnel)
    df['Close'] = df['Close'].apply(lambda x: int(x))

    # Enregistrement dans un fichier CSV
    csv_filename = "oil_prices.csv"
    df.to_csv(csv_filename, index=True, sep=";")
    print(f"Données enregistrées dans {csv_filename}")

    # Tracer le graphique des prix du pétrole
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Close"], color="blue", linestyle="-", marker="o", markersize=3, label="Prix du pétrole (USD)")

    # Ajouter les labels et le titre
    plt.xlabel("Date")
    plt.ylabel("Prix ($)")
    plt.title("Évolution du prix du pétrole sur 10950 jours")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    # Affichage du graphique des prix
    plt.show()

    # Tracer la volatilité annuelle
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Annual Volatility"], color="red", linestyle="-", label="Volatilité Annuelle")

    # Ajouter les labels et le titre pour la volatilité
    plt.xlabel("Date")
    plt.ylabel("Volatilité Annuelle")
    plt.title("Volatilité Annuelle du Pétrole sur 10950 jours")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    # Affichage du graphique de volatilité
    plt.show()
