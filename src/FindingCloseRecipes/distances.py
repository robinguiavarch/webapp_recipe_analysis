import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RecipeDistanceCalculator:
    def __init__(self, recipes_df, id_column='id'):
        self.recipes_df = recipes_df
        self.id_to_index = pd.Series(recipes_df.index, index=recipes_df[id_column])


    # Exemple pour distance_for_recipe_tfidf
    def distance_for_recipe_tfidf(self, recipe_id, tfidf_matrix):
        if recipe_id not in self.id_to_index:
            raise ValueError("Identifiant de recette introuvable.")

        recipe_idx = self.id_to_index[recipe_id]
        recipe_vector = tfidf_matrix[int(recipe_idx)]  # Gardez la matrice sparse
        cosine_similarities = cosine_similarity(recipe_vector, tfidf_matrix).flatten()
        return 1 - cosine_similarities


    def distance_for_recipe_bow(self, recipe_id, bow_matrix):
        """
        Calcule la distance de Jaccard basée sur la matrice BoW.
        :param recipe_id: Identifiant de la recette de référence.
        :param bow_matrix: Matrice BoW (DataFrame, NumPy array ou sparse matrix).
        :return: Distances cosinus inversées.
        """
        if recipe_id not in self.id_to_index:
            raise ValueError("Identifiant de recette introuvable.")
        
        # Récupérer l'index de la recette dans le DataFrame
        recipe_idx = self.id_to_index[recipe_id]

        # Si bow_matrix est une DataFrame
        if isinstance(bow_matrix, pd.DataFrame):
            recipe_vector = bow_matrix.iloc[int(recipe_idx)].to_numpy().reshape(1, -1)
            bow_matrix = bow_matrix.to_numpy()
        else:
            recipe_vector = bow_matrix[int(recipe_idx)]

        # Calculer les similarités cosinus entre la recette et toutes les autres
        cosine_similarities = cosine_similarity(recipe_vector, bow_matrix).flatten()

        return 1 - cosine_similarities


    def distance_euclidean_for_recipe(self, recipe_id, numeric_df, weights_array):
        if recipe_id not in self.id_to_index:
            raise ValueError("Identifiant de recette introuvable.")
        recipe_idx = self.id_to_index[recipe_id]
        recipe_vector = numeric_df.iloc[int(recipe_idx)].values
        differences = numeric_df.values - recipe_vector
        squared_diff = differences ** 2
        weighted_squared_diff = squared_diff * weights_array
        return np.sqrt(np.sum(weighted_squared_diff, axis=1))
