from .file_handler import read_csv_file, read_dtype, write_file
from .stats import get_col_mean, get_col_median, get_col_mode, get_col_max, get_col_min

class Dataframe:
    def __init__(self, data: dict, dtype: dict):
        self.data = data
        self.dtype = dtype
    
    @classmethod
    def read_csv(cls, data_path, dtype_path):
        """
        Read a CSV file and return a Dataframe instance.
        
        Args:
            data_path (str): Path to the CSV data file
            dtype_path (str): Path to the CSV dtype file
            
        Returns:
            Dataframe: A new Dataframe instance
            
        Raises:
            FileNotFoundError: If data or dtype file is not found
            ValueError: If dtype file format is invalid
        """
        try:
            dtypes = read_dtype(dtype_path)
            dataset = read_csv_file(data_path, dtypes)
            df = cls(dataset, dtypes)
            return df
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Could not read file: {e}")
        except ValueError as e:
            raise ValueError(f"Invalid data format: {e}")
    
    def count_nulls(self):
        """
        Count null values in each column.
        
        Returns:
            dict: Dictionary mapping column names to null counts
        """
        null_counts = {}
        for col, values in self.data.items():
            null_count = sum(1 for val in values if val is None)
            null_counts[col] = null_count
        return null_counts    
    
    def describe(self, path="data/describe.csv"):
        """
        Generate descriptive statistics for all columns.
        
        Args:
            path (str): Output path for the statistics CSV file
            
        Raises:
            TypeError: If numeric columns contain non-numeric values
            ValueError: If columns are empty or invalid
            IOError: If unable to write to output file
        """
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
            
            if self.dtype.get(col) in ['int', 'float']:
                # Compute numeric statistics with exception handling
                try:
                    maxs.append(get_col_max(values))
                except (TypeError, ValueError) as e:
                    print(f"Warning: Could not compute max for '{col}': {e}")
                    maxs.append(None)
                
                try:
                    mins.append(get_col_min(values))
                except (TypeError, ValueError) as e:
                    print(f"Warning: Could not compute min for '{col}': {e}")
                    mins.append(None)
                
                try:
                    means.append(get_col_mean(values))
                except (TypeError, ValueError) as e:
                    print(f"Warning: Could not compute mean for '{col}': {e}")
                    means.append(None)
                
                try:
                    medians.append(get_col_median(values))
                except (TypeError, ValueError) as e:
                    print(f"Warning: Could not compute median for '{col}': {e}")
                    medians.append(None)
            else:
                maxs.append(None)
                mins.append(None)
                means.append(None)
                medians.append(None)
            
            # Mode can be computed for any column type
            try:
                modes.append(get_col_mode(values))
            except ValueError as e:
                print(f"Warning: Could not compute mode for '{col}': {e}")
                modes.append(None)

        description = {
            'column': cols,
            'nulls': nulls,
            'max': maxs,
            'min': mins,
            'mean': means,
            'median': medians,
            'mode': modes,
        }

        try:
            write_file(path, description)
            print(f"Statistics written to {path}")
        except IOError as e:
            raise IOError(f"Could not write statistics file: {e}")
    
    def fillna(self, num_strategy, cat_strategy):
        """
        Fill missing values in dataframe.
        
        Args:
            num_strategy (function): Function to compute fill value for numeric columns (e.g., get_col_mean)
            cat_strategy (function): Function to compute fill value for categorical columns (e.g., get_col_mode)
            
        Raises:
            TypeError: If strategy functions receive incompatible data types
            ValueError: If strategy functions cannot compute fill values
        """
        for col, values in self.data.items():
            fill_value = None
            
            try:
                # Determine fill strategy based on column type
                if self.dtype.get(col) in ['int', 'float']:
                    if num_strategy:
                        fill_value = num_strategy(values)
                else:  # categorical/string columns
                    if cat_strategy:
                        fill_value = cat_strategy(values)
                
                # Only fill if we have a valid fill value
                if fill_value is not None:
                    self.data[col] = [val if val is not None else fill_value for val in values]
                    print(f"Filled missing values in column '{col}' with '{fill_value}'")
                    
            except TypeError as e:
                print(f"Error: Cannot fill column '{col}' - {e}")
                print(f"  Skipping column '{col}'")
            except ValueError as e:
                print(f"Warning: Cannot compute fill value for column '{col}' - {e}")
                print(f"  Skipping column '{col}'")
    
    def to_csv(self, file_path):
        """
        Write dataframe to a CSV file.
        
        Args:
            file_path (str): Path to the output CSV file
            
        Raises:
            IOError: If unable to write to the specified file
            ValueError: If data is invalid or empty
        """
        try:
            write_file(file_path, self.data)
            print(f"Data written to {file_path}")
        except (IOError, ValueError) as e:
            raise IOError(f"Could not write CSV file: {e}")
