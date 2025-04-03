# server.R
library(shiny)
library(ggplot2)
library(readr)

# Charger les données
gold_data <- read_csv2("data/gold_prices.csv")
oil_data <- read_csv2("data/oil_prices.csv")


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
}
