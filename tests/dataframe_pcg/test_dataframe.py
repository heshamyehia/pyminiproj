import dataframe_pcg.dataframe as dfmod
from dataframe_pcg.dataframe import Dataframe


# TEST_CASE_1
def test_init_stores_references():
    data = {"a": [1, 2]}
    dtype = {"a": "int"}
    df = Dataframe(data, dtype)
    data["a"].append(3)
    assert df.data["a"] == [1, 2, 3]


# TEST_CASE_2
def test_read_csv_uses_helpers_and_returns_dataframe(monkeypatch):
    calls = {}

    def fake_read_dtype(dtype_param):
        calls["dtype_param"] = dtype_param
        return {"a": "int"}

    def fake_read_csv_file(data_param, dtypes_param):
        calls["data_param"] = data_param
        calls["dtypes_param"] = dtypes_param
        return {"col1": [1, 2, 3]}

    monkeypatch.setattr(dfmod, "read_dtype", fake_read_dtype)
    monkeypatch.setattr(dfmod, "read_csv_file", fake_read_csv_file)

    df = Dataframe.read_csv("path/to/data.csv", "dtype_path")

    assert isinstance(df, Dataframe)
    assert df.data == {"col1": [1, 2, 3]}
    assert df.dtype == {"a": "int"}
    assert calls["dtype_param"] == "dtype_path"
    assert calls["data_param"] == "path/to/data.csv"
    assert calls["dtypes_param"] == {"a": "int"}


# TEST_CASE_3
def test_count_nulls_counts_none_values():
    data = {"col": [1, None, 3, None], "col2": [None, 2, None, 4]}
    dtype = {"col": "int", "col2": "int"}
    df = Dataframe(data, dtype)
    result = df.count_nulls()
    assert result == {"col": 2, "col2": 2}


# TEST_CASE_5
def test_fillna_numeric_and_categorical_strategies(monkeypatch):
    data = {
        "num": [1, None, 3, None],
        "cat": ["a", None, "b", None],
    }
    dtype = {"num": "int", "cat": "string"}
    df = Dataframe(data, dtype)

    # Simple strategies: fill with fixed values
    df.fillna(lambda vals: 99, lambda vals: "UNK")

    assert df.data["num"] == [1, 99, 3, 99]
    assert df.data["cat"] == ["a", "UNK", "b", "UNK"]


# TEST_CASE_6
def test_to_csv_calls_write_file(monkeypatch):
    captured = {}

    def fake_write_file(path, data):
        captured["path"] = path
        captured["data"] = data

    monkeypatch.setattr(dfmod, "write_file", fake_write_file)

    data = {"col": [1]}
    dtype = {"col": "int"}
    df = Dataframe(data, dtype)
    df.to_csv("output.csv")

    assert captured["path"] == "output.csv"
    assert captured["data"] == data
