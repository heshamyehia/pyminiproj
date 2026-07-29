import pytest

from dataframe_pcg.dataframe import Dataframe


# TEST_CASE_1
def test_init_stores_exact_data_and_dtype_objects():
    data = {"value": [1]}
    dtype = {"value": "int"}

    dataframe = Dataframe(data, dtype)

    assert dataframe.data is data
    assert dataframe.dtype is dtype
    data["value"].append(2)
    assert dataframe.data["value"] == [1, 2]


# TEST_CASE_2
def test_read_csv_uses_reader_results_and_constructs_calling_class(monkeypatch):
    dtypes = {"score": "float"}
    dataset = {"score": [1.5, None]}
    calls = []

    def fake_read_dtype(dtype_path):
        calls.append(("read_dtype", dtype_path))
        return dtypes

    def fake_read_csv_file(data_path, received_dtypes):
        calls.append(("read_csv_file", data_path, received_dtypes))
        return dataset

    monkeypatch.setattr(
        "dataframe_pcg.dataframe.read_dtype",
        fake_read_dtype,
    )
    monkeypatch.setattr(
        "dataframe_pcg.dataframe.read_csv_file",
        fake_read_csv_file,
    )

    class ChildDataframe(Dataframe):
        pass

    result = ChildDataframe.read_csv("values.csv", "types.csv")

    assert type(result) is ChildDataframe
    assert result.data is dataset
    assert result.dtype is dtypes
    assert calls == [
        ("read_dtype", "types.csv"),
        ("read_csv_file", "values.csv", dtypes),
    ]


# TEST_CASE_3
def test_count_nulls_counts_only_none_and_handles_empty_columns():
    dataframe = Dataframe(
        {
            "mixed": [None, 0, False, "", [], None],
            "empty": [],
        },
        {},
    )

    result = dataframe.count_nulls()

    assert result == {"mixed": 2, "empty": 0}
    assert type(result["mixed"]) is int
    assert type(result["empty"]) is int


# TEST_CASE_4
def test_describe_writes_aligned_numeric_and_categorical_statistics(monkeypatch):
    numeric_values = [1, None, 3]
    categorical_values = ["red", None, "red"]
    calls = []
    written = {}

    def fake_max(values):
        calls.append(("max", values))
        return 3

    def fake_min(values):
        calls.append(("min", values))
        return 1

    def fake_mean(values):
        calls.append(("mean", values))
        return 2.0

    def fake_median(values):
        calls.append(("median", values))
        return 2.0

    def fake_mode(values):
        calls.append(("mode", values))
        return "numeric-mode" if values is numeric_values else "red"

    def fake_write_file(path, description):
        written["path"] = path
        written["description"] = description
        return "ignored"

    monkeypatch.setattr("dataframe_pcg.dataframe.get_col_max", fake_max)
    monkeypatch.setattr("dataframe_pcg.dataframe.get_col_min", fake_min)
    monkeypatch.setattr("dataframe_pcg.dataframe.get_col_mean", fake_mean)
    monkeypatch.setattr("dataframe_pcg.dataframe.get_col_median", fake_median)
    monkeypatch.setattr("dataframe_pcg.dataframe.get_col_mode", fake_mode)
    monkeypatch.setattr("dataframe_pcg.dataframe.write_file", fake_write_file)

    dataframe = Dataframe(
        {"score": numeric_values, "color": categorical_values},
        {"score": "float", "color": "category"},
    )

    result = dataframe.describe("summary.csv")

    assert result is None
    assert written["path"] == "summary.csv"
    description = written["description"]
    assert description["column"] == ["score", "color"]
    assert description["nulls"] == [1, 1]
    assert description["max"] == [3, None]
    assert description["min"] == [1, None]
    assert description["mean"][0] == pytest.approx(2.0)
    assert description["mean"][1] is None
    assert description["median"][0] == pytest.approx(2.0)
    assert description["median"][1] is None
    assert description["mode"] == ["numeric-mode", "red"]
    assert calls == [
        ("max", numeric_values),
        ("min", numeric_values),
        ("mean", numeric_values),
        ("median", numeric_values),
        ("mode", numeric_values),
        ("mode", categorical_values),
    ]


