from flask import Flask, render_template, request

app = Flask(__name__)

# Exemple de base de données simple avec des recettes et le nombre d'ingrédients
recettes = {
    "Pizza": 5,
    "Salade": 3,
    "Gâteau au chocolat": 7
}

@app.route('/')
def index():
    return render_template('index.html')  # Cette fonction rend la page principale

@app.route('/recette', methods=['POST'])
def afficher_ingredients():
    recette = request.form['recette']
    nb_ingredients = recettes.get(recette, "Recette non trouvée")
    return f"La recette '{recette}' a {nb_ingredients} ingrédients."

if __name__ == '__main__':
    app.run(debug=True)
