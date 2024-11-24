import requests
import os
import dotenv
import itertools

dotenv.load_dotenv()
thesaurus_api_key = os.getenv('THESAURUS_APIKEY')


def check_limit(word, set_of_words):
    if len(word) > 3 and word not in set_of_words:
        set_of_words.add(word)


def break_word_into_possible_words(word, set_of_words):
    for i in range(len(word)):
        #adds to right side by adding characters to end of word
        new_word = word[:i]
        check_limit(new_word, set_of_words)

        # trims from left side, by moving inward
        new_word = word[i:]
        check_limit(new_word, set_of_words)

        for j in range(i + 1, len(word) + 1):
            substring = word[i:j]
            check_limit(substring, set_of_words)


def get_words_five_char(text_list):
    sum = 0
    for word in text_list:
        word_length = len(word)
        if word_length > 4:
            sum += 1
    return sum


def calc_score(score, text_list):
    weighted_sum = get_words_five_char(text_list)
    if (weighted_sum > 0):
        return round(score / weighted_sum * 100, 2)
    else:
        return round(score / len(text_list) * 100, 2)


def score_word(word, synonyms_list, keywords_sliced_list, keyword_list):
    score = 0
    for keyword in keyword_list:
        if word == keyword:
            score += 1

    for keyword in keywords_sliced_list:
        if word == keyword:
            score += 0.75

    for synonym in synonyms_list:
        if word == synonym:
            score += 0.5

        elif word in synonym:
            score += 0.25

    return score


def api_request(keyword):
    try:
        synonyms = set()
        relevant_synonyms = set()
        # 1000 queries per day
        response = requests.get(
            f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{keyword}?key={thesaurus_api_key}")
        response.raise_for_status()
        similar_words = response.json()
        if similar_words and isinstance(similar_words, list) and 'meta' in similar_words[0]:
            synonyms.update(similar_words[0]['meta']['syns'][0])
        if similar_words and isinstance(similar_words, list) and 'def' in similar_words[0]:
            relevant_synonyms = similar_words[0]['def'][0]['sseq'][0][0][1]['rel_list']
        else:
            synonyms = set()
        if len(relevant_synonyms) > 0:
            for index, group in enumerate(relevant_synonyms):
                for item in group:
                    synonyms.add(item['wd'])
    except (requests.exceptions.RequestException, KeyError, IndexError) as e:
        print(f"Error fetching synonyms for '{keyword}': {e}")
        synonyms = set()
    return synonyms


def flatten_list(word_list):
    flat_list = list(itertools.chain.from_iterable(word_list))
    return flat_list


def algorithm(text, keywords):
    score = 0
    keyword_list = keywords.split()
    text_list = text.split()
    synonyms_list = set()
    keywords_sliced_list = set()
    synonyms_sliced_list = set()
    text_sliced_list = set()

    for keyword in keyword_list:
        synonyms_list.update(api_request(keyword))
        break_word_into_possible_words(keyword, keywords_sliced_list)

    synonyms_list = flatten_list(synonyms_list)
    for synonym in synonyms_list:
        break_word_into_possible_words(synonym, synonyms_sliced_list)

    for text in text_list:
        break_word_into_possible_words(text.lower(), text_sliced_list)

    for keyword in keywords_sliced_list:
        for synonym in synonyms_sliced_list:
            if keyword == synonym:
                synonyms_sliced_list.remove(synonym)

    for text in text_sliced_list:
        score += score_word(text, synonyms_sliced_list, keywords_sliced_list, keyword_list)
    score = calc_score(score, text_list)

    return score


if __name__ == '__main__':
    keyword_input = input("What is the keywords?")
    text_input = input("What is the text?")
    print(algorithm(text_input, keyword_input))
