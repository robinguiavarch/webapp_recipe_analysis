import pandas as pd
import streamlit as st
from scipy.spatial.distance import jaccard
import numpy as np

# Chargement des données avec gestion des erreurs
@st.cache_data
def load_data(namefile : str):
    try:
        table = pd.read_csv(namefile, encoding='ISO-8859-1', on_bad_lines='warn')

        # Filtrer pour ne conserver que les IDs numériques
        table["contributor_id"] = table["contributor_id"].astype(str)
        
        table = table[table["contributor_id"].str.isdigit()]
        
        table["contributor_id"] = table["contributor_id"].astype(int)
                    
        return table
    
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return pd.DataFrame()
    
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return 1 - (intersection / union)

# Charger les données
table_recipes = load_data(namefile='RAW_recipes.csv')

if table_recipes.empty:
    st.error("Impossible de charger les données. Veuillez vérifier le fichier CSV.")

# Vérifier si les données sont chargées correctement

# Liste d'options
# options = ["Par ID"]

# # Création de la liste déroulante
# selected_option = st.selectbox(
#     "Veuillez sélectionner un moyen d'accès :",  # Titre de la liste déroulante
#     options,                                     # Options disponibles
#     index=0                                      # Option par défaut sélectionnée
# )

# # Affichage de la sélection
# st.write(f"Vous avez sélectionné : **{selected_option}**")

st.set_option('client.showErrorDetails', False)


user_input = (st.text_input("Entrez votre identifiant de contributeur :", ""))

if st.button("Valider ID"):
    if not user_input.isdigit():
        st.warning("Veuillez entrer une valeur valide pour l'ID.")
    else:
        user_id = int(user_input)
        # Vérifier si l'ID existe dans la colonne contributor_id
        if user_id in table_recipes['contributor_id'].values:
            cols_used = ['tags','id','name','steps','description']
            st.success(f"L'ID {user_id} existe !")
            st.markdown('<div style="text-align: center;">🔻</div>', unsafe_allow_html=True)
            st.write('\n')
            with st.container():
                st.dataframe(table_recipes[table_recipes['contributor_id'] == user_id][cols_used].head())

            recipe_input = st.text_input("Entrez un nom de recette :", "")
            #filtrer avec ttes les recettes id qu'il a fait (tt)
            #id_recette
        else:
            st.warning(f"ID : {user_id} n'existe pas dans la base de données")
            user_id_set = set(user_input)
            distances = table_recipes['contributor_id'].apply(
                lambda x: jaccard_similarity(user_id_set, set(str(x)))
            )
            table_recipes['jaccard_distance'] = distances
            closest_ids = table_recipes.nsmallest(3, 'jaccard_distance')['contributor_id']
            for i,id in enumerate(closest_ids.tolist()):
                if np.abs(len(str(id))-len(user_input)) > 2:
                    if i == closest_ids.size:
                        st.write("Aucun ID proche n'a été trouvé")
                    continue                   
                st.write(f"- ID proche {i+1} : {id}")
        



