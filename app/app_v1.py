import pandas as pd
import streamlit as st
from recipe_app import RecipeApp

# Charger les datasets avec l'option low_memory=False
merged_clean_df = pd.read_csv('base_light_V3.csv', low_memory=False)
ingredients_part1 = pd.read_csv('id_ingredients_up_to_207226.csv', low_memory=False)
ingredients_part2 = pd.read_csv('id_ingredients_up_to_537716.csv', low_memory=False)

# Ajouter un fond d'écran (image à partir de l'URL)
page_bg_img = '''
<style>
.stApp {
    background-image: url("https://burst.shopifycdn.com/photos/flatlay-iron-skillet-with-meat-and-other-food.jpg?width=925&format=pjpg&exif=0&iptc=0");
    background-size: cover;
    background-repeat: no-repeat; 
    background-attachment: fixed;
}
body {
    color: #8B4513; /* Change tout le texte au centre en marron */
}
h1, h2, h3, h4, h5, h6 {
    color: #8B4513; /* Couleur du texte */
    background-color: rgba(255, 255, 255, 0.8); /* Rectangle blanc semi-transparent */
    padding: 10px; /* Espacement interne */
    border-radius: 10px; /* Coins arrondis */
    display: inline-block; /* Ajuster la taille du rectangle au texte */
    text-align: center; /* Centrer le texte */
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2); /* Ajouter une ombre légère */
}
.sidebar .block-container h1, .sidebar .block-container h2, .sidebar .block-container h3, .sidebar .block-container h4 {
    font-size: larger; /* Augmente la taille des textes dans la barre latérale */
}
.stTextContainer {
    color: #8B4513; /* Couleur du texte dans les rectangles */
    background-color: rgba(255, 255, 255, 0.8); /* Rectangle blanc semi-transparent */
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 15px;
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2); /* Ombre légère */
}
.sidebar-content {
    visibility: visible; /* Ouvre le menu de gauche par défaut */
    opacity: 1;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Style pour personnaliser le menu et agrandir la flèche
menu_style = '''
<style>
.sidebar .block-container label {
    font-weight: bold;
    font-style: italic;
    font-size: large; /* Augmente la taille du texte Menu */
}
.sidebar .block-container .radio {
    font-size: larger; /* Augmente la taille des options Accueil et Idée recette */
}
.css-1v0mbdj .stSelectbox div[role="combobox"] {
    font-size: larger; /* Augmente la taille du texte dans le menu déroulant */
}
.css-1v0mbdj .stSelectbox div[role="combobox"]::after {
    content: " ⬇️ Chercher ici !"; /* Ajoute le texte "Chercher ici" avec une grande flèche */
    font-size: larger;
    font-weight: bold;
    color: #8B4513; /* Marron pour correspondre au thème */
}
</style>
'''
st.markdown(menu_style, unsafe_allow_html=True)

# Créer le menu pour changer de page
menu = st.sidebar.radio("**_Menu_**", ["Accueil", "Idée recette !"], index=0)

if menu == "Accueil":
    # Titre de l'application
    st.title("Recherche des meilleures recettes")

    # Ajout de filtres interactifs (placés à droite)
    with st.sidebar:
        st.header("Filtres")
        selected_palmares = st.multiselect(
            "Filtrer par palmarès",
            options=merged_clean_df['palmarès'].unique(),
            default=merged_clean_df['palmarès'].unique()
        )

        selected_steps_category = st.multiselect(
            "Filtrer par catégorie de steps",
            options=merged_clean_df['steps_category'].unique(),
            default=merged_clean_df['steps_category'].unique()
        )

    # Appliquer les filtres
    filtered_df = merged_clean_df[
        (merged_clean_df['palmarès'].isin(selected_palmares)) & 
        (merged_clean_df['steps_category'].isin(selected_steps_category))
    ]

    # Menu déroulant pour sélectionner un contributor_id
    unique_contributor_ids = sorted(filtered_df['contributor_id'].unique())
    contributor_id = st.selectbox("Sélectionnez un contributor_id :", options=unique_contributor_ids)

    # Vérifier si un contributor_id est sélectionné
    if contributor_id:
        # Filtrer les données pour le contributor_id
        contributor_recipes = filtered_df[filtered_df['contributor_id'] == contributor_id]

        if not contributor_recipes.empty:
            # Limiter à 20 recettes maximum
            top_20_ids = contributor_recipes['id'].head(20)

            # Filtrer les fichiers d'ingrédients pour les IDs sélectionnés
            relevant_ingredients_part1 = ingredients_part1[ingredients_part1['id'].isin(top_20_ids)]
            relevant_ingredients_part2 = ingredients_part2[ingredients_part2['id'].isin(top_20_ids)]

            # Fusionner les deux datasets d'ingrédients
            ingredients_combined = pd.concat([relevant_ingredients_part1, relevant_ingredients_part2])

            # Fusionner avec les données principales
            merged_data = pd.merge(contributor_recipes, ingredients_combined, on='id', how='inner')

            # Sélectionner les colonnes importantes
            display_data = merged_data[['name', 'average_rating', 'minutes', 'palmarès', 'steps_category', 'ingredients']].head(20)

            # Afficher les données
            st.subheader(f"Recettes pour le contributor_id {contributor_id} (max 20 recettes)")
            st.dataframe(display_data)
        else:
            st.warning("Aucune recette trouvée pour ce contributor_id.")

    # Afficher les données filtrées avec les filtres interactifs
    st.subheader("Recettes filtrées selon vos critères")
    st.dataframe(filtered_df[['name', 'average_rating', 'minutes', 'palmarès', 'steps_category']].head(10))

elif menu == "Idée recette !":
    # Titre de la page
    st.title("Idée recette !")
    st.markdown('<div class="stTextContainer">Ici, vous pouvez explorer de nouvelles idées de recettes.</div>', unsafe_allow_html=True)

    # Instancier et exécuter RecipeApp
    app = RecipeApp()
    app.run()
