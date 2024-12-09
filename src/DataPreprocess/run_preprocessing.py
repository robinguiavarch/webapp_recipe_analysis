from src.DataPreprocess.data_preprocessor import DataPreprocessor

if __name__ == "__main__":
    file_path = "data/Raw_recipes.csv"
    ingredient_map_path = "data/ingr_map.csv"
    output_path = "data/pp_recipes.csv"

    preprocessor = DataPreprocessor(file_path, ingredient_map_path)
    preprocessor.load_data()
    preprocessor.preprocess()
    preprocessor.save_data(output_path)

    print("Préprocessing terminé. Données sauvegardées dans :", output_path)