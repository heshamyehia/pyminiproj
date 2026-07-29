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
    assert get_col_max([1, 2, 3]) == 3


# TEST_CASE_2
def test_get_col_max_type_error():
    with pytest.raises(TypeError):
        get_col_max([1, "a"])


# TEST_CASE_3
def test_get_col_min_basic():
    assert get_col_min([1, 2, 3]) == 1


# TEST_CASE_4
def test_get_col_min_type_error():
    with pytest.raises(TypeError):
        get_col_min([1, "a"])


# TEST_CASE_5
def test_get_col_mean_basic():
    assert get_col_mean([1, 2, 3]) == pytest.approx(2.0)


# TEST_CASE_6
def test_get_col_mean_type_error():
    with pytest.raises(TypeError):
        get_col_mean([1, "a"])


# TEST_CASE_7
def test_get_col_median_odd():
    assert get_col_median([1, 2, 3]) == 2


# TEST_CASE_8
def test_get_col_median_two_error():
    with pytest.raises(IndexError):
        get_col_median([1, 3])


# TEST_CASE_9
def test_get_col_mode_empty():
    assert get_col_mode([]) is None


# TEST_CASE_10
def test_get_col_mode_basic():
    assert get_col_mode([1, 2, 2, 3, 3]) == 2


# TEST_CASE_11
def test_get_stat_basic():
    data = {"a": [1, 2], "b": [1.0, 2.0], "c": ["x", "y"]}
    dtypes = {"a": "int", "b": "float", "c": "string"}
    result = get_stat(data, dtypes, get_col_mean)
    assert result == {"a": pytest.approx(1.5), "b": pytest.approx(1.5)}


# TEST_CASE_12
def test_get_stat_skip_non_numeric():
    data = {"x": [4, 6], "y": ["a", "b"]}
    dtypes = {"x": "int", "y": "string"}
    result = get_stat(data, dtypes, get_col_mean)
    assert result == {"x": pytest.approx(5.0)}
