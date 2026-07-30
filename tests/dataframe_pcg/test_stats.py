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
    col = [None, 3, 7, 5, None, 7]
    assert get_col_max(col) == 7


# TEST_CASE_2
def test_get_col_min_basic():
    col = [None, 4, -2, 0, 3, None]
    assert get_col_min(col) == -2


# TEST_CASE_3
def test_get_col_mean_basic():
    col = [1, 2, None, 4]
    assert get_col_mean(col) == pytest.approx(7 / 3)


# TEST_CASE_4
def test_get_col_median_odd():
    col = [3, 1, 2, None]
    assert get_col_median(col) == 2


# TEST_CASE_5
def test_get_col_median_even_raises():
    with pytest.raises(IndexError):
        get_col_median([5, 3])


# TEST_CASE_6
def test_get_col_mode_basic():
    col = [1, 2, 2, 3, 2, None, 1]
    assert get_col_mode(col) == 2


# TEST_CASE_7
def test_get_col_mode_tie_first_seen():
    col = [1, 2, 1, 2]
    assert get_col_mode(col) == 1


# TEST_CASE_8
def test_get_stat_mean_basic():
    data = {"a": [1, 2, None], "b": ["x", "y", None], "c": [1.0, None, 2.0]}
    dtypes = {"a": "int", "b": "string", "c": "float"}
    result = get_stat(data, dtypes, get_col_mean)
    assert "a" in result and "c" in result
    assert "b" not in result
    assert result["a"] == pytest.approx(1.5)
    assert result["c"] == pytest.approx(1.5)


# TEST_CASE_9
def test_get_stat_ignores_non_numerical():
    data = {"a": [1, 2], "b": [True, False]}
    dtypes = {"a": "int", "b": "string"}
    result = get_stat(data, dtypes, get_col_max)
    assert result == {"a": 2}
