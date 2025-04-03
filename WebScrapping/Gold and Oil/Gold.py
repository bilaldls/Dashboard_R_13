import yfinance as yf
import matplotlib.pyplot as plt


# Définition du ticker de l’or sur Yahoo Finance
ticker = "GC=F"

# Récupération des données historiques
gold_data = yf.Ticker(ticker)
df = gold_data.history(period="1000d")  # Récupérer les données sur 1000 jours
df.index = df.index.tz_localize(None)
# Vérifier si les données existent
if df.empty:
    print(" Aucune donnée trouvée.")
else:

    df['Close'] = df['Close'].apply(lambda x: int(x))  # Convertir les valeurs en entier
    # Enregistrement dans un fichier Excel
    csv_filename = "gold_prices.csv"
    df.to_csv(csv_filename, index=True, sep=";")
    print(f"Données enregistrées dans {csv_filename}")

    # Tracer le graphique des prix
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Close"], color="blue", linestyle="-", marker="o", markersize=3, label="Prix de l'or (USD)")

    # Ajout des labels et titre
    plt.xlabel("Date")
    plt.ylabel("Prix ($)")
    plt.title("Évolution du prix de l'or sur 1000 jours")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    # Affichage du graphique
    plt.show()
