import requests
import os
import dotenv
import itertools

dotenv.load_dotenv()
thesaurus_api_key = os.getenv('THESAURUS_APIKEY')


def check_gt_three(word, list_of_words):
    if len(word) > 3 and word not in list_of_words:
        list_of_words.append(word)


def break_word_into_possible_words(word):
    word_list = []
    for i in range(len(word)):
        #could probably refactor this and 24-31 into one function
        #adds to right side by adding characters to end of word
        new_word = word[:i]
        check_gt_three(new_word, word_list)

        # trims from left side, by moving inward
        new_word = word[i:]
        check_gt_three(new_word, word_list)

        for j in range(i + 1, len(word) + 1):
            substring = word[i:j]
            check_gt_three(substring, word_list)

    return word_list


#add new function or modify this one to just break down each word and return a list of the substrings
def score_word(word1, word2):
    score = 0
    
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
    keywords_sliced_list = []

    for keyword in keyword_list:
        synonyms = api_request(keyword)
        keyword_sliced = break_word_into_possible_words(keyword)
        for index, item in enumerate(keyword_sliced):
            keywords_sliced_list.append(keyword_sliced[index])

    print("keywords sliced")
    print(keywords_sliced_list)
    print("synonyms")
    print(synonyms)
    text_sliced_list_flat = []
    for text in text_list:
        text_sliced_list = break_word_into_possible_words(text)
        for index, item in enumerate(text_sliced_list):
            text_sliced_list_flat.append(text_sliced_list[index])
    print("text words")
    print(text_sliced_list_flat)
    for text in text_sliced_list_flat:
        for keyword in keywords_sliced_list:
            score += score_word(text, keyword)
    if len(text_list) > 0:
        print(score)
        print(score / len(text_list) * 100)
    else:
        print("Text is empty")


if __name__ == '__main__':
    keyword_input = input("What is the keywords?")
    text_input = input("What is the text?")

    algorithm(text_input, keyword_input)
