import pytest

from main import Dataframe, main, stats


# TEST_CASE_1
def test_main_runs_full_workflow_with_exact_arguments_and_prints_null_counts(
    monkeypatch, capsys
):
    calls = []
    null_counts = {"age": 0, "name": 2}

    class FakeDataframe:
        def fillna(self, mean_func, mode_func):
            calls.append(("fillna", mean_func, mode_func))
            return "ignored fillna result"

        def count_nulls(self):
            calls.append(("count_nulls",))
            return null_counts

        def describe(self):
            calls.append(("describe",))
            return "ignored describe result"

        def to_csv(self, path):
            calls.append(("to_csv", path))
            return "ignored to_csv result"

    fake_df = FakeDataframe()

    def fake_read_csv(datapath, dtype):
        calls.append(("read_csv", datapath, dtype))
        return fake_df

    monkeypatch.setattr(Dataframe, "read_csv", fake_read_csv)

    result = main()

    assert result is None
    assert capsys.readouterr().out == "{'age': 0, 'name': 2}\n"
    assert calls == [
        ("read_csv", "data/titanic.csv", "data/titanic_dtype.csv"),
        ("fillna", stats.get_col_mean, stats.get_col_mode),
        ("count_nulls",),
        ("describe",),
        ("to_csv", "data/titanic_cleaned.csv"),
    ]


# TEST_CASE_2
def test_main_propagates_read_csv_exception_and_stops(monkeypatch, capsys):
    expected_error = RuntimeError("read failed")

    def fake_read_csv(datapath, dtype):
        assert datapath == "data/titanic.csv"
        assert dtype == "data/titanic_dtype.csv"
        raise expected_error

    monkeypatch.setattr(Dataframe, "read_csv", fake_read_csv)

    with pytest.raises(RuntimeError) as exc_info:
        main()

    assert exc_info.value is expected_error
    assert capsys.readouterr().out == ""


# TEST_CASE_3
def test_main_uses_original_dataframe_when_fillna_returns_another_object(
    monkeypatch, capsys
):
    calls = []

    class ReplacementDataframe:
        def count_nulls(self):
            raise AssertionError("replacement dataframe must not be used")

    class OriginalDataframe:
        def fillna(self, mean_func, mode_func):
            calls.append(("fillna", mean_func, mode_func))
            return ReplacementDataframe()

        def count_nulls(self):
            calls.append(("count_nulls",))

        def describe(self):
            calls.append(("describe",))

        def to_csv(self, path):
            calls.append(("to_csv", path))

    original_df = OriginalDataframe()
    monkeypatch.setattr(Dataframe, "read_csv", lambda datapath, dtype: original_df)

    result = main()

    assert result is None
    assert capsys.readouterr().out == "None\n"
    assert calls == [
        ("fillna", stats.get_col_mean, stats.get_col_mode),
        ("count_nulls",),
        ("describe",),
        ("to_csv", "data/titanic_cleaned.csv"),
    ]


# TEST_CASE_4
def test_main_does_not_describe_or_write_when_count_nulls_raises(monkeypatch, capsys):
    calls = []
    expected_error = ValueError("count failed")

    class FakeDataframe:
        def fillna(self, mean_func, mode_func):
            calls.append("fillna")

        def count_nulls(self):
            calls.append("count_nulls")
            raise expected_error

        def describe(self):
            calls.append("describe")

        def to_csv(self, path):
            calls.append("to_csv")

    monkeypatch.setattr(Dataframe, "read_csv", lambda datapath, dtype: FakeDataframe())

    with pytest.raises(ValueError) as exc_info:
        main()

    assert exc_info.value is expected_error
    assert calls == ["fillna", "count_nulls"]
    assert capsys.readouterr().out == ""


# TEST_CASE_5
def test_main_does_not_write_csv_when_describe_raises(monkeypatch, capsys):
    calls = []
    expected_error = LookupError("describe failed")

    class FakeDataframe:
        def fillna(self, mean_func, mode_func):
            calls.append("fillna")

        def count_nulls(self):
            calls.append("count_nulls")
            return []

        def describe(self):
            calls.append("describe")
            raise expected_error

        def to_csv(self, path):
            calls.append("to_csv")

    monkeypatch.setattr(Dataframe, "read_csv", lambda datapath, dtype: FakeDataframe())

    with pytest.raises(LookupError) as exc_info:
        main()

    assert exc_info.value is expected_error
    assert calls == ["fillna", "count_nulls", "describe"]
    assert capsys.readouterr().out == "[]\n"
