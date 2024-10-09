import logging
import os

# Vérifie si le répertoire logs existe, sinon le créer
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configurer le logger pour deux fichiers : un pour le debug et un pour les erreurs
debug_handler = logging.FileHandler("logs/debug.log")
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

error_handler = logging.FileHandler("logs/error.log")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Configurer le logger avec les deux gestionnaires
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(debug_handler)
logger.addHandler(error_handler)

class Division:
    def __init__(self, a: float, b: float) -> None:
        self.a=a
        self.b=b

    def diviser(self) -> float:
        """Divise a par b, tout en gérant la division par zéro."""
        if not isinstance(self.a, (int, float)) or not isinstance(self.b, (int, float)):
            raise ValueError("Les valeurs doivent être des nombres.")
        
        try:
            resultat = self.a / self.b
            logging.debug(f"Division réussie : {self.a} / {self.b} = {resultat}")
            return resultat
        except ZeroDivisionError:
            logging.error(f"Erreur : Division par zéro avec a={self.a} et b={self.b}")
            return float('inf')

# Créer une instance de la classe Division
division = Division(10, 2)

# Appeler la méthode diviser et afficher le résultat
print(division.diviser())  # Résultat attendu : 5.0

# Tester avec une division par zéro
division_zero = Division(10, 0)
print(
    division_zero.diviser()
)  # Résultat attendu : Erreur : Division par zéro n'est pas autorisée.
