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
def test_get_col_max_basic():
    assert get_col_max([1, 3, 2, None, 5]) == 5


# TEST_CASE_2
def test_get_col_max_all_none():
    assert get_col_max([None, None]) is None


# TEST_CASE_3
def test_get_col_min_basic():
    assert get_col_min([3, 1, 4, None, -2]) == -2


# TEST_CASE_4
def test_get_col_min_all_none():
    assert get_col_min([None, None]) is None


# TEST_CASE_5
def test_get_col_mean_basic():
    assert get_col_mean([1, 2, 3]) == pytest.approx(2.0)


# TEST_CASE_6
def test_get_col_mean_with_none():
    assert get_col_mean([None, 5]) == pytest.approx(5.0)


# TEST_CASE_7
def test_get_col_median_odd():
    assert get_col_median([3, 1, 2]) == 2


# TEST_CASE_8
def test_get_col_median_even_case():
    assert get_col_median([3, 1, 2, 4]) == pytest.approx(3.5)


# TEST_CASE_9
def test_get_col_mode_basic():
    assert get_col_mode([1, 2, 2, 3, 3]) == 2


# TEST_CASE_10
def test_get_col_mode_none():
    assert get_col_mode([None, None]) is None


# TEST_CASE_11
def test_get_stat_basic():
    data = {"a": [1, 2, 3], "b": ["x", "y"]}
    dtypes = {"a": "int", "b": "string"}
    result = get_stat(data, dtypes, lambda vals: get_col_mean(vals))
    assert result == {"a": pytest.approx(2.0)}


# TEST_CASE_12
def test_get_stat_none():
    data = {"a": ["x", "y"]}
    dtypes = {"a": "string"}
    result = get_stat(data, dtypes, get_col_max)
    assert result == {}
