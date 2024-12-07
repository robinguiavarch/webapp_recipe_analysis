from typing import List
import requests
from PIL import Image
import io
import streamlit as st
import logging
import pandas as pd

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("debug_app.log"),
        logging.FileHandler("errors_app.log"),
    ],
)

# Fonction pour réinitialiser les logs
def reset_logger():
    # Supprimer tous les handlers de log existants
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    # Reconfigurer le logger avec un nouveau handler
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


logger = logging.getLogger(__name__)

class AppManager:

    def hide_streamlit_ui_elements(self, hide_menu: bool = True, hide_footer: bool = True, custom_class: str = None):
        """
        Masque certains éléments de l'interface Streamlit, comme le menu, le footer, ou des éléments spécifiques.

        Parameters:
        ----------
        hide_menu : bool, optional
            Indique si le menu de Streamlit doit être masqué. Par défaut, True.
        hide_footer : bool, optional
            Indique si le footer de Streamlit doit être masqué. Par défaut, True.
        custom_class : str, optional
            Nom de classe CSS spécifique à masquer. Si None, aucun div supplémentaire ne sera masqué.

        Returns:
        -------
        None
            Applique les styles CSS pour masquer les éléments dans l'interface utilisateur Streamlit.

        Raises:
        ------
        Exception
            Si une erreur survient lors de l'application des styles.
        """
        try:
            # Construire le style CSS de manière dynamique
            hide_streamlit_style = """
            <style>
            """
            if hide_menu:
                hide_streamlit_style += """
                header {visibility: hidden;}
                """
            if hide_footer:
                hide_streamlit_style += """
                .streamlit-footer {display: none;}
                """
            if custom_class:
                hide_streamlit_style += f"""
                .{custom_class} {{display: none;}}
                """
            hide_streamlit_style += """
            </style>
            """
            # Appliquer le style CSS
            st.markdown(hide_streamlit_style, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Erreur lors du masquage des éléments Streamlit : {e}")

    def suggest_similar_ids(self,table_recipes : pd.DataFrame, user_input: str, max_suggestions: int = 3) -> List[int]:
        """
        Propose des IDs similaires basés sur la distance de Jaccard entre l'entrée utilisateur
        et les contributeurs dans la table des recettes.

        Parameters:
        ----------
        table_recipes : pd.DataFrame
            Dataframe des recettes
        user_input : str
            Identifiant de l'utilisateur sous forme de chaîne.
        max_suggestions : int, optional
            Nombre maximum d'IDs similaires à retourner (par défaut 3).
        

        Returns:
        -------
        List[int]
            Liste des IDs similaires triés par distance croissante.
        """
        try:
            user_id_set = set(user_input)
            distances = table_recipes["contributor_id"].apply(
                lambda x: self.jaccard_similarity(user_id_set, set(str(x)))
            )
            table_recipes["jaccard_distance"] = distances
            closest_ids = table_recipes.nsmallest(max_suggestions, "jaccard_distance")["contributor_id"]
            return closest_ids.tolist()
        except Exception as e:
            logger.error(f"Erreur dans la suggestion d'IDs : {e}")
            return []

    @staticmethod
    def jaccard_similarity(set1: set, set2: set) -> float:
        """
        Calcule la distance de Jaccard entre deux ensembles.

        Parameters:
        ----------
        set1 : set
            Premier ensemble à comparer.
        set2 : set
            Second ensemble à comparer.

        Returns:
        -------
        float
            Distance de Jaccard (1 - similarité de Jaccard). Retourne `float('inf')` en cas d'erreur.
        """
        try:
            intersection = len(set1.intersection(set2))
            union = len(set1.union(set2))
            return 1 - (intersection / union)
        except Exception as e:
            logger.error(f"Erreur dans le calcul de la similarité de Jaccard : {e}")
            return float('inf')

    def set_image(self, image_url: str):
        """
        Télécharge une image depuis une URL et l'affiche dans l'application.

        Parameters:
        ----------
        url_im : str
            URL de l'image à télécharger et afficher.

        Returns:
        -------
        None
            Affiche l'image dans l'interface utilisateur Streamlit.

        Raises:
        ------
        requests.RequestException
            En cas d'erreur de téléchargement de l'image depuis l'URL.
        Exception
            Pour toute autre erreur non prévue.
        """
        try:
            # Télécharger l'image distante
            response = requests.get(url_im,timeout=10)
            response.raise_for_status()  # Vérifie les erreurs HTTP

            # Lire l'image directement depuis les données téléchargées
            image = Image.open(io.BytesIO(response.content))
            image = image.resize((200, 100))

            # Afficher l'image
            st.image(image, caption="", use_container_width=True)

        except requests.RequestException as e:
            st.error(f"Erreur lors du téléchargement de l'image : {e}")
        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")
            
            
    def set_background_image(self, image_url: str):
        """
        Définit une image de fond pour l'application Streamlit à partir d'une URL.

        Parameters:
        ----------
        image_url : str
            URL de l'image à utiliser comme arrière-plan.

        Returns:
        -------
        None
            Applique l'image de fond dans l'interface utilisateur Streamlit.

        Raises:
        ------
        Exception
            Si une erreur survient lors de l'application de l'image.
        """
        try:
            # Générer le style CSS pour l'image de fond
            background_style = f"""
            <style>
            .stApp {{
                background: url("{image_url}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """
            # Appliquer le style
            st.markdown(background_style, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Erreur lors de l'application de l'image de fond : {e}")
            

    def display_adjusted_title(self, title: str, margin_top: int = 50, emoji: str = "🍲"):
        """
        Affiche un titre personnalisé avec un style ajusté pour Streamlit.

        Parameters:
        ----------
        title : str
            Le texte du titre à afficher.
        margin_top : int, optional
            La marge supérieure du titre (en pixels). Par défaut, 50.
        emoji : str, optional
            Un emoji à afficher à côté du titre. Par défaut, "🍲".

        Returns:
        -------
        None
            Le titre est directement rendu dans l'interface utilisateur Streamlit.
        """
        try:
            # Créer le style CSS pour ajuster la position du titre
            adjust_title_style = f"""
            <style>
            h1 {{
                position: fixed;
                margin-top: {margin_top}px; /* Ajuste la marge supérieure */
            }}
            </style>
            """
            # Appliquer le style et afficher le titre
            st.markdown(adjust_title_style, unsafe_allow_html=True)
            st.markdown(f'<h1 class="title">{title} {emoji}</h1>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Erreur lors de l'affichage du titre ajusté : {e}")

    def plot_tsne_ingredients(self, frac: float = 0.1, num_ingredients: int = 20):
        """
        Effectue une réduction de dimension avec t-SNE sur les ingrédients d'un dataset
        et trace une visualisation des ingrédients dominants.

        Parameters:
        ----------
        frac : float, optional
            Fraction du dataset à échantillonner pour la visualisation. Par défaut, 0.1.
        num_ingredients : int, optional
            Nombre d'ingrédients les plus fréquents à considérer pour la visualisation. Par défaut, 20.

        Returns:
        -------
        None
            Affiche une visualisation t-SNE dans l'application Streamlit.

        Raises:
        ------
        Exception
            Si une erreur survient lors de la génération ou de l'affichage de la visualisation.
        """
        try:
            import matplotlib.pyplot as plt
            from sklearn.decomposition import PCA
            from sklearn.manifold import TSNE
            from sklearn.feature_extraction.text import TfidfVectorizer
            from collections import Counter

            # Charger et échantillonner les données
            sampled_recipes = self.recipes.sample(frac=frac)
            
            # Identifier les ingrédients les plus fréquents
            all_ingredients = sampled_recipes['ingredients'].str.split().explode()
            top_ingredients = [item[0] for item in Counter(all_ingredients).most_common(num_ingredients)]

            # Filtrer les ingrédients
            sampled_recipes['filtered_ingredients'] = sampled_recipes['ingredients'].apply(
                lambda x: ' '.join([word for word in x.split() if word in top_ingredients])
            )

            # Identifier un ingrédient dominant
            def get_dominant_ingredient(ingredients):
                ingredient_list = ingredients.split()
                for ingredient in top_ingredients:
                    if ingredient in ingredient_list:
                        return ingredient
                return 'Other'

            sampled_recipes['dominant_ingredient'] = sampled_recipes['filtered_ingredients'].apply(get_dominant_ingredient)

            # Vectorisation avec TF-IDF
            vectorizer = TfidfVectorizer(stop_words='english')
            X = vectorizer.fit_transform(sampled_recipes['filtered_ingredients'])

            # Réduction avec PCA
            pca = PCA(n_components=5)
            X_pca = pca.fit_transform(X.toarray())

            # Réduction avec t-SNE
            tsne = TSNE(n_components=2, random_state=42, n_jobs=-1, perplexity=30, learning_rate=200, max_iter=300)
            X_tsne = tsne.fit_transform(X_pca)

            # Ajouter les coordonnées t-SNE au dataset
            sampled_recipes['tsne1'] = X_tsne[:, 0]
            sampled_recipes['tsne2'] = X_tsne[:, 1]

            # Générer une palette de couleurs dynamique
            unique_classes = sampled_recipes['dominant_ingredient'].nunique()
            palette = sns.color_palette("tab20", n_colors=unique_classes)

            # Visualisation
            plt.figure(figsize=(12, 8))
            sns.scatterplot(
                x='tsne1',
                y='tsne2',
                hue='dominant_ingredient',
                data=sampled_recipes,
                palette=palette,
                s=100,
                marker='o'
            )

            plt.title("t-SNE Visualization of Recipe Ingredients (Dominant Ingredients)", fontsize=16)
            plt.xlabel("t-SNE Component 1", fontsize=12)
            plt.ylabel("t-SNE Component 2", fontsize=12)
            plt.legend(title="Dominant Ingredient", bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.xticks([])  
            plt.yticks([])  
            plt.show()

        except Exception as e:
            st.error(f"Erreur lors de la génération du graphique t-SNE : {e}")





            
adjust_title_style = """
<style>
h1 {
    position: fixed;
    margin-top: 50px; /* Ajuste la marge supérieure, réduisez la valeur pour descendre le titre */
}
</style>
"""

st.markdown('<h1 class="title">Comparateur de Recettes 🍲</h1>', unsafe_allow_html=True)

st.markdown("""
    <script>
        document.addEventListener('keydown', function(event) {
            if (event.key === "Escape") {
                // Vous pouvez choisir ce que vous voulez faire ici. Par exemple, pour stopper l'application, rafraîchissez la page.
                window.location.reload();
            }
        });
    </script>
""", unsafe_allow_html=True)



hide_streamlit_style = """
            <style>
                /* Hide the Streamlit header and menu */
                header {visibility: hidden;}
                /* Optionally, hide the footer */
                .streamlit-footer {display: none;}
                /* Hide your specific div class, replace class name with the one you identified */
                .st-emotion-cache-uf99v8 {display: none;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
