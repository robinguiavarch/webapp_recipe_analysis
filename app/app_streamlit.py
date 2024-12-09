from src.FindingCloseRecipes.run_recipe_finder import run_recipe_finder
import pandas as pd
import streamlit as st
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

class RecipeManager:
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

    def find_user_recipes(self, user_id: int) -> Optional[pd.DataFrame]:
        """Trouve les recettes de l'utilisateur."""
        if user_id in self.table_recipes["contributor_id"].values:
            return self.table_recipes[self.table_recipes["contributor_id"] == user_id]
        return None


# Initialisation de l'application Streamlit
st.title("Gestion des Recettes 🍲")

# Charger le DataFrame "RAW_recipes.csv"
recipe_manager = RecipeManager(filename="data/RAW_recipes.csv")

if recipe_manager.table_recipes.empty:
    st.error("Impossible de charger les données. Veuillez vérifier le fichier CSV.")
else:
    # Saisie de l'ID utilisateur
    user_input = st.text_input("Entrez votre identifiant de contributeur :", "")

    if st.button("Valider ID"):
        if not user_input.isdigit():
            st.warning("Veuillez entrer une valeur valide pour l'ID.")
        else:
            user_id = int(user_input)
            st.session_state["user_id"] = user_id  # Sauvegarde de l'ID utilisateur

            user_recipes = recipe_manager.find_user_recipes(user_id)

            if user_recipes is not None:
                st.success(f"L'ID {user_id} existe !")
                st.markdown('<div style="text-align: center;">🔻</div>', unsafe_allow_html=True)
                cols_used = ["tags", "id", "name", "steps", "description"]
                st.session_state["user_recipes"] = user_recipes[cols_used]  # Sauvegarde des recettes de l'utilisateur
                st.dataframe(st.session_state["user_recipes"].head())
            else:
                st.warning(f"L'ID {user_id} n'existe pas dans la base de données.")

    # Si un utilisateur a été validé, afficher la suite
    if "user_id" in st.session_state:
        st.markdown("### Recettes de l'utilisateur validé")
        st.dataframe(st.session_state["user_recipes"].head())

        # Saisie de l'identifiant de recette
        recipe_input = st.text_input("Entrez l'identifiant de la recette :", "")

        if st.button("Valider cette recette"):
            if not recipe_input.isdigit():
                st.warning("Veuillez entrer un identifiant de recette valide.")
            else:
                recipe_id = int(recipe_input)
                st.session_state["recipe_id"] = recipe_id  # Sauvegarde de l'identifiant de recette

                # Trouver les indices des recettes les plus proches
                closest_indices = run_recipe_finder(recipe_id)
                st.session_state["closest_indices"] = closest_indices  # Sauvegarde des indices des recettes proches

                # Afficher les 100 recettes les plus proches
                st.write(f"Voici les 100 recettes les plus proches de la recette avec ID {recipe_id} :")
                raw_recipes = recipe_manager.table_recipes
                closest_recipes = raw_recipes.iloc[closest_indices]
                st.session_state["closest_recipes"] = closest_recipes  # Sauvegarde des recettes proches
                st.dataframe(closest_recipes)

    # Si des recettes proches ont été trouvées, afficher les résultats
    if "closest_recipes" in st.session_state:
        st.markdown("### Recettes les plus proches")
        st.dataframe(st.session_state["closest_recipes"])

