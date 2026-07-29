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
    assert get_col_max([None, 5, 3, None, 7]) == 7


# TEST_CASE_2
def test_get_col_max_none_and_empty():
    assert get_col_max([]) is None
    assert get_col_max([None, None]) is None


# TEST_CASE_3
def test_get_col_min_basic():
    assert get_col_min([None, 3, -2, 5]) == -2


# TEST_CASE_4
def test_get_col_mean_basic():
    assert get_col_mean([1, 2, 3]) == pytest.approx(2.0)


# TEST_CASE_5
def test_get_col_mean_all_none():
    assert get_col_mean([None, None]) is None


# TEST_CASE_6
def test_get_col_median_odd():
    assert get_col_median([1, 3, 2]) == 2


# TEST_CASE_7
def test_get_col_median_even_buggy():
    assert get_col_median([1, 2, 3, 4]) == pytest.approx(3.5)


# TEST_CASE_8
def test_get_col_mode_basic():
    assert get_col_mode([1, 2, 2, 3, 3]) == 2


# TEST_CASE_9
def test_get_stat_basic():
    data = {"a": [1, 2, None], "b": ["x", "y", None]}
    dtypes = {"a": "int", "b": "string"}
    res = get_stat(data, dtypes, get_col_mean)
    assert "a" in res and res["a"] == pytest.approx(1.5)
    assert "b" not in res


# TEST_CASE_10
def test_get_stat_skips_non_numeric():
    data = {"a": [1, 2], "b": [3, 4]}
    dtypes = {"a": "int", "b": "string"}
    res = get_stat(data, dtypes, get_col_min)
    assert res == {"a": 1}


# TEST_CASE_11
def test_get_col_max_type_error_path():
    with pytest.raises(TypeError):
        get_col_max([1, "2", 3])


# TEST_CASE_12
def test_get_col_mean_type_error_path():
    with pytest.raises(TypeError):
        get_col_mean([1, "2", 3])
