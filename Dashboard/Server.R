# server.R
library(shiny)
library(ggplot2)
library(readr)
library(dplyr)

# Charger les données
gold_data <- read_csv2("data/gold_prices.csv")
oil_data <- read_csv2("data/oil_prices.csv")
fed_data <- read_csv2("data/fed_funds_rate.csv")  # Assure-toi que ce fichier existe et est bien formaté


# Convertir en numérique si nécessaire
fed_data$`FED Funds Rate` <- as.numeric(gsub(",", ".", fed_data$`FED Funds Rate`))


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
      theme(axis.text.x = element_text(angle = 45, hjust = 1))  # Améliore lisibilité des années
  })
  
  # Créer le graphique des taux de la FED avec des points et une ligne
  output$plotFedRate <- renderPlot({
    ggplot(fed_data, aes(x = as.Date(Date), y = `FED Funds Rate`)) +
      geom_line(color = "gray70") +  # Ligne fine entre les points
      geom_point(color = "darkgreen", size = 2) +  # Points verts
      scale_y_continuous(breaks = seq(0, ceiling(max(fed_data$`FED Funds Rate`, na.rm = TRUE)), by = 1)) +  # Graduations de 1 en 1
      labs(title = "Taux directeur de la FED (Federal Funds Rate)",
           x = "Date", y = "Taux (%)") +
      theme_minimal()
  })
  
  
}
