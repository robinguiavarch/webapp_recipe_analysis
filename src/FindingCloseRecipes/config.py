NUMERIC_FEATURES = [
    'log_minutes',
    'calories',
    'total fat (PDV%)',
    'sugar (PDV%)',
    'sodium (PDV%)',
    'protein (PDV%)',
    'saturated fat (PDV%)',
    'carbohydrates (PDV%)'
]

WEIGHTS = {
    'name': 0.25,
    'tags': 0.2,
    'steps': 0.25,
    'ingredients': 0.25,
    'numeric': 0.05
}

WEIGHTS_NUM = {
    'log_minutes': 0.5,
    'calories': 0.2,
    'total fat (PDV%)': 0.05,
    'sugar (PDV%)': 0.05,
    'sodium (PDV%)': 0.05,
    'protein (PDV%)': 0.05,
    'saturated fat (PDV%)': 0.05,
    'carbohydrates (PDV%)': 0.05
}
