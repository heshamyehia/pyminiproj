# TEST_CASE_1
def test_read_csv_uses_external_loaders(monkeypatch):
    from dataframe_pcg.dataframe import Dataframe

    fake_dtypes = {"col": "int"}
    fake_dataset = {"col": [1, 2, 3]}

    def fake_read_dtype(dtype_arg):
        assert dtype_arg == "dtype_path"
        return fake_dtypes

    def fake_read_csv_file(data_arg, dtypes_arg):
        assert data_arg == "data_path"
        assert dtypes_arg == fake_dtypes
        return fake_dataset

    monkeypatch.setattr("dataframe_pcg.dataframe.read_dtype", fake_read_dtype)
    monkeypatch.setattr("dataframe_pcg.dataframe.read_csv_file", fake_read_csv_file)

    df = Dataframe.read_csv("data_path", "dtype_path")

    assert isinstance(df, Dataframe)
    assert df.data == fake_dataset
    assert df.dtype == fake_dtypes


# TEST_CASE_2
def test_count_nulls_counts_correctly():
    from dataframe_pcg.dataframe import Dataframe

    data = {"col1": [1, None, 2], "col2": [None, None, 3]}
    dtype = {"col1": "int", "col2": "int"}
    df = Dataframe(data, dtype)

    result = df.count_nulls()
    assert result == {"col1": 1, "col2": 2}


# TEST_CASE_3
def test_describe_writes_expected_description(monkeypatch):
    from dataframe_pcg.dataframe import Dataframe

    data = {"num": [1, None, 3], "cat": ["a", None, "b"]}
    dtype = {"num": "int", "cat": "str"}

    captured = {}

    def fake_get_col_max(values):
        return 3

    def fake_get_col_min(values):
        return 1

    def fake_get_col_mean(values):
        return 2

    def fake_get_col_median(values):
        return 2

    def fake_get_col_mode(values):
        return "mode"

    def fake_write_file(path, description):
        captured["path"] = path
        captured["description"] = description

    monkeypatch.setattr("dataframe_pcg.dataframe.get_col_max", fake_get_col_max)
    monkeypatch.setattr("dataframe_pcg.dataframe.get_col_min", fake_get_col_min)
    monkeypatch.setattr("dataframe_pcg.dataframe.get_col_mean", fake_get_col_mean)
    monkeypatch.setattr("dataframe_pcg.dataframe.get_col_median", fake_get_col_median)
    monkeypatch.setattr("dataframe_pcg.dataframe.get_col_mode", fake_get_col_mode)
    monkeypatch.setattr("dataframe_pcg.dataframe.write_file", fake_write_file)

    df = Dataframe(data, dtype)
    df.describe(path="output_desc.csv")

    assert captured["path"] == "output_desc.csv"
    desc = captured["description"]
    assert desc["column"] == ["num", "cat"]
    assert desc["nulls"] == [1, 1]
    assert desc["max"] == [3, None]
    assert desc["min"] == [1, None]
    assert desc["mean"] == [2, None]
    assert desc["median"] == [2, None]
    assert desc["mode"] == ["mode", "mode"]


# TEST_CASE_4
def test_fillna_numeric_replaces_none():
    from dataframe_pcg.dataframe import Dataframe

    data = {"n": [1, None, 3]}
    df = Dataframe(data, {"n": "int"})

    def fake_num_strategy(values):
        return 0

    df.fillna(fake_num_strategy, None)
    assert df.data["n"] == [1, 0, 3]


# TEST_CASE_5
def test_fillna_categorical_replaces_none():
    from dataframe_pcg.dataframe import Dataframe

    data = {"c": ["x", None, "y"]}
    df = Dataframe(data, {"c": "str"})

    def fake_cat_strategy(values):
        return "missing"

    df.fillna(None, fake_cat_strategy)
    assert df.data["c"] == ["x", "missing", "y"]


# TEST_CASE_6
def test_to_csv_writes_data(monkeypatch):
    from dataframe_pcg.dataframe import Dataframe

    data = {"a": [1, 2]}
    df = Dataframe(data, {"a": "int"})

    captured = {}

    def fake_write_file(path, data_out):
        captured["path"] = path
        captured["data"] = data_out

    monkeypatch.setattr("dataframe_pcg.dataframe.write_file", fake_write_file)

    df.to_csv("out.csv")

    assert captured["path"] == "out.csv"
    assert captured["data"] == data
