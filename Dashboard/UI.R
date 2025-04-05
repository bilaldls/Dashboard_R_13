library(shiny)

# Définir l'interface utilisateur
ui <- fluidPage(
  titlePanel("Dashboard des Prix des Matières Premières"),
  
  sidebarLayout(
    sidebarPanel(
      selectInput("choix", "Sélectionner un actif :", 
                  choices = c("Or", "Pétrole"), selected = "Or")
    ),
    
    mainPanel(
      plotOutput("plotPrix"),        # Graphique des prix
      plotOutput("plotVolatilite")   # Graphique de la volatilité annuelle
    )
  )
)


