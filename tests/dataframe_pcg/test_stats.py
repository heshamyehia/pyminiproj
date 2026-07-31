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
def test_get_col_max_behaviour():
    assert get_col_max([None, None]) is None
    assert get_col_max([None, 5, -2, 3.5, 5]) == 5
    assert get_col_max([1, -1, 1.5]) == 1.5
    with pytest.raises(TypeError):
        get_col_max([1, "2", 3])


# TEST_CASE_2
def test_get_col_min_behaviour():
    assert get_col_min([3, 1, 4]) == 1
    assert get_col_min([None, -5, 0]) == -5
    with pytest.raises(TypeError):
        get_col_min([1, "0", -1])


# TEST_CASE_3
def test_get_col_mean_behaviour():
    assert get_col_mean([1, 2, 3]) == pytest.approx(2.0)
    assert get_col_mean([1, None, 2]) == pytest.approx(1.5)
    with pytest.raises(TypeError):
        get_col_mean([1, "a"])


# TEST_CASE_4
def test_get_col_median_behaviour():
    assert get_col_median([3, 1, 2]) == 2
    assert get_col_median([1, 2, 3, 4]) == pytest.approx(3.5)
    assert get_col_median([]) is None


# TEST_CASE_5
def test_get_col_mode_behaviour():
    assert get_col_mode([]) is None
    assert get_col_mode([1, 1, 2, 2]) == 1
    assert get_col_mode([1, None, 1, None, 2]) == 1
    with pytest.raises(TypeError):
        get_col_mode([[1], [1]])


# TEST_CASE_6
def test_get_stat_behaviour():
    data = {"a": [1, 2, 3], "b": [1, None]}
    dtypes = {"a": "int", "b": "int"}
    assert get_stat(data, dtypes, get_col_max) == {"a": 3, "b": 1}

    data2 = {"a": [1, 2], "b": ["x", "y"]}
    dtypes2 = {"a": "int", "b": "string"}
    assert get_stat(data2, dtypes2, get_col_min) == {"a": 1}
