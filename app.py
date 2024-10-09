import streamlit as st
import pandas as pd
import ast  # N'oubliez pas d'importer ast

# Liste des ingrédients macro
ingredients_macro = [
    "butter", "sugar", "onion", "water", "eggs", "oil", "flour",
    "milk", "garlic", "pepper", "baking powder", "egg", "cheese",
    "lemon juice", "baking soda", "vanilla", "cinnamon", "tomatoe",
    "sour cream", "honey", "cream cheese", "celery", "soy sauce",
    "mayonnaise", "paprika", "chicken", "worcestershire sauce",
    "parsley", "cornstarch", "carrot", "chili", "bacon", "potatoe"
]

# Lire le fichier CSV
df = pd.read_csv("RAW_recipes.csv")


# Créez une copie du DataFrame
petit_df = df.iloc[:30].copy()

# Convertir la colonne 'ingredients' en listes si ce n'est pas déjà le cas
petit_df['ingredients'] = petit_df['ingredients'].apply(ast.literal_eval)

# Afficher le DataFrame et vérifier les ingrédients
st.write("Ingrédients avant normalisation:")
st.write(petit_df[['ingredients']].head())

# Fonction pour normaliser les ingrédients
def normalize_ingredients(ingredient_list):
    normalized_list = []
    for ingredient in ingredient_list:
        for macro in ingredients_macro:
            if macro in ingredient:  # Vérifie si l'ingrédient contient un des mots-clés
                normalized_list.append(macro)
                break
    return normalized_list  # Retourne seulement les ingrédients normalisés

# Créer la nouvelle colonne 'ingredient_macro'
petit_df['ingredient_macro'] = petit_df['ingredients'].apply(normalize_ingredients)

# Afficher le DataFrame final
st.write("DataFrame après normalisation:")
st.write(petit_df)

# Titre de l'application
st.title("Recettes et Ingrédients Macro")

# Sélection des ingrédients macro
selected_ingredients = st.multiselect("Sélectionnez des ingrédients macro", ingredients_macro)

# Filtrer les recettes en fonction des ingrédients sélectionnés
if selected_ingredients:
    filtered_recipes = petit_df[petit_df['ingredients'].apply(lambda x: any(ingredient in x for ingredient in selected_ingredients))]
    
    # Afficher les recettes correspondantes
    st.write(f"Recettes contenant {', '.join(selected_ingredients)} :")
    if not filtered_recipes.empty:
        for index, row in filtered_recipes.iterrows():
            st.write(f"- {row['name']}")  # Afficher le nom de la recette
    else:
        st.write("Aucune recette ne correspond à ces ingrédients.")
else:
    st.write("Veuillez sélectionner des ingrédients pour voir les recettes.")