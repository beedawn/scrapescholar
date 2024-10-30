import pytest
import algorithm.algorithm as algorithm


@pytest.fixture(autouse=True)
def word_set(tmpdir):
    set_of_words = {"test", "test2", "pizza"}
    yield set_of_words


def test_get_score():
    score = algorithm.calc_score(5, ["word", "word2"])

    assert (score == 500.0)


def test_check_limit(word_set):
    score = algorithm.check_limit("test", word_set)

    assert (word_set == {"test", "test2", "pizza"})


def test_break_into_possible_words_has_word(word_set):
    algorithm.break_word_into_possible_words("test", word_set)

    assert (word_set == {"test", "test2", "pizza"})


def test_break_into_possible_words_new_word(word_set):
    algorithm.break_word_into_possible_words("lunch", word_set)
    assert (word_set == {"test", "test2", "pizza", "lunch", "lunc", "unch"})


def test_get_five_words_char(word_set):
    score = algorithm.get_words_five_char(word_set)
    assert (score == 2)


def test_calc_score(word_set):
    score = algorithm.calc_score(5, word_set)
    assert (score == 250.0)


def test_calc_score(word_set):
    score = algorithm.calc_score(5, {"hi"})
    assert (score == 500.0)


def test_score_word(word_set):
    score = algorithm.score_word("hi", {"hi"}, {"hi"}, {"hi"})
    assert (score == 2.25)


def test_score_word_in_word(word_set):
    score = algorithm.score_word("hi", {"him"}, {"hi"}, {"hi"})
    assert (score == 2.0)

def test_api_request(word_set):
    synonyms = algorithm.api_request("hi")
    assert isinstance(synonyms, set)

def test_api_request_jibberish(word_set):
    synonyms = algorithm.api_request("gfgjfgfj")
    assert isinstance(synonyms, set)

def test_flatten_list(word_set):
    flat_list = algorithm.flatten_list([["hi"],["hey"]])
    assert flat_list == ["hi","hey"]


def test_algorithm(word_set):
    score = algorithm.algorithm("hello","hello")
    assert score == 325