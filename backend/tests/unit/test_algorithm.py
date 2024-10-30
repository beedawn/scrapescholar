import pytest
import algorithm.algorithm as algorithm


@pytest.fixture(autouse=True)
def word_list(tmpdir):
    list_of_words = ["test", "test2", "pizza"]
    yield list_of_words


def test_get_score():
    score = algorithm.calc_score(5, ["word", "word2"])

    assert (score == 500.0)


def test_check_limit(word_list):
    score = algorithm.check_limit("test", word_list)

    assert (word_list == ["test", "test2", "pizza"])


def test_break_into_possible_words_has_word(word_list):
    algorithm.break_word_into_possible_words("test", word_list)

    assert (word_list == ["test", "test2", "pizza"])


def test_break_into_possible_words_new_word(word_list):
    algorithm.break_word_into_possible_words("lunch", word_list)
    assert (word_list == ["test", "test2", "pizza", "lunch", "lunc", "unch"])


def test_get_five_words_char(word_list):
    score = algorithm.get_words_five_char(word_list)
    assert (score == 2)


def test_calc_score(word_list):
    score = algorithm.calc_score(5, word_list)
    assert (score == 250.0)





def test_flatten_list(word_list):
    new_word_list = []
    for word in word_list:
        new_word = [word]
        new_word_list.append(new_word)
    flattened_word_list = algorithm.flatten_list(new_word_list)
    assert (flattened_word_list == word_list)
