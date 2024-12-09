import pandas as pd
import ast

class DataCleaning:
    def __init__(self, data: pd.DataFrame):
        """
        Classe pour nettoyer les données, en supprimant les outliers et en traitant les anomalies.
        :param data: DataFrame contenant les données brutes
        """
        self.data = data.copy()

    def remove_long_recipes(self, max_minutes: int = 30*24*60):
        """
        Supprime les recettes dont le temps de préparation dépasse la limite spécifiée.
        :param max_minutes: Temps maximal en minutes (par défaut : 30 jours)
        """
        self.data = self.data[self.data['minutes'] <= max_minutes]
        return self

    def replace_zero_minutes(self, replacement_minutes: int = 8):
        """
        Remplace les valeurs de 'minutes' égales à 0 par une valeur par défaut.
        :param replacement_minutes: Valeur de remplacement pour les 0 (par défaut : 8 minutes)
        """
        self.data.loc[self.data['minutes'] == 0, 'minutes'] = replacement_minutes
        return self

    def remove_high_calories_recipes(self, max_calories: int = 10000):
        """
        Supprime les recettes ayant des calories supérieures à une valeur seuil.
        :param max_calories: Seuil maximal de calories (par défaut : 10,000)
        """
        if 'calories' in self.data.columns:
            self.data = self.data[self.data['calories'] <= max_calories]
        return self

    def map_ingredients(self, ingredient_map_path: str):
        """
        Remplace les noms d'ingrédients par des catégories générales en utilisant un fichier de mapping.
        :param ingredient_map_path: Chemin vers le fichier CSV contenant les mappings.
        """
        # Charger le fichier de mapping
        ingr_map = pd.read_csv(ingredient_map_path)
        ingredient_mapping = dict(zip(ingr_map['raw_ingr'], ingr_map['replaced']))

        # Fonction de remplacement des ingrédients dans une liste
        def replace_ingredients(ingredient_list):
            ingredients = ast.literal_eval(ingredient_list)  # Convertir la liste au format Python
            return [ingredient_mapping.get(ingredient, ingredient) for ingredient in ingredients]

        # Appliquer la fonction à la colonne 'ingredients'
        if 'ingredients' in self.data.columns:
            self.data['ingredients'] = self.data['ingredients'].apply(replace_ingredients)
        return self
    
    def handle_missing_values(self):
        """
        Gère les valeurs manquantes dans le DataFrame :
        - Remplace les chaînes vides et les 'None' par des NaN.
        - Supprime toutes les lignes contenant au moins un NaN dans n'importe quelle colonne.
        """
        # Remplacer les chaînes vides et 'None' par NaN
        self.data.replace("", pd.NA, inplace=True)  # Remplace les chaînes vides
        self.data.replace("None", pd.NA, inplace=True)  # Remplace les valeurs 'None'

        # Supprimer toutes les lignes avec au moins un NaN
        self.data = self.data.dropna()
        return self

    def get_cleaned_data(self):
        """
        Retourne le DataFrame nettoyé.
        """
        return self.data
