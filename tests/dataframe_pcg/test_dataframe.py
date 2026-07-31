import pytest

import dataframe_pcg.dataframe as dfmod
from dataframe_pcg.dataframe import Dataframe


# TEST_CASE_1
def test_init_sets_attributes():
    data = {"a": [1, 2], "b": [None, 3]}
    dtype = {"a": "int", "b": "str"}
    df = Dataframe(data, dtype)
    assert df.data == data
    assert df.dtype == dtype


# TEST_CASE_2
def test_read_csv_uses_helpers_and_constructs_instance(monkeypatch):
    def fake_read_dtype(dtype):
        return {"a": "int"}

    def fake_read_csv_file(data, dtypes):
        return {"a": [1, 2, 3]}

    monkeypatch.setattr(dfmod, "read_dtype", fake_read_dtype)
    monkeypatch.setattr(dfmod, "read_csv_file", fake_read_csv_file)

    result = Dataframe.read_csv("fake_data", "fake_dtype")
    assert isinstance(result, Dataframe)
    assert result.data == {"a": [1, 2, 3]}
    assert result.dtype == {"a": "int"}


# TEST_CASE_3
def test_count_nulls_counts_none_values():
    data = {"col1": [1, None, 3], "col2": [None, None, "x"]}
    df = Dataframe(data, {"col1": "int", "col2": "str"})
    counts = df.count_nulls()
    assert counts == {"col1": 1, "col2": 2}


# TEST_CASE_4
def test_describe_writes_expected_description(monkeypatch):
    data = {"col1": [1, None, 3], "col2": ["a", None, "b"]}
    dtype = {"col1": "int", "col2": "str"}
    df = Dataframe(data, dtype)

    captured = {}

    def fake_write(path, description):
        captured["path"] = path
        captured["description"] = description

    monkeypatch.setattr(dfmod, "write_file", fake_write)
    monkeypatch.setattr(dfmod, "get_col_max", lambda values: "MAX")
    monkeypatch.setattr(dfmod, "get_col_min", lambda values: "MIN")
    monkeypatch.setattr(dfmod, "get_col_mean", lambda values: "MEAN")
    monkeypatch.setattr(dfmod, "get_col_median", lambda values: "MEDIAN")
    monkeypatch.setattr(dfmod, "get_col_mode", lambda values: "MODE")

    df.describe(path="path/to/describe.csv")

    expected = {
        "column": ["col1", "col2"],
        "nulls": [1, 1],
        "max": ["MAX", None],
        "min": ["MIN", None],
        "mean": ["MEAN", None],
        "median": ["MEDIAN", None],
        "mode": ["MODE", "MODE"],
    }
    assert captured["path"] == "path/to/describe.csv"
    assert captured["description"] == expected


# TEST_CASE_5
def test_fillna_applies_strategies_for_numeric_and_categorical():
    data = {"num": [1, None, 3], "cat": ["a", None, "b"]}
    df = Dataframe(data, {"num": "int", "cat": "str"})

    def num_strategy(values):
        return 99

    def cat_strategy(values):
        return "missing"

    df.fillna(num_strategy, cat_strategy)

    assert df.data["num"] == [1, 99, 3]
    assert df.data["cat"] == ["a", "missing", "b"]


# TEST_CASE_6
def test_to_csv_writes_current_data(monkeypatch):
    captured = {}

    def fake_write(path, content):
        captured["path"] = path
        captured["content"] = content

    df = Dataframe({"x": [1, 2], "y": [3, 4]}, {"x": "int", "y": "int"})

    monkeypatch.setattr(dfmod, "write_file", fake_write)

    df.to_csv("out.csv")

    assert captured["path"] == "out.csv"
    assert captured["content"] == {"x": [1, 2], "y": [3, 4]}


# TEST_CASE_7
def test_read_csv_exception_propagation(monkeypatch):
    def fail_read_dtype(dtype):
        raise ValueError("bad dtype")

    monkeypatch.setattr(dfmod, "read_dtype", fail_read_dtype)

    with pytest.raises(ValueError):
        Dataframe.read_csv("data", "dtype")
