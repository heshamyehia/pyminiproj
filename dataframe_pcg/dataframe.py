from .file_handler import read_csv_file, read_dtype, write_file
from .stats import get_col_max, get_col_mean, get_col_median, get_col_min, get_col_mode


class Dataframe:
    def __init__(self, data: dict, dtype: dict):
        self.data = data
        self.dtype = dtype

    # TODO: define read_csv(data_path, dtype_path)

    @classmethod
    def read_csv(cls, data, dtype):
        dtypes = read_dtype(dtype)
        dataset = read_csv_file(data, dtypes)
        df = cls(dataset, dtypes)
        return df

    # TODO: define count_nulls()
    def count_nulls(self):
        null_counts = {}
        for col, values in self.data.items():
            null_count = sum(1 for val in values if val is None)
            null_counts[col] = null_count
        return null_counts

    # TODO: define describe() nulls , max ,min, mean, median, mode
    def describe(self, path="data/describe.csv"):
        cols = []
        nulls = []
        maxs = []
        mins = []
        means = []
        medians = []
        modes = []

        for col, values in self.data.items():
            cols.append(col)
            nulls.append(sum(1 for val in values if val is None))
            if self.dtype.get(col) in ["int", "float"]:
                maxs.append(get_col_max(values))
                mins.append(get_col_min(values))
                means.append(get_col_mean(values))
                medians.append(get_col_median(values))
            else:
                maxs.append(None)
                mins.append(None)
                means.append(None)
                medians.append(None)
            modes.append(get_col_mode(values))
        description = {
            "column": cols,
            "nulls": nulls,
            "max": maxs,
            "min": mins,
            "mean": means,
            "median": medians,
            "mode": modes,
        }

        write_file(path, description)

    # TODO: define fillna()
    def fillna(self, num_strategy, cat_strategy):
        for col, values in self.data.items():
            fill_value = None

            if self.dtype.get(col) in ["int", "float"]:
                if num_strategy:
                    fill_value = num_strategy(values)
            else:  # categorical
                if cat_strategy:
                    fill_value = cat_strategy(values)

            # Only fill if we have a valid fill value
            if fill_value is not None:
                self.data[col] = [
                    val if val is not None else fill_value for val in values
                ]

    # TODO: define to_csv()

    def to_csv(self, file_path):
        write_file(file_path, self.data)
