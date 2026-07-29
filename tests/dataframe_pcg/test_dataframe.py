import pytest

import dataframe_pcg.dataframe as dfmod
from dataframe_pcg.dataframe import Dataframe


# TEST_CASE_1
def test_read_csv_constructs_dataframe(monkeypatch):
    def fake_read_dtype(dtype):
        return {"A": "int", "B": "str"}

    def fake_read_csv_file(data, dtypes):
        return {"A": [1, 2], "B": ["x", "y"]}

    monkeypatch.setattr(dfmod, "read_dtype", fake_read_dtype)
    monkeypatch.setattr(dfmod, "read_csv_file", fake_read_csv_file)

    df = Dataframe.read_csv("dummy_path", "dtype_path")

    assert isinstance(df, Dataframe)
    assert df.data == {"A": [1, 2], "B": ["x", "y"]}
    assert df.dtype == {"A": "int", "B": "str"}


# TEST_CASE_2
def test_count_nulls_counts_properly():
    data = {"a": [1, None, 3], "b": [None, None, 5]}
    df = Dataframe(data, {"a": "int", "b": "int"})

    result = df.count_nulls()

    assert result == {"a": 1, "b": 2}


# TEST_CASE_3
def test_describe_writes_expected_summary(monkeypatch):
    data = {"num": [1, 2, 3], "cat": ["a", "a", "b"]}
    dtype = {"num": "int", "cat": "str"}
    df = Dataframe(data, dtype)

    def fake_max(vals):
        return max(vals) if vals else None

    def fake_min(vals):
        return min(vals) if vals else None

    def fake_mean(vals):
        return sum(vals) / len(vals) if vals else None

    def fake_median(vals):
        if not vals:
            return None
        s = sorted(vals)
        m = len(s) // 2
        return s[m] if len(s) % 2 == 1 else (s[m - 1] + s[m]) / 2

    def fake_mode(vals):
        from collections import Counter

        if not vals:
            return None
        c = Counter(vals)
        return c.most_common(1)[0][0]

    monkeypatch.setattr(dfmod, "get_col_max", fake_max)
    monkeypatch.setattr(dfmod, "get_col_min", fake_min)
    monkeypatch.setattr(dfmod, "get_col_mean", fake_mean)
    monkeypatch.setattr(dfmod, "get_col_median", fake_median)
    monkeypatch.setattr(dfmod, "get_col_mode", fake_mode)

    captured = {}

    def fake_write_file(path, description):
        captured["path"] = path
        captured["description"] = description

    monkeypatch.setattr(dfmod, "write_file", fake_write_file)

    df.describe(path="out.csv")

    description = captured["description"]
    assert captured["path"] == "out.csv"
    assert description["column"] == ["num", "cat"]
    assert description["nulls"] == [0, 0]
    assert description["max"] == [3, None]
    assert description["min"] == [1, None]
    assert description["mean"][0] == pytest.approx(2.0)
    assert description["median"] == [2, None]
    assert description["mode"] == [1, "a"]


# TEST_CASE_4
def test_fillna_applies_strategies_correctly():
    data = {"a": [1, None, 3], "b": [None, "x", None]}
    df = Dataframe(data, {"a": "int", "b": "str"})

    def num_strategy(vals):
        return 0

    def cat_strategy(vals):
        return "missing"

    df.fillna(num_strategy, cat_strategy)

    assert df.data["a"] == [1, 0, 3]
    assert df.data["b"] == ["missing", "x", "missing"]


# TEST_CASE_5
def test_to_csv_calls_write_file(monkeypatch):
    data = {"a": [1, 2]}
    df = Dataframe(data, {"a": "int"})

    called = {}

    def fake_write_file(path, payload):
        called["path"] = path
        called["payload"] = payload

    monkeypatch.setattr(dfmod, "write_file", fake_write_file)

    df.to_csv("out.csv")

    assert called["path"] == "out.csv"
    assert called["payload"] == data
