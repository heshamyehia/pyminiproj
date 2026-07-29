import dataframe_pcg.dataframe as dataframe_module
from dataframe_pcg.dataframe import Dataframe


# TEST_CASE_1
def test_init_assigns_data_and_dtype():
    data = {"A": [1, 2]}
    dtype = {"A": "int"}
    df = Dataframe(data, dtype)
    assert df.data is data
    assert df.dtype is dtype


# TEST_CASE_3
def test_count_nulls_counts_none_values():
    data = {"A": [1, None, 3], "B": [None, None, 2]}
    dtype = {"A": "int", "B": "int"}
    df = Dataframe(data, dtype)
    assert df.count_nulls() == {"A": 1, "B": 2}


# TEST_CASE_6
def test_to_csv_writes_internal_data(monkeypatch):
    data = {"A": [1, 2]}
    df = Dataframe(data, {"A": "int"})

    captured = {}

    def fake_write_file(path, payload):
        captured["path"] = path
        captured["payload"] = payload

    monkeypatch.setattr(dataframe_module, "write_file", fake_write_file)

    df.to_csv("out.csv")
    assert captured["path"] == "out.csv"
    assert captured["payload"] == data
