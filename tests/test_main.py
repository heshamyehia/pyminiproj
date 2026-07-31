import main as main_module
from main import main


# TEST_CASE_1
def test_main_inplace_mutation(monkeypatch, capsys):
    mode_holder = {"mode": "inplace"}

    def make_fake_class(mode_holder):
        class FakeDF:
            def __init__(self, mode):
                self.mode = mode
                self.mutated = False
                self.describe_called = False
                self.to_csv_path = None

            @classmethod
            def read_csv(cls, datapath, dtype):
                inst = cls(mode_holder["mode"])
                mode_holder["instance"] = inst
                return inst

            def fillna(self, *args, **kwargs):
                if self.mode == "inplace":
                    self.mutated = True

            def count_nulls(self):
                return 0 if self.mutated else 5

            def describe(self):
                mode_holder["describe_called"] = True

            def to_csv(self, path):
                mode_holder["to_csv_path"] = path

        return FakeDF

    FakeDF = make_fake_class(mode_holder)

    class FakeStats:
        @staticmethod
        def get_col_mean(x):
            return None

        @staticmethod
        def get_col_mode(x):
            return None

    # Patch the Dataframe class and stats used by main
    monkeypatch.setattr(main_module, "Dataframe", FakeDF)
    monkeypatch.setattr(main_module, "stats", FakeStats)

    main()  # execute the function under test

    out = capsys.readouterr().out
    assert out.strip() == "0"

    inst = mode_holder["instance"]
    assert inst.mutated is True
    assert mode_holder["to_csv_path"] == "data/titanic_cleaned.csv"
    assert mode_holder["describe_called"] is True


# TEST_CASE_2
def test_main_no_mutation(monkeypatch, capsys):
    mode_holder = {"mode": "nochange"}

    def make_fake_class(mode_holder):
        class FakeDF:
            def __init__(self, mode):
                self.mode = mode
                self.mutated = False
                self.describe_called = False
                self.to_csv_path = None

            @classmethod
            def read_csv(cls, datapath, dtype):
                inst = cls(mode_holder["mode"])
                mode_holder["instance"] = inst
                return inst

            def fillna(self, *args, **kwargs):
                if self.mode == "inplace":
                    self.mutated = True

            def count_nulls(self):
                return 0 if self.mutated else 5

            def describe(self):
                mode_holder["describe_called"] = True

            def to_csv(self, path):
                mode_holder["to_csv_path"] = path

        return FakeDF

    FakeDF = make_fake_class(mode_holder)

    class FakeStats:
        @staticmethod
        def get_col_mean(x):
            return None

        @staticmethod
        def get_col_mode(x):
            return None

    # Patch the Dataframe class and stats used by main
    monkeypatch.setattr(main_module, "Dataframe", FakeDF)
    monkeypatch.setattr(main_module, "stats", FakeStats)

    main()  # execute the function under test

    out = capsys.readouterr().out
    assert out.strip() == "5"

    inst = mode_holder["instance"]
    assert inst.mutated is False
    assert mode_holder["to_csv_path"] == "data/titanic_cleaned.csv"
    assert mode_holder["describe_called"] is True
