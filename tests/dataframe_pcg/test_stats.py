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
    assert get_col_max([1, None, 5, -3]) == 5


# TEST_CASE_2
def test_get_col_max_all_none():
    assert get_col_max([None, None]) is None


# TEST_CASE_3
def test_get_col_min_basic():
    assert get_col_min([4, None, -2, 7]) == -2


# TEST_CASE_4
def test_get_col_mean_basic():
    assert get_col_mean([1, 2, None, 3]) == pytest.approx(2.0)


# TEST_CASE_5
def test_get_col_mean_all_none():
    assert get_col_mean([]) is None


# TEST_CASE_6
def test_get_col_median_odd():
    assert get_col_median([3, 1, 2]) == 2


# TEST_CASE_7
def test_get_col_median_even_raises():
    with pytest.raises(IndexError):
        get_col_median([1, 2])


# TEST_CASE_9
def test_get_col_mode_basic():
    assert get_col_mode([1, 1, 2, 3, 3]) == 1


# TEST_CASE_10
def test_get_stat_basic_numeric_only():
    data = {"a": [1, 2, None], "b": [4, None, 5], "c": ["x", "y", "z"]}
    dtypes = {"a": "int", "b": "float", "c": "string"}
    result = get_stat(data, dtypes, get_col_mean)
    assert result["a"] == pytest.approx(1.5)
    assert result["b"] == pytest.approx(4.5)
