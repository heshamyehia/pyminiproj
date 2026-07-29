from dataframe_pcg.dataframe import Dataframe


# TEST_CASE_1
def test_read_csv_builds_dataframe(monkeypatch):
    mock_dtypes = {"A": "int", "B": "str"}
    mock_dataset = {"A": [1, 2], "B": ["x", "y"]}

    def fake_read_dtype(dtype):
        assert dtype == "dtype_path"
        return mock_dtypes

    def fake_read_csv_file(data, dtypes):
        assert data == "path/to/data.csv"
        assert dtypes == mock_dtypes
        return mock_dataset

    monkeypatch.setattr("dataframe_pcg.dataframe.read_dtype", fake_read_dtype)
    monkeypatch.setattr("dataframe_pcg.dataframe.read_csv_file", fake_read_csv_file)

    df = Dataframe.read_csv("path/to/data.csv", "dtype_path")

    assert isinstance(df, Dataframe)
    assert df.data == mock_dataset
    assert df.dtype == mock_dtypes


# TEST_CASE_2
def test_count_nulls_counts_none_values():
    df = Dataframe({"a": [1, None, 3], "b": [None, None, 5]}, {"a": "int", "b": "str"})
    res = df.count_nulls()
    assert res == {"a": 1, "b": 2}


# TEST_CASE_4
def test_fillna_numeric_and_categorical(monkeypatch):
    data = {"col_num": [1, None, 3], "col_cat": [None, "x", None]}
    dtype = {"col_num": "int", "col_cat": "str"}
    df = Dataframe(data, dtype)

    df.fillna(num_strategy=lambda vals: 0, cat_strategy=lambda vals: "missing")

    assert df.data["col_num"] == [1, 0, 3]
    assert df.data["col_cat"] == ["missing", "x", "missing"]


# TEST_CASE_5
def test_to_csv_writes_current_data(monkeypatch):
    written = {}

    def fake_write_file(path, data_to_write):
        written["path"] = path
        written["data"] = data_to_write

    monkeypatch.setattr("dataframe_pcg.dataframe.write_file", fake_write_file)

    df = Dataframe({"a": [1, None], "b": ["x", None]}, {"a": "int", "b": "str"})
    df.to_csv("out.csv")

    assert written["path"] == "out.csv"
    assert written["data"] == df.data


# TEST_CASE_6
def test_count_nulls_empty_data():
    df = Dataframe({}, {})
    assert df.count_nulls() == {}
