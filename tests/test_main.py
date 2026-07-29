import main


# TEST_CASE_1
def test_main_executes_with_patched_dependencies(monkeypatch, capsys):
    class FakeDataframe:
        last_read_args = None
        last_instance = None

        def __init__(self):
            FakeDataframe.last_instance = self
            self.nulls = 5
            self.describe_called = False
            self.to_csv_path = None
            self.fillna_args = None

        @classmethod
        def read_csv(cls, datapath, dtype):
            FakeDataframe.last_read_args = (datapath, dtype)
            return cls()

        def fillna(self, *args, **kwargs):
            self.fillna_args = args
            self.nulls = 0

        def count_nulls(self):
            return self.nulls

        def describe(self):
            self.describe_called = True

        def to_csv(self, path):
            self.to_csv_path = path

    class FakeStats:
        def __init__(self):
            self.get_col_mean = lambda *args, **kwargs: None
            self.get_col_mode = lambda *args, **kwargs: None

    monkeypatch.setattr(main, "Dataframe", FakeDataframe)
    monkeypatch.setattr(main, "stats", FakeStats())

    main.main()

    captured = capsys.readouterr()
    assert "0" in captured.out

    # Verify read_csv was called with correct paths
    assert FakeDataframe.last_read_args == (
        "data/titanic.csv",
        "data/titanic_dtype.csv",
    )

    # Verify the dataframe instance mutated as expected
    df_instance = FakeDataframe.last_instance
    assert df_instance is not None
    assert df_instance.nulls == 0
    assert df_instance.describe_called is True
    assert df_instance.to_csv_path == "data/titanic_cleaned.csv"

    # Verify fillna was called with the two function objects from stats
    assert df_instance.fillna_args is not None
    assert len(df_instance.fillna_args) == 2
    stats_obj = main.stats
    assert df_instance.fillna_args[0] is stats_obj.get_col_mean
    assert df_instance.fillna_args[1] is stats_obj.get_col_mode
