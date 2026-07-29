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
def test_get_col_max_normal():
    assert get_col_max([1, None, 5, 3]) == 5


# TEST_CASE_2
def test_get_col_max_all_none():
    assert get_col_max([None, None]) is None


# TEST_CASE_3
def test_get_col_min_normal():
    assert get_col_min([5, None, 1, 3]) == 1


# TEST_CASE_4
def test_get_col_min_all_none():
    assert get_col_min([None, None]) is None


# TEST_CASE_5
def test_get_col_mean_normal():
    assert get_col_mean([1, 2, 3]) == pytest.approx(2.0)


# TEST_CASE_6
def test_get_col_mean_with_none_and_float():
    assert get_col_mean([1, None, 2.5]) == pytest.approx(1.75)


# TEST_CASE_7
def test_get_col_median_odd():
    assert get_col_median([3, 1, 2]) == pytest.approx(2.0)


# TEST_CASE_8
def test_get_col_median_even_buggy():
    assert get_col_median([1, 2, 3, 4]) == pytest.approx(3.5)


# TEST_CASE_9
def test_get_col_mode_basic():
    assert get_col_mode([1, 2, 2, 3, 3, 3]) == 3


# TEST_CASE_11
def test_get_stat_empty_data():
    assert get_stat({}, {}, get_col_max) == {}


# TEST_CASE_12
def test_get_stat_multiple_numerical_columns_mean():
    data = {"a": [1.0, 3.0], "b": [2, 4]}
    dtypes = {"a": "float", "b": "int"}
    result = get_stat(data, dtypes, get_col_mean)
    assert "a" in result and "b" in result
    assert result["a"] == pytest.approx(2.0)
    assert result["b"] == pytest.approx(3.0)
