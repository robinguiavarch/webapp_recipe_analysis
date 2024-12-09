import numpy as np

class RecipeFinder:
    def __init__(self, recipes_df, id_column='id'):
        self.recipes_df = recipes_df
        self.id_column = id_column

    def find_closest_recipes(self, recipe_id, distances_dict, weights, top_n=100):
        """
        Trouve les indices des recettes les plus proches en combinant plusieurs distances.
        """
        # Vérifier la somme des poids
        assert sum(weights.values()) == 1, "La somme des poids doit être égale à 1."

        # Calculer la distance combinée
        combined_distance = sum(weights[key] * distances for key, distances in distances_dict.items())

        # Trier les indices par distance croissante
        sorted_indices = combined_distance.argsort()

        # Exclure la recette elle-même
        recipe_index = self.recipes_df.index[self.recipes_df[self.id_column] == recipe_id].tolist()[0]
        sorted_indices = sorted_indices[sorted_indices != recipe_index]

        # Obtenir les indices des recettes similaires
        top_n_indices = sorted_indices[:top_n]

        return top_n_indices

