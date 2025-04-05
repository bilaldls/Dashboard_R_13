import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

# Définition du ticker de l’or sur Yahoo Finance
ticker = "GC=F"

# Récupération des données historiques
gold_data = yf.Ticker(ticker)
df = gold_data.history(period="10950d")  # Récupérer les données sur 10950 jours
df.index = df.index.tz_localize(None)

# Vérifier si les données existent
if df.empty:
    print("Aucune donnée trouvée.")
else:
    df['Daily Return'] = df['Close'].pct_change()

    # Calcul de la volatilité pour chaque année
    df['Year'] = df.index.year  # Extraire l'année
    annual_volatility = df.groupby('Year')['Daily Return'].std() * np.sqrt(252)

    # Ajouter la volatilité annuelle dans une nouvelle colonne pour chaque ligne
    df['Annual Volatility'] = df['Year'].map(annual_volatility)

    # Convertir les valeurs en entier pour la colonne Close
    df['Close'] = df['Close'].apply(lambda x: int(x))

    # Enregistrement dans un fichier CSV
    csv_filename = "gold_prices.csv"
    df.to_csv(csv_filename, index=True, sep=";")
    print(f"Données enregistrées dans {csv_filename}")

    # Tracer le graphique des prix de l'or
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Close"], color="blue", linestyle="-", marker="o", markersize=3, label="Prix de l'or (USD)")

    # Ajouter les labels et le titre
    plt.xlabel("Date")
    plt.ylabel("Prix ($)")
    plt.title("Évolution du prix de l'or sur 10950 jours")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    # Affichage du graphique
    plt.show()

    # Tracer la volatilité annuelle
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Annual Volatility"], color="red", linestyle="-", label="Volatilité Annuelle")

    # Ajouter les labels et le titre pour la volatilité
    plt.xlabel("Date")
    plt.ylabel("Volatilité Annuelle")
    plt.title("Volatilité Annuelle de l'Or sur 10950 jours")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    # Affichage du graphique de volatilité
    plt.show()
