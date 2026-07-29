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
    assert get_col_max([3, None, 7, 5]) == 7


# TEST_CASE_2
def test_get_col_max_all_none():
    assert get_col_max([None, None]) is None


# TEST_CASE_3
def test_get_col_min_basic():
    assert get_col_min([3, None, 7, 5]) == 3


# TEST_CASE_4
def test_get_col_min_booleans():
    assert get_col_min([True, False, 1]) is False


# TEST_CASE_5
def test_get_col_mean_basic():
    assert get_col_mean([1, 2, 3]) == pytest.approx(2.0)


# TEST_CASE_6
def test_get_col_mean_all_none_returns_none():
    assert get_col_mean([None, None]) is None


# TEST_CASE_7
def test_get_col_median_empty_returns_none():
    assert get_col_median([]) is None


# TEST_CASE_8
def test_get_col_median_odd():
    assert get_col_median([3, 1, 2]) == 2


# TEST_CASE_9
def test_get_col_median_even_buggy():
    assert get_col_median([1, 2, 3, 4]) == 3.5


# TEST_CASE_10
def test_get_col_mode_basic():
    assert get_col_mode([1, 2, 2, 3, 2]) == 2


# TEST_CASE_11
def test_get_col_mode_tie_first_encountered():
    assert get_col_mode([1, 1, 2, 2]) == 1


# TEST_CASE_12
def test_get_stat_applies_to_numeric_only():
    data = {"a": [1, 2, 3], "b": ["x", "y", "z"], "c": [1.5, 2.5]}
    dtypes = {"a": "int", "b": "string", "c": "float"}
    res = get_stat(data, dtypes, get_col_mean)
    assert res.get("a") == pytest.approx(2.0)
    assert res.get("c") == pytest.approx(2.0)
    assert "b" not in res
