import pytest

from dataframe_pcg.dataframe import Dataframe


# TEST_CASE_2
def test_count_nulls_counts_nulls():
    data = {"a": [1, None, 3], "b": [None, None, "x"]}
    dtype = {"a": "int", "b": "str"}

    df = Dataframe(data, dtype)
    result = df.count_nulls()

    assert result == {"a": 1, "b": 2}


# TEST_CASE_3
def test_describe_numeric_and_categorical(monkeypatch):
    data = {"a": [1, 2, 3], "b": ["x", None, "y"]}
    dtype = {"a": "int", "b": "str"}

    def fake_get_col_max(values):
        non_none = [v for v in values if v is not None]
        return max(non_none) if non_none else None

    def fake_get_col_min(values):
        non_none = [v for v in values if v is not None]
        return min(non_none) if non_none else None

    def fake_get_col_mean(values):
        non_none = [v for v in values if v is not None]
        return sum(non_none) / len(non_none) if non_none else None

    def fake_get_col_median(values):
        non_none = sorted([v for v in values if v is not None])
        if not non_none:
            return None
        n = len(non_none)
        mid = n // 2
        if n % 2 == 1:
            return non_none[mid]
        else:
            return (non_none[mid - 1] + non_none[mid]) / 2

    def fake_get_col_mode(values):
        non_none = [v for v in values if v is not None]
        if not non_none:
            return None
        first = non_none[0]
        if isinstance(first, (int, float)):
            return "mode_num"
        else:
            return "mode_cat"

    def fake_write_file(path, description):
        # We'll handle capturing via monkeypatch in test by inspecting passed description
        fake_write_file.last_path = path
        fake_write_file.last_description = description

    monkeypatch.setattr("dataframe_pcg.dataframe.get_col_max", fake_get_col_max)
    monkeypatch.setattr("dataframe_pcg.dataframe.get_col_min", fake_get_col_min)
    monkeypatch.setattr("dataframe_pcg.dataframe.get_col_mean", fake_get_col_mean)
    monkeypatch.setattr("dataframe_pcg.dataframe.get_col_median", fake_get_col_median)
    monkeypatch.setattr("dataframe_pcg.dataframe.get_col_mode", fake_get_col_mode)
    monkeypatch.setattr("dataframe_pcg.dataframe.write_file", fake_write_file)

    df = Dataframe(data, dtype)
    df.describe(path="out.csv")

    last_path = getattr(fake_write_file, "last_path", None)
    last_description = getattr(fake_write_file, "last_description", None)

    assert last_path == "out.csv"
    expected = {
        "column": ["a", "b"],
        "nulls": [0, 1],
        "max": [3, None],
        "min": [1, None],
        "mean": [2.0, None],
        "median": [2, None],
        "mode": ["mode_num", "mode_cat"],
    }

    assert last_description is not None
    assert last_description["column"] == expected["column"]
    assert last_description["nulls"] == expected["nulls"]
    assert last_description["max"] == expected["max"]
    assert last_description["min"] == expected["min"]
    assert last_description["median"] == expected["median"]
    assert last_description["mode"] == expected["mode"]
    assert last_description["mean"][0] == pytest.approx(2.0)
    assert last_description["mean"][1] is None


# TEST_CASE_5
def test_fillna_none_strategies_no_op():
    data = {"a": [1, None], "b": ["x", None]}
    dtype = {"a": "int", "b": "str"}

    df = Dataframe(data, dtype)
    df.fillna(None, None)

    assert df.data == data


# TEST_CASE_7
def test_read_csv_raises_on_bad_dtype(monkeypatch):
    data = {"col": [1, 2]}
    dtype = {"col": "int"}

    def raise_read_dtype(_):
        raise ValueError("bad dtype")

    monkeypatch.setattr("dataframe_pcg.dataframe.read_dtype", raise_read_dtype)

    with pytest.raises(ValueError):
        Dataframe.read_csv(data, dtype)
