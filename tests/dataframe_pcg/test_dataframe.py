import dataframe_pcg.dataframe as dfm
from dataframe_pcg.dataframe import Dataframe


# TEST_CASE_1
def test_read_csv_constructs_dataframe(monkeypatch):
    expected_dtype = {"a": "int"}
    expected_dataset = {"a": [1, 2, 3]}

    def fake_read_dtype(dtype_arg):
        assert dtype_arg == "dtype_path"
        return expected_dtype

    def fake_read_csv_file(data_arg, dtypes_arg):
        assert data_arg == "data_path"
        assert dtypes_arg == expected_dtype
        return expected_dataset

    monkeypatch.setattr(dfm, "read_dtype", fake_read_dtype)
    monkeypatch.setattr(dfm, "read_csv_file", fake_read_csv_file)

    df = Dataframe.read_csv("data_path", "dtype_path")

    assert isinstance(df, Dataframe)
    assert df.data == expected_dataset
    assert df.dtype == expected_dtype


# TEST_CASE_2
def test_count_nulls_basic():
    data = {"col1": [1, None, 3], "col2": [None, None], "col3": [5]}
    df = Dataframe(data, {"col1": "int", "col2": "int", "col3": "int"})
    assert df.count_nulls() == {"col1": 1, "col2": 2, "col3": 0}


# TEST_CASE_3
def test_describe_writes_expected_stats(monkeypatch):
    data = {"a": [1, 2, 3], "b": ["x", "y", "x"], "c": [2, 4, 6]}
    dtype = {"a": "int", "b": "str", "c": "float"}
    df = Dataframe(data, dtype)

    def fake_max(vals):
        return max(vals) if vals else None

    def fake_min(vals):
        return min(vals) if vals else None

    def fake_mean(vals):
        return (
            sum(vals) // len(vals) if vals else None
        )  # integer division for determinism

    def fake_median(vals):
        if not vals:
            return None
        s = sorted(vals)
        n = len(s)
        mid = n // 2
        if n % 2 == 1:
            return s[mid]
        else:
            return (s[mid - 1] + s[mid]) // 2

    def fake_mode(vals):
        if vals == [1, 2, 3]:
            return "M_A"
        if vals == ["x", "y", "x"]:
            return "M_B"
        if vals == [2, 4, 6]:
            return "M_C"
        return "M"

    written = {}

    def fake_write_file(path, description):
        written["path"] = path
        written["description"] = description

    monkeypatch.setattr(dfm, "get_col_max", fake_max)
    monkeypatch.setattr(dfm, "get_col_min", fake_min)
    monkeypatch.setattr(dfm, "get_col_mean", fake_mean)
    monkeypatch.setattr(dfm, "get_col_median", fake_median)
    monkeypatch.setattr(dfm, "get_col_mode", fake_mode)
    monkeypatch.setattr(dfm, "write_file", fake_write_file)

    df.describe()  # uses default path

    expected_desc = {
        "column": ["a", "b", "c"],
        "nulls": [0, 0, 0],
        "max": [3, None, 6],
        "min": [1, None, 2],
        "mean": [2, None, 4],
        "median": [2, None, 4],
        "mode": ["M_A", "M_B", "M_C"],
    }

    assert written["path"] == "data/describe.csv"
    assert written["description"] == expected_desc


# TEST_CASE_4
def test_fillna_applies_strategies(monkeypatch):
    data = {"num": [1, None, 3], "cat": ["a", None, "c"]}
    dtype = {"num": "int", "cat": "str"}
    df = Dataframe(data, dtype)

    def num_strategy(vals):
        return -1

    def cat_strategy(vals):
        return "missing"

    df.fillna(num_strategy, cat_strategy)

    assert df.data["num"] == [1, -1, 3]
    assert df.data["cat"] == ["a", "missing", "c"]


# TEST_CASE_5
def test_to_csv_calls_write_file_with_data(monkeypatch):
    data = {"x": [1, 2, 3]}
    dtype = {"x": "int"}
    df = Dataframe(data, dtype)

    captured = {}

    def fake_write_file(path, payload):
        captured["path"] = path
        captured["payload"] = payload

    monkeypatch.setattr(dfm, "write_file", fake_write_file)

    df.to_csv("out.csv")

    assert captured["path"] == "out.csv"
    assert captured["payload"] == data
