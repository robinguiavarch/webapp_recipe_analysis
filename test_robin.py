class TestRobin:
    def __init__(self):
        self.message = "Test ajout de fichier Robin"
    
    def afficher_message(self):
        print(self.message)

# Instanciation de la classe et appel de la méthode
test = TestRobin()          # Création de l'objet test
test.afficher_message()      # Appel de la méthode pour afficher le message