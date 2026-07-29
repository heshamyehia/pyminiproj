import pytest

import dataframe_pcg.dataframe as df_module
from dataframe_pcg.dataframe import Dataframe


# TEST_CASE_1
def test_count_nulls_basic():
    data = {"A": [1, None, 3], "B": [None, None, 2]}
    dtype = {"A": "int", "B": "int"}
    df = Dataframe(data, dtype)
    assert df.count_nulls() == {"A": 1, "B": 2}


# TEST_CASE_2
def test_describe_with_monkeypatched_stats(monkeypatch):
    data = {"A": [1, 2, 3], "B": ["x", "x", "y"]}
    dtype = {"A": "int", "B": "str"}

    def mock_max(vals):
        non_none = [v for v in vals if v is not None]
        return max(non_none) if non_none else None

    def mock_min(vals):
        non_none = [v for v in vals if v is not None]
        return min(non_none) if non_none else None

    def mock_mean(vals):
        non_none = [v for v in vals if v is not None]
        return sum(non_none) / len(non_none) if non_none else None

    def mock_median(vals):
        non_none = sorted([v for v in vals if v is not None])
        n = len(non_none)
        if n == 0:
            return None
        mid = n // 2
        if n % 2 == 1:
            return non_none[mid]
        else:
            return (non_none[mid - 1] + non_none[mid]) / 2

    def mock_mode(vals):
        from collections import Counter

        non_none = [v for v in vals if v is not None]
        if not non_none:
            return None
        c = Counter(non_none)
        maxfreq = max(c.values())
        modes = [k for k, v in c.items() if v == maxfreq]
        return min(modes)

    captured = {}

    def mock_write(path, desc):
        captured["path"] = path
        captured["desc"] = desc

    monkeypatch.setattr(df_module, "get_col_max", mock_max)
    monkeypatch.setattr(df_module, "get_col_min", mock_min)
    monkeypatch.setattr(df_module, "get_col_mean", mock_mean)
    monkeypatch.setattr(df_module, "get_col_median", mock_median)
    monkeypatch.setattr(df_module, "get_col_mode", mock_mode)
    monkeypatch.setattr(df_module, "write_file", mock_write)

    df = Dataframe(data, dtype)
    df.describe(path="out/describe.csv")

    assert captured["path"] == "out/describe.csv"
    desc = captured["desc"]

    assert desc["column"] == ["A", "B"]
    assert desc["nulls"] == [0, 0]
    assert desc["max"] == [3, None]
    assert desc["min"] == [1, None]
    assert desc["mean"][0] == pytest.approx(2.0)
    assert desc["mean"][1] is None
    assert desc["median"][0] == pytest.approx(2.0)
    assert desc["median"][1] is None
    assert desc["mode"][0] == 1
    assert desc["mode"][1] == "x"


# TEST_CASE_3
def test_fillna_numeric_strategy(monkeypatch):
    data = {"n": [1, None, 3], "c": ["a", None, "b"]}
    dtype = {"n": "int", "c": "str"}

    def numeric_strategy(vals):
        if any(v is None for v in vals):
            return 0
        return None

    df = Dataframe(data, dtype)
    df.fillna(numeric_strategy, None)

    assert df.data["n"] == [1, 0, 3]
    assert df.data["c"] == ["a", None, "b"]


# TEST_CASE_4
def test_read_csv_classmethod_with_monkeypatched_helpers(monkeypatch):
    captured = {}

    def mock_read_dtype(dtype_arg):
        captured["dtype_arg"] = dtype_arg
        return {"A": "int"}

    def mock_read_csv_file(data_path, dtypes):
        captured["data_path"] = data_path
        captured["dtypes"] = dtypes
        return {"A": [1, 2, 3]}

    monkeypatch.setattr(df_module, "read_dtype", mock_read_dtype)
    monkeypatch.setattr(df_module, "read_csv_file", mock_read_csv_file)

    df = Dataframe.read_csv("data.csv", "dtype.json")

    assert isinstance(df, Dataframe)
    assert df.data == {"A": [1, 2, 3]}
    assert df.dtype == {"A": "int"}
    assert captured["dtype_arg"] == "dtype.json"
    assert captured["data_path"] == "data.csv"
    assert captured["dtypes"] == {"A": "int"}


# TEST_CASE_5
def test_to_csv_writes_current_data(monkeypatch):
    data = {"A": [1, 2, 3], "B": [4, 5, 6]}
    dtype = {"A": "int", "B": "int"}

    captured = {}

    def mock_write_file(path, data_dict):
        captured["path"] = path
        captured["data"] = data_dict

    monkeypatch.setattr(df_module, "write_file", mock_write_file)

    df = Dataframe(data, dtype)
    df.to_csv("out.csv")

    assert captured["path"] == "out.csv"
    assert captured["data"] == data
