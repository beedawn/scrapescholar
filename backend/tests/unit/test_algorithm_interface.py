import pytest
import algorithm.algorithm_interface as algorithm_interface


@pytest.fixture(autouse=True)
def word_set(tmpdir):
    set_of_words = {"test", "test2", "pizza"}
    yield set_of_words


def test_algorithm(word_set):
    score = algorithm_interface.algorithm_interface("hello","hello")
    assert score == 100


def test_algorithm_abstract(word_set):
    score = algorithm_interface.algorithm_interface("hello","hello","hello")
    assert score == 100