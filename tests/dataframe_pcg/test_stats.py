import math

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
    assert get_col_max([1, 3, None, 2]) == 3


# TEST_CASE_2
def test_get_col_max_none_only():
    assert get_col_max([None, None]) is None


# TEST_CASE_3
def test_get_col_max_nan():
    res = get_col_max([float("nan")])
    assert math.isnan(res)


# TEST_CASE_4
def test_get_col_min_basic():
    assert get_col_min([-2, -5, 0]) == -5


# TEST_CASE_5
def test_get_col_min_none_only():
    assert get_col_min([None, None]) is None


# TEST_CASE_6
def test_get_col_mean_basic():
    assert get_col_mean([1, 2, 3]) == pytest.approx(2.0)


# TEST_CASE_7
def test_get_col_mean_none_only():
    assert get_col_mean([None, None]) is None


# TEST_CASE_8
def test_get_col_median_odd():
    assert get_col_median([1, 3, 2]) == 2


# TEST_CASE_10
def test_get_col_median_even_four_elements():
    assert get_col_median([1, 2, 3, 4]) == pytest.approx(3.5)


# TEST_CASE_11
def test_get_col_mode_basic_and_tie():
    # In [1,1,2,2], both 1 and 2 have freq 2; first encountered (1) should be returned
    assert get_col_mode([1, 1, 2, 2]) == 1


# TEST_CASE_12
def test_get_stat_applies_function_mean():
    data = {"a": [1, 2, 3], "b": [1.0, 2.0]}
    dtypes = {"a": "int", "b": "float"}
    result = get_stat(data, dtypes, get_col_mean)
    assert result["a"] == pytest.approx(2.0)
    assert result["b"] == pytest.approx(1.5)
