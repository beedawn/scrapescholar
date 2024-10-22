import requests
import os
import dotenv
import itertools

dotenv.load_dotenv()
thesaurus_api_key = os.getenv('THESAURUS_APIKEY')


def slice_word(word, synonyms, keyword_list):
    score = 0
    for i in range(len(word)):
        new_word = word[:i]
        print(new_word)
        if new_word in synonyms:
            print(new_word)
            score += .25
        if new_word in keyword_list:
            score += .5
    for i in range(len(word)):
        new_word = word[i:]
        print(new_word)
        if new_word in synonyms:
            print(new_word)
            # score += .75
        if new_word in keyword_list:
            score += .5

    for i in range(len(word)):
        for j in range(i + 1, len(word) + 1):
            substring=word[i:j]
            if substring in keyword_list:
                print(substring)
                score += .25
            if substring in synonyms:
                print(substring)
                score += .10
    return score


def api_request(keyword):
    try:
        # 1000 queries per day
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

    for keyword in keyword_list:
        synonyms = api_request(keyword)

    # full_list_of_synonyms = []
    # Neat idea but think this just causes halucinations
    # for synonym in synonyms:
    #     for aword in synonym:
    #         full_list_of_synonyms.append(api_request(aword))

    # full_list_of_synonyms = list(itertools.chain(*full_list_of_synonyms))

    # synonyms = list(itertools.chain(*synonyms))
    # synonyms.extend(full_list_of_synonyms)

    print(synonyms)
    for keyword in keyword_list:
        for word in text_list:
            if keyword == word:
                score += 1
                print("plus 1")
                continue
            elif word in synonyms:
                score += .5
            score += (
                slice_word(word, synonyms, keyword_list)
                )

    if len(text_list) > 0:
        print(score)
        print(score / len(text_list) * 100)
    else:
        print("Text is empty")


if __name__ == '__main__':
    keyword_input = input("What is the keywords?")
    text_input = input("What is the text?")

    algorithm(text_input, keyword_input)
