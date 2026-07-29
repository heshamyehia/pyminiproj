import pytest

from dataframe_pcg.stats import (
    get_col_max,
    get_col_mean,
    get_col_median,
    get_col_min,
    get_col_mode,
)


# TEST_CASE_1
def test_get_col_max_typical():
    assert get_col_max([1, None, 3, 2]) == 3


# TEST_CASE_2
def test_get_col_max_empty():
    assert get_col_max([]) is None


# TEST_CASE_4
def test_get_col_min_typical():
    assert get_col_min([4, None, 2, 7]) == 2


# TEST_CASE_5
def test_get_col_min_empty():
    assert get_col_min([]) is None


# TEST_CASE_6
def test_get_col_mean_basic():
    assert get_col_mean([1, 2, 3]) == pytest.approx(2.0)


# TEST_CASE_7
def test_get_col_mean_with_none():
    assert get_col_mean([1.5, None, 2.5]) == pytest.approx(2.0)


# TEST_CASE_8
def test_get_col_median_odd():
    assert get_col_median([1, 3, 2]) == 2


# TEST_CASE_9
def test_get_col_median_even():
    assert get_col_median([1, 2, 3, 4]) == pytest.approx(3.5)


# TEST_CASE_10
def test_get_col_mode_basic():
    assert get_col_mode([1, 2, 2, 3, None, 2]) == 2


# TEST_CASE_11
def test_get_col_mode_tie_breaker():
    assert get_col_mode([1, 1, 2, 2]) == 1
