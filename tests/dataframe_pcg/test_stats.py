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
    assert get_col_max([1, None, 5, -2, 3]) == 5


# TEST_CASE_2
def test_get_col_max_empty():
    assert get_col_max([]) is None


# TEST_CASE_3
def test_get_col_min_basic():
    assert get_col_min([3, None, 0, -5, 10]) == -5


# TEST_CASE_4
def test_get_col_min_empty():
    assert get_col_min([]) is None


# TEST_CASE_5
def test_get_col_mean_basic():
    assert get_col_mean([1, 2, 3, None]) == pytest.approx(2.0)


# TEST_CASE_6
def test_get_col_mean_empty():
    assert get_col_mean([]) is None


# TEST_CASE_7
def test_get_col_median_odd():
    assert get_col_median([3, 1, 2]) == 2


# TEST_CASE_8
def test_get_col_median_even_2_raises():
    with pytest.raises(IndexError):
        get_col_median([1, 2])


# TEST_CASE_9
def test_get_col_median_even_4():
    # This follows the buggy implementation: for [1,2,3,4], returns (3+4)/2 = 3.5
    assert get_col_median([1, 2, 3, 4]) == pytest.approx(3.5)


# TEST_CASE_10
def test_get_col_mode_basic():
    assert get_col_mode([1, 2, 2, 3, 3, 3, None]) == 3


# TEST_CASE_11
def test_get_col_mode_tie_first_encountered():
    # Tie between 1 and 2, first encountered is 1
    assert get_col_mode([1, 1, 2, 2]) == 1


# TEST_CASE_12
def test_get_stat_applies_to_numeric_columns():
    data = {"a": [1, 2, 3], "b": [1.0, 2.0], "c": ["x", "y"]}
    dtypes = {"a": "int", "b": "float", "c": "string"}
    result = get_stat(data, dtypes, get_col_mean)
    assert "a" in result and "b" in result
    assert "c" not in result
    assert result["a"] == pytest.approx(2.0)
    assert result["b"] == pytest.approx(1.5)
