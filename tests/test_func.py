from fix_func.func import get_first_matching_object, word_statistics


def test_empty_iterable_returns_none():
    assert get_first_matching_object(lambda x: True, []) is None


def test_no_match_returns_none():
    assert get_first_matching_object(lambda x: x > 10, [1, 2, 3]) is None


def test_returns_first_matching_with_list():
    data = [1, 3, 4, 8]
    assert get_first_matching_object(lambda x: x % 2 == 0, data) == 4


def test_works_with_generator_iterable():
    gen = (i for i in range(5))
    assert get_first_matching_object(lambda x: x >= 3, gen) == 3


def test_works_with_tuple_and_custom_predicate():
    data = ("apple", "banana", "pear")
    assert get_first_matching_object(lambda s: s.startswith("b"), data) == "banana"


def test_empty_input_returns_empty_dict():
    assert word_statistics([]) == {}


def test_case_insensitive_and_repeats():
    lines = ["Hello hello HeLLo"]
    assert word_statistics(lines) == {"hello": 3}


def test_punctuation_and_multiline():
    lines = [
        "Python, is great. Python is fun!",
        "Fun with python; PYTHON."
    ]
    expected = {"python": 4, "fun": 2, "is": 2, "great": 1, "with": 1}
    assert word_statistics(lines) == expected


def test_tie_breaks_by_word_asc():
    lines = ["apple banana", "banana apple"]
    assert word_statistics(lines) == {"apple": 2, "banana": 2}


def test_mixed_words_counts_and_order():
    lines = ["Dog, cat. Dog!", "cat dog mouse."]
    assert word_statistics(lines) == {"dog": 3, "cat": 2, "mouse": 1}


def test_large_input_stress_but_fast():
    lines = ["alpha beta alpha"] * 10_000
    result = word_statistics(lines)
    assert result == {"alpha": 20_000, "beta": 10_000}
