from sklearn.preprocessing import StandardScaler

class Normalizer:
    def __init__(self):
        self.scaler = StandardScaler()

    def normalize(self, data):
        columns_to_normalize = [
            'log_minutes', 'calories', 'total fat (PDV%)', 'sugar (PDV%)',
            'sodium (PDV%)', 'protein (PDV%)', 'saturated fat (PDV%)', 'carbohydrates (PDV%)'
        ]
        data[columns_to_normalize] = self.scaler.fit_transform(data[columns_to_normalize])
        return data