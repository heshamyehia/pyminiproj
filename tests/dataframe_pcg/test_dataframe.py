import pytest

import dataframe_pcg.dataframe as dfmod
from dataframe_pcg.dataframe import Dataframe


# TEST_CASE_1
def test_init_stores_values():
    data = {"A": [1, 2, None], "B": ["x", None]}
    dtype = {"A": "int", "B": "object"}
    df = Dataframe(data, dtype)
    assert df.data is data
    assert df.dtype is dtype


# TEST_CASE_2
def test_read_csv_builds_dataframe(monkeypatch):
    dtypes = {"A": "int"}
    dataset = {"A": [1, 2, 3]}
    monkeypatch.setattr(dfmod, "read_dtype", lambda dtype: dtypes)
    monkeypatch.setattr(dfmod, "read_csv_file", lambda data, dtypes2: dataset)
    df = Dataframe.read_csv("path.csv", "dtype_path")
    assert isinstance(df, Dataframe)
    assert df.data == dataset
    assert df.dtype == dtypes


# TEST_CASE_3
def test_count_nulls_counts_correctly():
    data = {"A": [1, None, 3], "B": [None, None]}
    dtype = {"A": "int", "B": "object"}
    df = Dataframe(data, dtype)
    result = df.count_nulls()
    assert result == {"A": 1, "B": 2}


# TEST_CASE_4
def test_fillna_replaces_none_in_numeric_and_categorical(monkeypatch):
    data = {"A": [1, None, 3], "B": ["x", None, "y"]}
    dtype = {"A": "int", "B": "object"}
    df = Dataframe(data, dtype)

    # Strategies
    def numeric_strategy(vals):
        return 99

    def categorical_strategy(vals):
        return "missing"

    df.fillna(numeric_strategy, categorical_strategy)

    assert df.data["A"] == [1, 99, 3]
    assert df.data["B"] == ["x", "missing", "y"]


# TEST_CASE_5
def test_to_csv_calls_write_file_with_data(monkeypatch):
    data = {"A": [1, 2]}
    dtype = {"A": "int"}
    df = Dataframe(data, dtype)

    calls = []

    def fake_write_file(path, content):
        calls.append((path, content))

    monkeypatch.setattr(dfmod, "write_file", fake_write_file)
    df.to_csv("out.csv")
    assert calls == [("out.csv", data)]


# TEST_CASE_7
def test_count_nulls_raises_type_error_on_none_values():
    df = Dataframe({"A": None}, {"A": "int"})
    with pytest.raises(TypeError):
        df.count_nulls()
