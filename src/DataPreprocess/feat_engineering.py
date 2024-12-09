import pandas as pd
import numpy as np

class FeatEngineering:
    def __init__(self, data: pd.DataFrame):
        """
        Classe pour effectuer le feature engineering sur le dataset.
        
        :param data: DataFrame contenant les données brutes
        """
        self.data = data.copy()

    def extract_nutrition_features(self):
        """
        Sépare la colonne 'nutrition' en colonnes distinctes pour chaque type de nutrition.
        Nettoie les colonnes 'calories' et 'carbohydrates (PDV%)'.
        """
        # Séparation des colonnes
        nutrition_columns = [
            'calories', 'total fat (PDV%)', 'sugar (PDV%)', 'sodium (PDV%)',
            'protein (PDV%)', 'saturated fat (PDV%)', 'carbohydrates (PDV%)'
        ]
        self.data[nutrition_columns] = self.data['nutrition'].str.split(",", expand=True)

        # Nettoyage des données
        self.data['calories'] = self.data['calories'].apply(lambda x: x.replace('[', '') if isinstance(x, str) else x)
        self.data['carbohydrates (PDV%)'] = self.data['carbohydrates (PDV%)'].apply(lambda x: x.replace(']', '') if isinstance(x, str) else x)

        # Conversion en float
        self.data[nutrition_columns] = self.data[nutrition_columns].astype('float')
        return self

    def drop_useless_features(self):
        """
        Supprime les colonnes inutiles pour l'analyse.
        """
        columns_to_drop = ['submitted', 'nutrition', 'description', 'n_steps', 'n_ingredients']
        self.data.drop(columns=columns_to_drop, inplace=True, errors='ignore')
        return self

    def log_transform_minutes(self):
        """
        Applique une transformation logarithmique sur la colonne 'minutes' et la renomme en 'log_minutes'.
        """
        if 'minutes' in self.data.columns:
            self.data['log_minutes'] = np.log(self.data['minutes'])
            self.data.drop(columns=['minutes'], inplace=True)
        return self

    def get_preprocessed_data(self):
        """
        Retourne le DataFrame après toutes les transformations.
        """
        return self.data
