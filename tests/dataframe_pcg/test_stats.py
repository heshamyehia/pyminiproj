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
def test_get_col_max_behaviors():
    assert get_col_max([3, -2, 7, None]) == -2
    assert get_col_max([3, 5]) == 3
    assert get_col_max([]) is None
    assert get_col_max([None, None]) is None
    assert get_col_max([10]) == 10


# TEST_CASE_2
def test_get_col_min_behaviors():
    assert get_col_min([3, -2, 7, None]) == -2
    assert get_col_min([3, 5]) == 3
    assert get_col_min([]) is None
    assert get_col_min([None, None]) is None
    assert get_col_min([4]) == 4


# TEST_CASE_3
def test_get_col_mean_behaviors():
    assert get_col_mean([1, 2, None, 3]) == pytest.approx(2.0)
    assert get_col_mean([5]) == pytest.approx(5.0)
    assert get_col_mean([]) is None
    assert get_col_mean([None, None]) is None


# TEST_CASE_4
def test_get_col_median_behaviors():
    assert get_col_median([3, 1, 2]) == 2
    assert get_col_median([1, 2, 3, 4]) == pytest.approx(3.5)
    with pytest.raises(IndexError):
        get_col_median([1, 2])


# TEST_CASE_5
def test_get_col_mode_behaviors():
    assert get_col_mode([1, 2, 2, 3, None, 3, 3]) == 3
    assert get_col_mode([1, 1, 2, 2, None]) == 1
    assert get_col_mode([None, None]) is None


# TEST_CASE_6
def test_get_stat_behaviors():
    data = {"a": [1, 2, 3], "b": [1.0, 2.0], "c": ["x", "y"], "d": []}
    dtypes = {"a": "int", "b": "float", "c": "string", "d": "int"}
    res = get_stat(data, dtypes, get_col_mean)
    assert res["a"] == pytest.approx(2.0)
    assert res["b"] == pytest.approx(1.5)
    assert res.get("d", None) is None
    assert "c" not in res
