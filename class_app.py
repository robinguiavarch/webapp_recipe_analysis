import pandas as pd
import streamlit as st
from scipy.spatial.distance import jaccard
import numpy as np
import logging
from typing import Optional, List

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("debug_app.log"),
        logging.FileHandler("errors_app.log"),
    ],
)
logger = logging.getLogger(__name__)

#effacer les données précédentes du loer pour une nouvelle exécution

class RecipeManager():
    def __init__(self, filename: str):
        self.filename = filename
        self.table_recipes = self.load_data()

    @st.cache_data
    def load_data(_self) -> pd.DataFrame:
        """Charge les données CSV avec gestion des erreurs."""
        try:
            table = pd.read_csv(_self.filename, encoding="ISO-8859-1", on_bad_lines="warn")
            table["contributor_id"] = table["contributor_id"].astype(str)
            table = table[table["contributor_id"].str.isdigit()]
            table["contributor_id"] = table["contributor_id"].astype(int)
            logger.info("Données chargées avec succès.")
            return table
        except Exception as e:
            st.error(f"Erreur lors du chargement des données : {e}")
            logger.error(f"Erreur lors du chargement des données : {e}")
            return pd.DataFrame()

    @staticmethod
    def jaccard_similarity(set1: set, set2: set) -> float:
        """Calcule la distance de Jaccard entre deux ensembles."""
        try:
            intersection = len(set1.intersection(set2))
            union = len(set1.union(set2))
            return 1 - (intersection / union)
        except Exception as e:
            logger.error(f"Erreur dans le calcul de la similarité de Jaccard : {e}")
            return float('inf')

    def validate_user_id(self, user_id: int) -> Optional[pd.DataFrame]:
        """Vérifie si un ID utilisateur existe dans la table."""
        if user_id in self.table_recipes["contributor_id"].values:
            return self.table_recipes[self.table_recipes["contributor_id"] == user_id]
        return None

    def suggest_similar_ids(self, user_input: str, max_suggestions: int = 3) -> List[int]:
        """Propose des IDs similaires basés sur la distance de Jaccard."""
        try:
            user_id_set = set(user_input)
            distances = self.table_recipes["contributor_id"].apply(
                lambda x: self.jaccard_similarity(user_id_set, set(str(x)))
            )
            self.table_recipes["jaccard_distance"] = distances
            closest_ids = self.table_recipes.nsmallest(max_suggestions, "jaccard_distance")["contributor_id"]
            return closest_ids.tolist()
        except Exception as e:
            logger.error(f"Erreur dans la suggestion d'IDs : {e}")
            return []


# Initialisation de l'application Streamlit
st.title("Gestion des Recettes 🍲")
recipe_manager = RecipeManager(filename="RAW_recipes.csv")

if recipe_manager.table_recipes.empty:
    st.error("Impossible de charger les données. Veuillez vérifier le fichier CSV.")
else:
    user_input = st.text_input("Entrez votre identifiant de contributeur :", "")

    if st.button("Valider ID"):
        if not user_input.isdigit():
            st.warning("Veuillez entrer une valeur valide pour l'ID.")
        else:
            user_id = int(user_input)
            user_recipes = recipe_manager.validate_user_id(user_id)

            if user_recipes is not None:
                st.success(f"L'ID {user_id} existe !")
                st.markdown('<div style="text-align: center;">🔻</div>', unsafe_allow_html=True)
                st.write('\n')
                cols_used = ["tags", "id", "name", "steps", "description"]
                st.dataframe(user_recipes[cols_used].head())

                recipe_input = st.text_input("Entrez un nom de recette :", "")
                if st.button("Valider cette recette"):
                    st.write(f"Voici les 100 recettes les plus proches de {recipe_input}")
                    # Ajout logique de suggestions de recettes ici...
            else:
                st.warning(f"L'ID {user_id} n'existe pas dans la base de données.")
                similar_ids = recipe_manager.suggest_similar_ids(user_input)
                if similar_ids:
                    for i, similar_id in enumerate(similar_ids, 1):
                        st.write(f"- ID proche {i} : {similar_id}")
                else:
                    st.info("Aucun ID proche n'a été trouvé.")
