
library(shiny)

# Charger l'interface utilisateur et la logique serveur
source("ui.R")
source("server.R")


# Lancer l'application
shinyApp(ui = ui, server = server)
