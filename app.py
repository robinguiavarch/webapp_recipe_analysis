import pandas as pd
import streamlit as st
from scipy.spatial.distance import jaccard

# Chargement des données avec gestion des erreurs
@st.cache_data
def load_data(namefile : str):
    try:
        table = pd.read_csv(namefile, encoding='ISO-8859-1', on_bad_lines='warn')

        # Filtrer pour ne conserver que les IDs numériques
        table["contributor_id"] = table["contributor_id"].astype(str)
        
        table = table[table["contributor_id"].str.isdigit()]
        
        
        # Convertir les IDs en entiers
        table['contributor_id'] = table['contributor_id'].astype(int)
        
        return table
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return pd.DataFrame()

# Charger les données
table_recipes = load_data(namefile='RAW_recipes.csv')

# Vérifier si les données sont chargées correctement
if not table_recipes.empty:
    st.title("Gestion de sélection avec une liste déroulante")

    # Liste d'options
    options = ["Par ID", "Par Recette"]

    # Création de la liste déroulante
    selected_option = st.selectbox(
        "Veuillez sélectionner un moyen d'accès :",  # Titre de la liste déroulante
        options,                                     # Options disponibles
        index=0                                      # Option par défaut sélectionnée
    )

    # Affichage de la sélection
    st.write(f"Vous avez sélectionné : **{selected_option}**")

    # Action basée sur la sélection
    if selected_option == "Par ID":
        user_input = st.text_input("Entrez une valeur pour l'ID :", "")

        if st.button("Valider ID"):
            if not user_input.isdigit():
                st.warning("Veuillez entrer une valeur valide pour l'ID.")
            else:
                user_id = int(user_input)
                # Vérifier si l'ID existe dans la colonne contributor_id
                if user_id in table_recipes['contributor_id'].values:
                    st.success(f"L'ID {user_id} existe !")
                else:
                    st.warning(f"ID : {user_id} n'existe pas dans la base de données.Voici une liste des 3 IDS les plus proces")
                    user_id_vec = list(str(user_id))
                    distances = table_recipes['contributor_id'].apply(
                        lambda x: 1 - jaccard(user_id_vec, list(str(x)))
                    )
                    table_recipes['jaccard_distance'] = distances
                    closest_ids = table_recipes.nsmallest(3, 'jaccard_distance')['contributor_id']
                    for i,id in enumerate(closest_ids.tolist()):
                        st.write(f"- ID {id} (Distance de Jaccard : {table_recipes.nsmallest(3, 'jaccard_distance')['jaccard_distance'].iloc[i]:.2f})")
             

    elif selected_option == "Par Recette":
        user_input = st.number_input(
            "Entrez un nombre pour la recette :",
            min_value=0,
            max_value=100,
            step=1
        )
        if st.button("Valider Recette"):
            st.write(f"Vous avez entré : **{user_input}**")

else:
    st.error("Impossible de charger les données. Veuillez vérifier le fichier CSV.")

