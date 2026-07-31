import pytest

from dataframe_pcg.dataframe import Dataframe


# TEST_CASE_1
def test_read_csv_constructs_dataframe(monkeypatch):
    calls = {}

    def mock_read_dtype(dtype_path):
        calls["dtype_arg"] = dtype_path
        return {"col1": "int", "col2": "str"}

    def mock_read_csv_file(data, dtypes):
        calls["data_arg"] = data
        calls["dtypes_arg"] = dtypes
        return {"col1": [1, 2, None], "col2": ["a", None, "c"]}

    monkeypatch.setattr("dataframe_pcg.dataframe.read_dtype", mock_read_dtype)
    monkeypatch.setattr("dataframe_pcg.dataframe.read_csv_file", mock_read_csv_file)

    df = Dataframe.read_csv("path/to/data.csv", "path/to/dtype.json")

    assert isinstance(df, Dataframe)
    assert df.data == {"col1": [1, 2, None], "col2": ["a", None, "c"]}
    assert df.dtype == {"col1": "int", "col2": "str"}
    assert calls["dtype_arg"] == "path/to/dtype.json"
    assert calls["data_arg"] == "path/to/data.csv"
    assert calls["dtypes_arg"] == {"col1": "int", "col2": "str"}


# TEST_CASE_2
def test_count_nulls_basic():
    df = Dataframe({"A": [1, None, 3], "B": [None, None, 5]}, {"A": "int", "B": "int"})
    result = df.count_nulls()
    assert result == {"A": 1, "B": 2}


# TEST_CASE_3
def test_describe_numeric_and_non_numeric_and_modes(monkeypatch):
    recorded = {}

    def mock_get_col_max(vals):
        return 5

    def mock_get_col_min(vals):
        return 0

    def mock_get_col_mean(vals):
        return 2.5

    def mock_get_col_median(vals):
        return 2

    def mock_get_col_mode(vals):
        return "MODE"

    def mock_write_file(path, description):
        recorded["path"] = path
        recorded["description"] = description

    monkeypatch.setattr("dataframe_pcg.dataframe.get_col_max", mock_get_col_max)
    monkeypatch.setattr("dataframe_pcg.dataframe.get_col_min", mock_get_col_min)
    monkeypatch.setattr("dataframe_pcg.dataframe.get_col_mean", mock_get_col_mean)
    monkeypatch.setattr("dataframe_pcg.dataframe.get_col_median", mock_get_col_median)
    monkeypatch.setattr("dataframe_pcg.dataframe.get_col_mode", mock_get_col_mode)
    monkeypatch.setattr("dataframe_pcg.dataframe.write_file", mock_write_file)

    data = {"n": [1, None, 3], "c": ["x", None, "y"]}
    df = Dataframe(data, {"n": "int", "c": "str"})
    df.describe(path="output/describe.csv")

    expected = {
        "column": ["n", "c"],
        "nulls": [1, 1],
        "max": [5, None],
        "min": [0, None],
        "mean": [2.5, None],
        "median": [2, None],
        "mode": ["MODE", "MODE"],
    }

    assert recorded["path"] == "output/describe.csv"
    assert recorded["description"] == expected


# TEST_CASE_4
def test_fillna_numeric_and_categorical():
    df = Dataframe(
        {"num": [1, None, 3], "cat": ["a", None, "b"]}, {"num": "int", "cat": "str"}
    )

    def num_strategy(vals):
        return 0 if any(v is None for v in vals) else None

    def cat_strategy(vals):
        return "missing" if any(v is None for v in vals) else None

    df.fillna(num_strategy, cat_strategy)

    assert df.data["num"] == [1, 0, 3]
    assert df.data["cat"] == ["a", "missing", "b"]


# TEST_CASE_5
def test_to_csv_calls_write_file(monkeypatch):
    recorded = {}

    def fake_write_file(path, data):
        recorded["path"] = path
        recorded["data"] = data

    monkeypatch.setattr("dataframe_pcg.dataframe.write_file", fake_write_file)

    df = Dataframe({"A": [1, 2]}, {"A": "int"})
    df.to_csv("out.csv")

    assert recorded["path"] == "out.csv"
    assert recorded["data"] == {"A": [1, 2]}


# TEST_CASE_6
def test_read_csv_propagates_exception(monkeypatch):
    def raise_error(dtype):
        raise ValueError("bad dtype")

    monkeypatch.setattr("dataframe_pcg.dataframe.read_dtype", raise_error)

    with pytest.raises(ValueError):
        Dataframe.read_csv("data.csv", "dtype_path")


# TEST_CASE_7
def test_describe_empty_dataset_writes_empty(monkeypatch):
    captured = {}

    def fake_write(path, description):
        captured["path"] = path
        captured["description"] = description

    monkeypatch.setattr("dataframe_pcg.dataframe.write_file", fake_write)

    df = Dataframe({}, {})
    df.describe("d/describe.csv")

    assert captured["path"] == "d/describe.csv"
    assert captured["description"] == {
        "column": [],
        "nulls": [],
        "max": [],
        "min": [],
        "mean": [],
        "median": [],
        "mode": [],
    }
