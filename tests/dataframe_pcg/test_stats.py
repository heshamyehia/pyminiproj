import pytest

from dataframe_pcg.stats import (
    get_col_max,
    get_col_mean,
    get_col_median,
    get_col_min,
    get_col_mode,
    get_stat,
)


# TEST_CASE_2
def test_get_col_max_normal():
    assert get_col_max([None, 2, 5, None, 3]) == 5


# TEST_CASE_3
def test_get_col_min_basic():
    assert get_col_min([5, None, 3, 9]) == 3


# TEST_CASE_5
def test_get_col_mean_all_none():
    assert get_col_mean([None, None]) is None


# TEST_CASE_7
def test_get_col_median_even():
    assert get_col_median([1, 2, 3, 4]) == pytest.approx(3.5)


# TEST_CASE_8
def test_get_col_mode_basic():
    assert get_col_mode([1, 1, 2, 3]) == 1


# TEST_CASE_9
def test_get_col_mode_none():
    assert get_col_mode([None, None]) is None


# TEST_CASE_10
def test_get_stat_applies_function():
    data = {"a": [1, 2, 3], "b": [1.0, None, 3.0], "c": ["x", "y"]}
    dtypes = {"a": "int", "b": "float", "c": "string"}
    result = get_stat(data, dtypes, get_col_max)
    assert result == {"a": 3, "b": 3.0}


# TEST_CASE_11
def test_get_col_max_type_error_in_mixed():
    with pytest.raises(TypeError):
        get_col_max([1, "a", 2])
