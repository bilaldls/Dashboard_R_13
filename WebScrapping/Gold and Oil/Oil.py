import yfinance as yf
import matplotlib.pyplot as plt

# Définition du ticker du pétrole brut WTI sur Yahoo Finance
ticker = "CL=F"

# Récupération des données historiques
oil_data = yf.Ticker(ticker)
df = oil_data.history(period="1000d")  # Récupérer les données sur 1000 jours
df.index = df.index.tz_localize(None)  # Supprimer la timezone pour éviter les erreurs Excel

# Vérifier si les données existent
if df.empty:
    print("Aucune donnée trouvée.")
else:
    # Enregistrement dans un fichier CSV
    csv_filename = "oil_prices.csv"
    df.to_csv(csv_filename, index=True, sep=";")
    print(f"Données enregistrées dans {csv_filename}")

    # Tracer le graphique des prix du pétrole
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Close"], color="blue", linestyle="-", marker="o", markersize=3, label="Prix du pétrole (USD)")

    # Ajout des labels et titre
    plt.xlabel("Date")
    plt.ylabel("Prix ($)")
    plt.title("Évolution du prix du pétrole sur 1000 jours")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    # Affichage du graphique
    plt.show()

