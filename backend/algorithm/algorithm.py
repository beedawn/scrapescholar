import requests
import os
import dotenv
import itertools

dotenv.load_dotenv()
thesaurus_api_key = os.getenv('THESAURUS_APIKEY')


def api_request(keyword):
    try:
        # 1000 queries per dat
        response = requests.get(
            f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{keyword}?key={thesaurus_api_key}")
        response.raise_for_status()
        similar_words = response.json()
        if similar_words and isinstance(similar_words, list) and 'meta' in similar_words[0]:
            synonyms = similar_words[0]['meta']['syns'][0]
        else:
            synonyms = []
    except (requests.exceptions.RequestException, KeyError, IndexError) as e:
        print(f"Error fetching synonyms for '{keyword}': {e}")
        synonyms = []
    return synonyms


def algorithm(text, keywords):
    score = 0
    keyword_list = keywords.split()
    text_list = text.split()
    synonyms = []
    full_list_of_synonyms = []
    for keyword in keyword_list:
        synonyms.append(api_request(keyword))

    # Neat idea but think this just causes halucinations
    # for synonym in synonyms:
    #     for aword in synonym:
    #         full_list_of_synonyms.append(api_request(aword))

    # full_list_of_synonyms = list(itertools.chain(*full_list_of_synonyms))

    synonyms = list(itertools.chain(*synonyms))
    # synonyms.extend(full_list_of_synonyms)

    print(synonyms)
    for keyword in keyword_list:
        for word in text_list:
            if keyword == word:
                score += 1
            elif word in synonyms:
                score += .5
    if len(text_list) > 0:
        print(score / len(text.split()) * 100)
    else:
        print("Text is empty")


if __name__ == '__main__':
    keyword_input = input("What is the keywords?")
    text_input = input("What is the text?")

    algorithm(text_input, keyword_input)
