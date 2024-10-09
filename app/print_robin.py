class PrintRobin:
    def __init__(self):
        self.message = "Test ajout de fichier Robin"

    def afficher_message(self):
        print(self.message)


# Instanciation de la classe et appel de la méthode
print_rob = PrintRobin()  # Création de l'objet test
print_rob.afficher_message()  # Appel de la méthode pour afficher le message
