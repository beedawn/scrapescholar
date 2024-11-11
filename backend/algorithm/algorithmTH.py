import requests
import os
import dotenv
import itertools
import json
import string

dotenv.load_dotenv()
thesaurus_api_key = os.getenv('THESAURUS_APIKEY')
dictionary_api_key = os.getenv('DICTIONARY_APIKEY')
# file_path = os.path.join(os.path.dirname(__file__), 'words_dictionary.json')
# print("File Path")
# print(file_path)

# with open(file_path) as f:
#     data = json.load(f)

def check_limit(word, set_of_words):
    if len(word) >= 3 and word not in set_of_words:                  ##### do you even need this loop?
        set_of_words.add(word)
        print("Set of Words")
        print(set_of_words)


def break_word_into_possible_words(word, set_of_words):
    for i in range(len(word)):
        if i+3 < len(word)+1:                                             ##### i + 3 saves running the first two iterations of the loop
            #adds to right side by adding characters to end of word
            print("Break word into poss keywords loop:" + str(i))
            new_word = word[:i+3]                                       ###### i + 1 saves one loop
            print("New Word: " + new_word)
            check_limit(new_word, set_of_words)

        # trims from left side, by moving inward
        new_word = word[i:]
        check_limit(new_word, set_of_words)

        # for j in range(i + 1, len(word) + 1):
        #     substring = word[i:j]
        #     check_limit(substring, set_of_words)


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


def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)


def algorithm(text, keywords):
    score = 0
    keyword_list = keywords.split()
    print("Keyword List")
    print(keyword_list)
    no_punctuation_text = remove_punctuation(text)
    text_list = no_punctuation_text.split()
    print("Text List")
    print(text_list)
    synonyms_list = set()
    keywords_sliced_list = set()
    synonyms_sliced_list = set()
    text_sliced_list = set()

    for keyword in keyword_list:
        synonyms_list.update(api_request(keyword))
        print('Synonym List')
        print(synonyms_list)
        break_word_into_possible_words(keyword, keywords_sliced_list)
        print("done with breaking keywords")
    #flatten synonyms list since its not flat
    synonyms_list = flatten_list(synonyms_list)
    for synonym in synonyms_list:
        break_word_into_possible_words(synonym, synonyms_sliced_list)

    for text in text_list:
        break_word_into_possible_words(text, text_sliced_list)

    for keyword in keywords_sliced_list:
        for synonym in synonyms_sliced_list:
            if keyword == synonym:
                synonyms_sliced_list.remove(synonym)

    for text in text_sliced_list:
        score += score_word(text, synonyms_sliced_list, keywords_sliced_list, keyword_list)
    score = calc_score(score, text_list)

    return score


def clean(text):
    text_list = set()   
    no_punctuation_text = remove_punctuation(text)
    text_list_no_punct = no_punctuation_text.split()
    for text_item in text_list_no_punct:
        if len(text_item) > 3:
            text_list.add(text_item.lower())
    print("Text List")
    print(text_list)
    return(text_list)


def compare(text, keywords):
    num_similar = 0
    for item in text:
        if item in keywords:
            num_similar += 1
    return([num_similar, len(text)])

def get_stems(keywords):
    score = 0
    
    keyword_stems = set()

    keyword_list = keywords.split()
    for each_item in keyword_list:
        keyword_stems.add(each_item)
    print("Keyword List")
    print(keyword_stems)


    # keywords_list = set()
    # similar_list = set()
    
    # keyword_definition = set()

    for word in keyword_list:
        print("word = " + word)
        response = requests.get("https://www.dictionaryapi.com/api/v3/references/thesaurus/json/"+word+"?key="+thesaurus_api_key)
        responseJSON = response.json()
        # print(responseJSON)
        for item in responseJSON:
            if 'meta' in item and 'stems' in item['meta']:
                for metaStem in item['meta']['stems']:
                    if len(metaStem) > 3:
                        keyword_stems.add(metaStem)
            else:
                if len(item) > 3:
                    keyword_stems.add(item)
        # definition = str(responseJSON[0]['shortdef']).split()
        #for word in definition:
        #    if len(word) > 3:
        #       keyword_definition.add(word)
    print("Keyword Stems:")
    print(keyword_stems)
    return(keyword_stems)
    # print("Keyword Definition:")
    # print(keyword_definition)

def score_word():
    return

#
# if __name__ == '__main__':
#     keyword_input = input("What is the keywords?")
#     text_input = input("What is the text?")
#     algorithm(text_input, keyword_input)
