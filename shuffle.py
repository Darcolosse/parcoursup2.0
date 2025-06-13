import json
import random

# Fonction pour mélanger les valeurs dans un dictionnaire
def shuffle_json(data):
    if isinstance(data, list):
        # Mélanger la liste
        random.shuffle(data)
        # Mélanger récursivement les éléments dans la liste
        return [shuffle_json(item) for item in data]
    elif isinstance(data, dict):
        # Créer un nouveau dictionnaire avec des valeurs mélangées
        shuffled_dict = {}
        for key, value in data.items():
            if isinstance(value, (list, dict)):
                # Mélanger récursivement les structures imbriquées
                shuffled_dict[key] = shuffle_json(value)
            else:
                shuffled_dict[key] = value
        return shuffled_dict
    else:
        return data

# Charger les données JSON à partir d'un fichier
input_file_path = 'students.json'
with open(input_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Mélanger les données JSON
shuffled_data = shuffle_json(data)

# Convertir les données mélangées au format JSON
shuffled_json = json.dumps(shuffled_data, indent=2)
print(shuffled_json)

# Sauvegarder les données mélangées dans un nouveau fichier
output_file_path = 'students2.json'
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(shuffled_data, file, indent=2)
