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
    assert get_col_max([1, None, 5, 3]) == 5


# TEST_CASE_2
def test_get_col_max_nan_behavior():
    col = [float("nan"), 2.0, None]
    res = get_col_max(col)
    assert isinstance(res, float)
    assert math.isnan(res)


# TEST_CASE_3
def test_get_col_min_basic():
    assert get_col_min([1, None, -3, 0]) == -3


# TEST_CASE_4
def test_get_col_min_nan_behavior():
    col = [float("nan")]
    res = get_col_min(col)
    assert isinstance(res, float)
    assert math.isnan(res)


# TEST_CASE_5
def test_get_col_mean_basic():
    assert get_col_mean([1, None, 3]) == pytest.approx(2.0)


# TEST_CASE_6
def test_get_col_mean_all_none():
    assert get_col_mean([None, None]) is None


# TEST_CASE_7
def test_get_col_median_odd():
    assert get_col_median([3, 1, 2]) == 2


# TEST_CASE_8
def test_get_col_median_even():
    assert get_col_median([1, 2, 3, 4]) == pytest.approx(3.5)


# TEST_CASE_10
def test_get_col_mode_basic_and_none():
    assert get_col_mode([1, 2, 2, 3, None]) == 2
    assert get_col_mode([None, None]) is None


# TEST_CASE_11
def test_get_stat_basic():
    data = {"a": [1, 2], "b": [3, 4]}
    dtypes = {"a": "int", "b": "string"}
    result = get_stat(data, dtypes, get_col_mean)
    assert result == {"a": pytest.approx(1.5)}


# TEST_CASE_12
def test_get_stat_skips_non_numeric():
    data = {"a": [1, 2], "b": [1, 2]}
    dtypes = {"a": "int", "b": "string"}
    result = get_stat(data, dtypes, get_col_max)
    assert result == {"a": 2}
