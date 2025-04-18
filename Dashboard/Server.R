# server.R
library(shiny)
library(ggplot2)
library(readr)
library(dplyr)

# Charger les données
gold_data <- read_csv2("data/gold_prices.csv")
oil_data <- read_csv2("data/oil_prices.csv")
fed_data <- read_csv2("data/fed_funds_rate.csv")
bce_data <- read.csv2("data/taux_refinancement_bce.csv")

# Convertir en numérique si nécessaire
fed_data$`FED Funds Rate` <- as.numeric(gsub(",", ".", fed_data$`FED Funds Rate`))
bce_data$Taux <- as.numeric(gsub(",", ".", bce_data$Taux))

# Conversion explicite de la colonne Annual Volatility en numérique
gold_data$`Annual Volatility` <- as.numeric(gsub(",", ".", gold_data$`Annual Volatility`))
oil_data$`Annual Volatility` <- as.numeric(gsub(",", ".", oil_data$`Annual Volatility`))


# Définir la logique du serveur
server <- function(input, output) {
  
  # Fonction réactive pour choisir les bonnes données en fonction de la sélection
  donnees_reactives <- reactive({
    if (input$choix == "Or") {
      gold_data
    } else {
      oil_data
    }
  })
  
  # Fonction réactive pour le choix des taux : FED ou BCE
  taux_reactif <- reactive({
    if (input$taux_choisi == "FED") {
      fed_data %>%
        mutate(Taux = `FED Funds Rate`, Banque = "FED") %>%
        select(Date, Taux, Banque)
    } else {
      bce_data %>%
        mutate(Banque = "BCE") %>%
        select(Date, Taux, Banque)
    }
  })
  
  # Créer le graphique
  output$plotPrix <- renderPlot({
    ggplot(donnees_reactives(), aes(x = Date, y = Close)) +
      geom_line(color = "blue") +
      labs(title = paste("Évolution du prix du", input$choix),
           x = "Date", y = "Prix (USD)") +
      theme_minimal()
  })
  
  # Créer l'histogramme de la volatilité annuelle
  output$plotVolatilite <- renderPlot({
    donnees_agregees <- donnees_reactives() %>%
      dplyr::mutate(Year = as.numeric(format(Date, "%Y"))) %>%
      dplyr::group_by(Year) %>%
      dplyr::summarise(VolatiliteAnnuelle = mean(`Annual Volatility`, na.rm = TRUE))
    
    ggplot(donnees_agregees, aes(x = factor(Year), y = VolatiliteAnnuelle)) +
      geom_col(fill = "red") +
      labs(title = paste("Volatilité annuelle du", input$choix),
           x = "Année", y = "Volatilité Annuelle") +
      theme_minimal() +
      theme(axis.text.x = element_text(angle = 45, hjust = 1))
  })
  
  # Créer le graphique des taux (FED ou BCE) dynamiquement
  output$plotFedRate <- renderPlot({
    data <- taux_reactif()
    
    ggplot(data, aes(x = as.Date(Date), y = Taux)) +
      geom_line(color = "gray70") +
      geom_point(color = "darkgreen", size = 2) +
      scale_y_continuous(breaks = seq(0, ceiling(max(data$Taux, na.rm = TRUE)), by = 1)) +
      labs(title = paste("Taux directeur -", unique(data$Banque)),
           x = "Date", y = "Taux (%)") +
      theme_minimal()
  })
}
