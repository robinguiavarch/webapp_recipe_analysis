import pandas as pd
from src.DataPreprocess.normalizer import Normalizer
from src.DataPreprocess.feat_engineering import FeatEngineering
from src.DataPreprocess.data_cleaning import DataCleaning
from src.DataPreprocess.vectorizer_preparator import VectorizerPreparator

class DataPreprocessor:
    def __init__(self, file_path, ingredient_map_path):
        """
        Classe pour charger, nettoyer, traiter et sauvegarder les données.
        :param file_path: Chemin vers le fichier de données brut
        :param ingredient_map_path: Chemin vers le fichier de mapping des ingrédients
        """
        self.file_path = file_path
        self.ingredient_map_path = ingredient_map_path
        self.data = None

    def load_data(self):
        """
        Charge les données depuis le fichier CSV.
        """
        self.data = pd.read_csv(self.file_path)
        return self.data

    def save_data(self, output_path):
        """
        Sauvegarde les données prétraitées dans un fichier CSV.
        :param output_path: Chemin vers le fichier de sortie
        """
        self.data.to_csv(output_path, index=False)

    def preprocess(self):
        """
        Pipeline complet de prétraitement.
        Étapes : Nettoyage des données, Feature Engineering, Préparation pour la vectorisation, Normalisation.
        """
        # Étape 1 : Nettoyage des données préliminaire
        cleaner = DataCleaning(self.data)
        self.data = (
            cleaner
            .replace_zero_minutes(replacement_minutes=8)         # Remplace les 0 dans 'minutes'
            .remove_long_recipes(max_minutes=30*24*60)          # Supprime les recettes avec un temps de préparation > 1 mois
            .map_ingredients(self.ingredient_map_path)         # Remplace les noms d'ingrédients par des catégories
            .get_cleaned_data()
        )

        # Étape 2 : Feature engineering
        feat_engineer = FeatEngineering(self.data)
        self.data = (
            feat_engineer
            .extract_nutrition_features()                       # Crée les colonnes nutritionnelles
            .drop_useless_features()                            # Supprime les colonnes inutiles
            .log_transform_minutes()                            # Transforme 'minutes' en 'log_minutes'
            .get_preprocessed_data()
        )

        # Supprime les lignes contenant des NaN après le Feature Engineering
        cleaner = DataCleaning(self.data)
        self.data = cleaner.handle_missing_values().get_cleaned_data()

        # Étape 3 : Suppression des recettes riches en calories (après création des colonnes nutritionnelles)
        self.data = (
            DataCleaning(self.data)
            .remove_high_calories_recipes(max_calories=10000)   # Supprime les recettes avec des calories > 10,000
            .get_cleaned_data()
        )

        # Étape 4 : Préparation pour la vectorisation
        vectorizer = VectorizerPreparator(self.data)
        self.data = (
            vectorizer
            .process_ingredients()
            .process_steps()
            .process_name()
            .process_tags()
            .get_prepared_data()
        )

        # Étape 5 : Normalisation
        normalizer = Normalizer()
        self.data = normalizer.normalize(self.data)

        # Supprime les lignes contenant des NaN à la toute fin du pipeline
        cleaner = DataCleaning(self.data)
        self.data = cleaner.handle_missing_values().get_cleaned_data()

        return self.data





