library(shiny)
# Définir l'interface utilisateur
ui <- navbarPage("Dashboard des Prix des Matières Premières",
                 # Onglet 1 : Prix & Volatilité
                 tabPanel("Prix & Volatilité",
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
                 ),
                 
                 # Onglet 2 : Taux de la FED
                 tabPanel("Taux de la FED",
                          mainPanel(
                            plotOutput("plotFedRate")       # Nouveau graphique à afficher
                          )
                 )
)


