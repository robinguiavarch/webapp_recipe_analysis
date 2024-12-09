from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import pandas as pd

class RecipeVectorizer:
    def __init__(self, recipes_df):
        self.recipes_df = recipes_df
        self.vectorizers = {}

    def vectorize_tfidf(self, column_name):
        """Vectorisation TF-IDF pour une colonne donnée."""
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(self.recipes_df[column_name])
        self.vectorizers[column_name] = vectorizer
        return tfidf_matrix  # Retourne une matrice sparse

    def vectorize_bow(self, column_name):
        """Vectorisation Bag of Words pour une colonne donnée."""
        vectorizer = CountVectorizer()
        bow_matrix = vectorizer.fit_transform(self.recipes_df[column_name])
        self.vectorizers[column_name] = vectorizer
        return bow_matrix  # Retourne une matrice sparse
