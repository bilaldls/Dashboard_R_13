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
                 
                 tabPanel("Taux banques centrales",
                          sidebarLayout(
                            sidebarPanel(
                              selectInput("taux_choisi", "Choisir la banque centrale :", 
                                          choices = c("FED", "BCE"), selected = "FED")
                            ),
                            mainPanel(
                              plotOutput("plotFedRate")  # <- C'est ça qui manquait
                            )
                          )
                 )
)


