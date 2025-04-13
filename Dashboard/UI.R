library(shiny)

# Définir l'interface utilisateur
ui <- navbarPage("Dashboard Finance/Economie",
                 
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
                 
                 # Onglet 2 : Taux des banques centrales
                 tabPanel("Taux banques centrales",
                          sidebarLayout(
                            sidebarPanel(
                              selectInput("taux_choisi", "Choisir la banque centrale :", 
                                          choices = c("FED", "BCE"), selected = "FED")
                            ),
                            mainPanel(
                              plotOutput("plotFedRate")  # Graphique des taux
                            )
                          )
                 ),
                 
                 # Onglet 3 : Corrélation (avec 2 graphiques)
                 tabPanel("Corrélation Taux - Or",
                          sidebarLayout(
                            sidebarPanel(
                              helpText("Corrélation entre le taux directeur et le prix / la volatilité de l'or ou du pétrole")
                            ),
                            mainPanel(
                              plotOutput("plotScatterCorrelation", height = "400px"),  # Scatter + régression
                              plotOutput("plotBoxVolatilite", height = "400px"),       # Boxplot des volatilités
                              plotOutput("plotCrossCorrelation", height = "400px")
                            )
                          )
                 )
)

