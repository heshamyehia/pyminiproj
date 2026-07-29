import dataframe_pcg.dataframe as dp
from dataframe_pcg.dataframe import Dataframe


# TEST_CASE_3
def test_count_nulls_basic():
    df = Dataframe({"a": [1, None, None], "b": [None, 2, 3]}, {"a": "int", "b": "int"})
    counts = df.count_nulls()
    assert counts == {"a": 2, "b": 1}


# TEST_CASE_4
def test_describe_writes_and_values(monkeypatch):
    # Prepare a dataframe with one numeric and one non-numeric column
    df = Dataframe({"x": [1, 2, None], "y": ["a", None]}, {"x": "int", "y": "str"})

    # Patch external helpers to produce deterministic outputs
    monkeypatch.setattr(dp, "get_col_max", lambda v: 10)
    monkeypatch.setattr(dp, "get_col_min", lambda v: 0)
    monkeypatch.setattr(dp, "get_col_mean", lambda v: 5.5)
    monkeypatch.setattr(dp, "get_col_median", lambda v: 5)
    monkeypatch.setattr(dp, "get_col_mode", lambda v: "mode")

    captured = {}

    def fake_write_file(path, description):
        captured["path"] = path
        captured["description"] = description

    monkeypatch.setattr(dp, "write_file", fake_write_file)

    df.describe()

    expected_description = {
        "column": ["x", "y"],
        "nulls": [1, 1],
        "max": [10, None],
        "min": [0, None],
        "mean": [5.5, None],
        "median": [5, None],
        "mode": ["mode", "mode"],
    }

    assert captured.get("path") == "data/describe.csv"
    assert captured.get("description") == expected_description


# TEST_CASE_5
def test_fillna_numeric_replaces_none():
    df = Dataframe({"n": [1, None, 3], "s": ["a", "b", "c"]}, {"n": "int", "s": "str"})

    df.fillna(lambda vals: 0, None)

    assert df.data["n"] == [1, 0, 3]
    assert df.data["s"] == ["a", "b", "c"]


# TEST_CASE_6
def test_fillna_categorical_replaces_none():
    df = Dataframe(
        {"cat": [None, "x", None], "num": [1, 2, 3]}, {"cat": "str", "num": "int"}
    )

    df.fillna(None, lambda vals: "missing")

    assert df.data["cat"] == ["missing", "x", "missing"]
    assert df.data["num"] == [1, 2, 3]


# TEST_CASE_7
def test_to_csv_calls_write_file(monkeypatch):
    captured = {}

    def fake_write_file(path, data):
        captured["path"] = path
        captured["data"] = data

    monkeypatch.setattr(dp, "write_file", fake_write_file)

    df = Dataframe({"a": [1, 2]}, {"a": "int"})
    df.to_csv("out.csv")

    assert captured["path"] == "out.csv"
    assert captured["data"] == {"a": [1, 2]}
