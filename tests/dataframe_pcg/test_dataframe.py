import dataframe_pcg.dataframe as dfmod
from dataframe_pcg.dataframe import Dataframe


# TEST_CASE_1
def test_read_csv_constructs_dataframe(monkeypatch):
    # Setup stubs to simulate file_handler behavior
    def fake_read_dtype(dtype_path):
        return {"type": "int"}

    def fake_read_csv_file(data_path, dtypes):
        return {"col": [1, 2, 3]}

    captured = {}

    def fake_write_file(path, description):
        captured["path"] = path
        captured["description"] = description

    monkeypatch.setattr(dfmod, "read_dtype", fake_read_dtype)
    monkeypatch.setattr(dfmod, "read_csv_file", fake_read_csv_file)
    monkeypatch.setattr(dfmod, "write_file", fake_write_file)

    df = Dataframe.read_csv("data_path.csv", "dtype_path.json")

    assert isinstance(df, Dataframe)
    assert df.data == {"col": [1, 2, 3]}
    assert df.dtype == {"type": "int"}


# TEST_CASE_2
def test_count_nulls_counts_none_values():
    data = {
        "a": [1, None, 3],
        "b": [None, None, 5],
    }
    df = Dataframe(data, {"a": "int", "b": "int"})
    counts = df.count_nulls()
    assert counts == {"a": 1, "b": 2}


# TEST_CASE_5
def test_init_stores_references():
    data = {"a": [1]}
    dtype = {"a": "int"}
    df = Dataframe(data, dtype)

    # Mutate the original data after construction
    data["a"].append(2)

    # Dataframe should reflect the mutation since it stores references
    assert df.data["a"] == [1, 2]


# TEST_CASE_6
def test_to_csv_writes_current_data(monkeypatch):
    data = {"a": [1, None, 3]}
    dtype = {"a": "int"}
    captured = {}

    def fake_write_file(path, payload):
        captured["path"] = path
        captured["payload"] = payload

    monkeypatch.setattr(dfmod, "write_file", fake_write_file)

    df = Dataframe(data, dtype)
    df.to_csv("out.csv")

    assert captured["path"] == "out.csv"
    assert captured["payload"] == data
