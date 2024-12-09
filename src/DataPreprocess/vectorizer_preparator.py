import ast
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

# Télécharger les stop words si nécessaire
nltk.download("stopwords")
nltk.download("punkt")

class VectorizerPreparator:
    def __init__(self, data):
        """
        Classe pour préparer les données textuelles pour la vectorisation.
        :param data: DataFrame contenant les colonnes textuelles à transformer.
        """
        self.data = data.copy()
        self.stemmer = SnowballStemmer("english")
        self.stop_words = set(stopwords.words("english"))

    def process_ingredients(self):
        """
        Transforme la colonne 'ingredients' en une chaîne de caractères.
        """
        if "ingredients" in self.data.columns:
            self.data["ingredients"] = self.data["ingredients"].apply(lambda x: " ".join(x))
        return self

    def process_steps(self):
        """
        Traite la colonne 'steps' : joint les étapes, enlève les stop words et la ponctuation,
        applique le stemming uniquement sur les mots, et transforme en une chaîne de caractères.
        """
        if "steps" in self.data.columns:
            def process_steps_stemming(list_steps):
                # Convertir la liste au format Python
                list_text = ast.literal_eval(list_steps)
                # Joindre les étapes
                text = " ".join(list_text)
                # Tokeniser
                tokens = nltk.word_tokenize(text)
                # Filtrer les stop words et la ponctuation, mais garder les nombres
                filtered_tokens = [
                    word for word in tokens 
                    if word.isalnum() and (word.isdigit() or word not in self.stop_words)
                ]
                # Appliquer le stemming uniquement sur les mots
                processed_tokens = [
                    self.stemmer.stem(word) if word.isalpha() else word 
                    for word in filtered_tokens
                ]
                # Reformer une chaîne de caractères
                return " ".join(processed_tokens)

            self.data["steps"] = self.data["steps"].apply(process_steps_stemming)
        return self

    def process_name(self):
        """
        Traite la colonne 'name' : enlève les stop words et la ponctuation,
        applique le stemming, et transforme en une chaîne de caractères.
        """
        if "name" in self.data.columns:
            def process_name_stemming(string_name):
                # Tokeniser
                tokens = nltk.word_tokenize(string_name)
                # Supprimer les stop words et la ponctuation
                filtered_tokens = [word for word in tokens if word.isalpha() and word not in self.stop_words]
                # Appliquer le stemming
                stemmed_tokens = [self.stemmer.stem(word) for word in filtered_tokens]
                # Reformer une chaîne de caractères
                return " ".join(stemmed_tokens)

            self.data["name"] = self.data["name"].apply(process_name_stemming)
        return self

    def process_tags(self):
        """
        Transforme la colonne 'tags' en une chaîne de caractères.
        """
        if "tags" in self.data.columns:
            self.data["tags"] = self.data["tags"].apply(lambda x: " ".join(ast.literal_eval(x)))
        return self

    def get_prepared_data(self):
        """
        Retourne le DataFrame préparé pour la vectorisation.
        """
        return self.data
