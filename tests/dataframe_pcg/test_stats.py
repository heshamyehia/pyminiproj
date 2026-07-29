import pytest

from dataframe_pcg.stats import (
    get_col_max,
    get_col_mean,
    get_col_median,
    get_col_min,
    get_col_mode,
    get_stat,
)


# TEST_CASE_1
def test_get_col_max_ignores_none_and_handles_negative_values():
    assert get_col_max([None, -5, -2, None, -9]) == -2


# TEST_CASE_2
def test_get_col_max_returns_none_without_non_none_values_and_rejects_mixed_types():
    assert get_col_max([None, None]) is None
    with pytest.raises(TypeError):
        get_col_max([1, "2"])


# TEST_CASE_3
def test_get_col_min_ignores_none_and_uses_numeric_boolean_comparison():
    result = get_col_min([None, True, 2, False])
    assert result is False


# TEST_CASE_4
def test_get_col_min_returns_none_without_values_and_rejects_non_iterable_input():
    assert get_col_min([]) is None
    with pytest.raises(TypeError):
        get_col_min(3)


# TEST_CASE_5
def test_get_col_mean_ignores_none_and_returns_float():
    result = get_col_mean([0.1, None, 0.2])
    assert isinstance(result, float)
    assert result == pytest.approx(0.15)


# TEST_CASE_6
def test_get_col_mean_returns_none_without_values_and_rejects_non_addable_values():
    assert get_col_mean([None, None]) is None
    with pytest.raises(TypeError):
        get_col_mean([1, "2"])


# TEST_CASE_7
def test_get_col_median_covers_empty_and_odd_length_paths():
    assert get_col_median([None, None]) is None
    assert get_col_median([3, None, 1, 2]) == 2


# TEST_CASE_8
def test_get_col_median_even_length_uses_right_of_center_indices():
    result = get_col_median([4, 1, 3, 2])
    assert isinstance(result, float)
    assert result == pytest.approx(3.5)


# TEST_CASE_9
def test_get_col_median_two_values_raises_index_error():
    with pytest.raises(IndexError):
        get_col_median([1, 2])


# TEST_CASE_10
def test_get_col_mode_ignores_none_and_keeps_first_key_when_frequencies_tie():
    assert get_col_mode([None, 2, 1, 1, 2]) == 2
    assert get_col_mode([None, None]) is None


# TEST_CASE_11
def test_get_col_mode_merges_equal_boolean_and_integer_keys_and_rejects_unhashable_values():
    result = get_col_mode([True, 1, False, 0])
    assert result is True
    with pytest.raises(TypeError):
        get_col_mode([[1], [1]])


# TEST_CASE_12
def test_get_stat_processes_only_exact_numeric_dtype_strings_and_propagates_callback_errors():
    data = {
        "age": [10, 20],
        "score": [1.5, 2.5],
        "name": ["a", "b"],
        "wrong_case": [100],
        "missing_dtype": [200],
    }
    dtypes = {
        "age": "int",
        "score": "float",
        "name": "string",
        "wrong_case": "Int",
        "extra": "int",
    }

    result = get_stat(data, dtypes, get_col_mean)

    assert set(result) == {"age", "score"}
    assert isinstance(result["age"], float)
    assert result["age"] == pytest.approx(15.0)
    assert isinstance(result["score"], float)
    assert result["score"] == pytest.approx(2.0)

    with pytest.raises(TypeError):
        get_stat({"age": [10]}, {"age": "int"}, None)