# TEST_CASE_5
def test_describe_empty_data_uses_default_path_and_empty_lists(monkeypatch):
    recorded = {}

    def fake_write_file(path, description):
        recorded["path"] = path
        recorded["description"] = description

    monkeypatch.setattr("dataframe_pcg.dataframe.write_file", fake_write_file)

    result = Dataframe({}, {}).describe()

    assert result is None
    assert recorded["path"] == "data/describe.csv"
    assert recorded["description"] == {
        "column": [],
        "nulls": [],
        "max": [],
        "min": [],
        "mean": [],
        "median": [],
        "mode": [],
    }


# TEST_CASE_6
def test_fillna_selects_strategy_by_exact_dtype_and_accepts_falsey_fills():
    numeric_values = [1, None]
    categorical_values = ["x", None]
    unrecognized_values = [None, 3]
    strategy_calls = []

    def numeric_strategy(values):
        strategy_calls.append(("numeric", values))
        return 0

    def categorical_strategy(values):
        strategy_calls.append(("categorical", values))
        return ""

    dataframe = Dataframe(
        {
            "number": numeric_values,
            "category": categorical_values,
            "unrecognized": unrecognized_values,
        },
        {
            "number": "int",
            "category": "category",
            "unrecognized": "Int",
        },
    )

    result = dataframe.fillna(numeric_strategy, categorical_strategy)

    assert result is None
    assert dataframe.data == {
        "number": [1, 0],
        "category": ["x", ""],
        "unrecognized": ["", 3],
    }
    assert strategy_calls == [
        ("numeric", numeric_values),
        ("categorical", categorical_values),
        ("categorical", unrecognized_values),
    ]


# TEST_CASE_7
def test_fillna_preserves_column_identity_when_strategy_returns_none():
    original = [None, "value"]
    dataframe = Dataframe({"category": original}, {"category": "text"})

    result = dataframe.fillna(None, lambda values: None)

    assert result is None
    assert dataframe.data["category"] is original
    assert dataframe.data["category"] == [None, "value"]


# TEST_CASE_8
def test_fillna_replaces_no_null_column_with_new_list_when_fill_is_valid():
    original = (1, 2)
    dataframe = Dataframe({"number": original}, {"number": "float"})

    result = dataframe.fillna(lambda values: 9.5, None)

    assert result is None
    assert dataframe.data["number"] == [1, 2]
    assert type(dataframe.data["number"]) is list
    assert dataframe.data["number"] is not original


# TEST_CASE_9
def test_fillna_propagates_strategy_exception_after_prior_column_mutation():
    first_values = [None]
    second_values = [None]
    dataframe = Dataframe(
        {"first": first_values, "second": second_values},
        {"first": "int", "second": "int"},
    )

    def strategy(values):
        if values is second_values:
            raise RuntimeError("strategy failed")
        return 7

    with pytest.raises(RuntimeError, match="strategy failed"):
        dataframe.fillna(strategy, None)

    assert dataframe.data["first"] == [7]
    assert dataframe.data["second"] is second_values
    assert dataframe.data["second"] == [None]


# TEST_CASE_10
def test_to_csv_passes_exact_path_and_data_to_writer_and_discards_return(
    monkeypatch,
):
    data = {"name": ["Ada"]}
    recorded = {}

    def fake_write_file(path, received_data):
        recorded["path"] = path
        recorded["data"] = received_data
        return "writer result"

    monkeypatch.setattr("dataframe_pcg.dataframe.write_file", fake_write_file)

    result = Dataframe(data, {"name": "text"}).to_csv("output.csv")

    assert result is None
    assert recorded["path"] == "output.csv"
    assert recorded["data"] is data
