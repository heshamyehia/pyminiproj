import main


# TEST_CASE_1
def test_main_fillna_mutates_in_place(monkeypatch, capsys):
    class FakeDFMutate:
        latest_instance = None
        to_csv_called_with = None

        def __init__(self):
            FakeDFMutate.latest_instance = self
            self.nulls = 5
            self.fillna_args = None

        @classmethod
        def read_csv(cls, datapath, dtype):
            return cls()

        def fillna(self, a, b):
            self.fillna_args = (a, b)
            self.nulls = 0  # mutate in place

        def count_nulls(self):
            return self.nulls

        def describe(self):
            self.descr = True

        def to_csv(self, path):
            FakeDFMutate.to_csv_called_with = path

    class DummyStats:
        get_col_mean = "mean_callable"
        get_col_mode = "mode_callable"

    monkeypatch.setattr(main, "Dataframe", FakeDFMutate)
    monkeypatch.setattr(main, "stats", DummyStats)

    main.main()
    out = capsys.readouterr().out
    assert out.strip() == "0"
    inst = FakeDFMutate.latest_instance
    assert inst.fillna_args == (DummyStats.get_col_mean, DummyStats.get_col_mode)
    assert FakeDFMutate.to_csv_called_with == "data/titanic_cleaned.csv"


# TEST_CASE_2
def test_main_fillna_no_mutation(monkeypatch, capsys):
    class FakeDFNoMutate:
        latest_instance = None
        to_csv_called_with = None

        def __init__(self):
            FakeDFNoMutate.latest_instance = self
            self.nulls = 7
            self.fillna_args = None

        @classmethod
        def read_csv(cls, datapath, dtype):
            return cls()

        def fillna(self, a, b):
            self.fillna_args = (a, b)
            # does not mutate in place

        def count_nulls(self):
            return self.nulls

        def describe(self):
            self.descr = True

        def to_csv(self, path):
            FakeDFNoMutate.to_csv_called_with = path

    class DummyStats:
        get_col_mean = "mean_callable"
        get_col_mode = "mode_callable"

    monkeypatch.setattr(main, "Dataframe", FakeDFNoMutate)
    monkeypatch.setattr(main, "stats", DummyStats)

    main.main()
    out = capsys.readouterr().out
    assert out.strip() == "7"
    assert FakeDFNoMutate.to_csv_called_with == "data/titanic_cleaned.csv"
