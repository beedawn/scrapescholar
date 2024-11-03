import json
from collections import defaultdict

def create_subdictionaries(file_path):
    with open(file_path, 'r') as file:
        words = json.load(file)

    subdictionaries = defaultdict(list)

    # Iterate over words and add them to the appropriate subdictionary
    for word in words:
        if len(word) >= 3:
            prefix = word[:3]
            subdictionaries[prefix].append(word)

    return dict(subdictionaries)

       
create_subdictionaries("./words_dictionary.json")
