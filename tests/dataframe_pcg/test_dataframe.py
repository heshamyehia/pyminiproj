import pytest

import dataframe_pcg.dataframe as dfmod
from dataframe_pcg.dataframe import Dataframe


# TEST_CASE_1
def test_init_sets_attributes():
    data = {"A": [1, 2], "B": [None, 3]}
    dtype = {"A": "int", "B": "float"}
    df = Dataframe(data, dtype)
    assert df.data == data
    assert df.dtype == dtype


# TEST_CASE_2
def test_read_csv_factory_uses_helpers(monkeypatch):
    calls = {}

    def fake_read_dtype(dtype_input):
        calls["dtype_input"] = dtype_input
        return {"A": "int"}

    def fake_read_csv_file(data_input, dtypes_input):
        calls["data_input"] = data_input
        calls["dtypes_input"] = dtypes_input
        return {"A": [1, 2, 3]}

    monkeypatch.setattr(dfmod, "read_dtype", fake_read_dtype)
    monkeypatch.setattr(dfmod, "read_csv_file", fake_read_csv_file)

    df = Dataframe.read_csv("path/to/data.csv", "dtype_path.csv")
    assert isinstance(df, Dataframe)
    assert df.data == {"A": [1, 2, 3]}
    assert df.dtype == {"A": "int"}
    assert calls["dtype_input"] == "dtype_path.csv"
    assert calls["data_input"] == "path/to/data.csv"
    assert calls["dtypes_input"] == {"A": "int"}


# TEST_CASE_3
def test_count_nulls_counts_each_column():
    data = {"A": [1, None, 2], "B": [None, None], "C": [3]}
    df = Dataframe(data, {"A": "int", "B": "str", "C": "int"})
    result = df.count_nulls()
    assert result == {"A": 1, "B": 2, "C": 0}


# TEST_CASE_4
def test_describe_writes_and_computes(monkeypatch):
    data = {"A": [1, 2, None], "B": [3.0, 4.0, 5.0], "C": ["x", "x", None]}
    dtype = {"A": "int", "B": "float", "C": "str"}
    df = Dataframe(data, dtype)

    def fake_get_max(vals):
        non_none = [v for v in vals if v is not None]
        if not non_none:
            return None
        return max(non_none)

    def fake_get_min(vals):
        non_none = [v for v in vals if v is not None]
        if not non_none:
            return None
        return min(non_none)

    def fake_get_mean(vals):
        non_none = [v for v in vals if v is not None]
        if not non_none:
            return None
        return sum(non_none) / len(non_none)

    def fake_get_median(vals):
        non_none = sorted([v for v in vals if v is not None])
        if not non_none:
            return None
        n = len(non_none)
        mid = n // 2
        if n % 2 == 1:
            return non_none[mid]
        else:
            return (non_none[mid - 1] + non_none[mid]) / 2

    def fake_get_mode(vals):
        from collections import Counter

        non_none = [v for v in vals if v is not None]
        if not non_none:
            return None
        counts = Counter(non_none)
        maxcount = max(counts.values())
        modes = [k for k, v in counts.items() if v == maxcount]
        return min(modes)

    monkeypatch.setattr(dfmod, "get_col_max", fake_get_max)
    monkeypatch.setattr(dfmod, "get_col_min", fake_get_min)
    monkeypatch.setattr(dfmod, "get_col_mean", fake_get_mean)
    monkeypatch.setattr(dfmod, "get_col_median", fake_get_median)
    monkeypatch.setattr(dfmod, "get_col_mode", fake_get_mode)

    recorded = {}

    def fake_write_file(path, description):
        recorded["path"] = path
        recorded["description"] = description

    monkeypatch.setattr(dfmod, "write_file", fake_write_file)

    ret = df.describe()
    assert ret is None

    expected_path = "data/describe.csv"
    assert recorded["path"] == expected_path

    desc = recorded["description"]
    assert desc["column"] == ["A", "B", "C"]
    assert desc["nulls"] == [1, 0, 1]

    assert desc["max"][0] == 2
    assert desc["max"][1] == pytest.approx(5.0)
    assert desc["max"][2] is None

    assert desc["min"][0] == 1
    assert desc["min"][1] == pytest.approx(3.0)
    assert desc["min"][2] is None

    assert desc["mean"][0] == pytest.approx(1.5)
    assert desc["mean"][1] == pytest.approx(4.0)
    assert desc["mean"][2] is None

    assert desc["median"][0] == pytest.approx(1.5)
    assert desc["median"][1] == pytest.approx(4.0)
    assert desc["median"][2] is None

    assert desc["mode"][0] == 1
    assert desc["mode"][1] == pytest.approx(3.0)
    assert desc["mode"][2] == "x"


# TEST_CASE_5
def test_fillna_numeric_and_categorical():
    data = {"A": [1, None, 3], "B": ["x", None, "y"]}
    dtype = {"A": "int", "B": "str"}
    df = Dataframe(data, dtype)

    def num_strategy(vals):
        return 0

    def cat_strategy(vals):
        return "missing"

    df.fillna(num_strategy, cat_strategy)

    assert df.data["A"] == [1, 0, 3]
    assert df.data["B"] == ["x", "missing", "y"]


# TEST_CASE_6
def test_to_csv_calls_write_file(monkeypatch):
    data = {"A": [1, 2]}
    df = Dataframe(data, {"A": "int"})

    captured = {}

    def fake_write_file(path, payload):
        captured["path"] = path
        captured["payload"] = payload

    monkeypatch.setattr(dfmod, "write_file", fake_write_file)

    df.to_csv("out.csv")

    assert captured["path"] == "out.csv"
    assert captured["payload"] == data


# TEST_CASE_7
def test_read_csv_raises_on_bad_dtype(monkeypatch):
    def bad_read_dtype(_):
        raise ValueError("bad dtype")

    monkeypatch.setattr(dfmod, "read_dtype", bad_read_dtype)

    with pytest.raises(ValueError):
        Dataframe.read_csv("data.csv", "bad")
