# Dataframe Package

A simple Python library for reading, analyzing, and cleaning CSV data files.

## What It Does

- Read CSV files
- Handle missing values
- Compute statistics (mean, median, mode, min, max)
- Save cleaned data

## Quick Start

```python
from dataframe_pcg import Dataframe, stats

# Load your data
df = Dataframe.read_csv("data.csv", "dtype.csv")

# Fill missing values
df.fillna(stats.get_col_mean, stats.get_col_mode)

# Save cleaned data
df.to_csv("cleaned_data.csv")
```

## Installation

No installation needed! Just put the `dataframe_pcg` folder in your project.

**Requirements:** Python 3.6+

## Project Structure

```
your_project/
├── dataframe_pcg/      # The package
│   ├── __init__.py
│   ├── dataframe.py
│   ├── file_handler.py
│   └── stats.py
├── main.py             # Your code
└── data/               # Your CSV files
```

## How To Use

### 1. Create a Data Type File

Make a CSV that defines your column types:

**dtype.csv:**
```csv
column,dtype
Age,float
Name,string
Count,int
```

Types: `int`, `float`, `string`

### 2. Load Data

```python
from dataframe_pcg import Dataframe

df = Dataframe.read_csv("data.csv", "dtype.csv")
```

### 3. Check Missing Values

```python
nulls = df.count_nulls()
print(nulls)  # {'Age': 10, 'Name': 5}
```

### 4. Fill Missing Values

```python
from dataframe_pcg import stats

# Numeric → mean, Categorical → mode
df.fillna(stats.get_col_mean, stats.get_col_mode)
```

### 5. Get Statistics

```python
df.describe("statistics.csv")
```

### 6. Save Results

```python
df.to_csv("cleaned_data.csv")
```

## Complete Example

```python
from dataframe_pcg import Dataframe, stats

# Load
df = Dataframe.read_csv("titanic.csv", "titanic_dtype.csv")

# Check nulls
print("Missing values:", df.count_nulls())

# Fill nulls
df.fillna(stats.get_col_mean, stats.get_col_mode)

# Generate stats
df.describe("statistics.csv")

# Save
df.to_csv("titanic_cleaned.csv")
```

## Available Functions

### Statistical Functions

```python
from dataframe_pcg import stats

stats.get_col_mean([1, 2, 3, None, 5])     # 2.75
stats.get_col_median([1, 2, 3, 4, 5])      # 3
stats.get_col_mode(['a', 'b', 'b', 'c'])   # 'b'
stats.get_col_min([1, 2, 3])               # 1
stats.get_col_max([1, 2, 3])               # 3
```

### Dataframe Methods

```python
df.count_nulls()              # Count missing values
df.fillna(num_func, cat_func) # Fill missing values
df.describe()                 # Generate statistics
df.to_csv(path)              # Save to CSV
```

## Common Issues

**Error: "No module named 'dataframe_pcg'"**
- Make sure `main.py` is outside the `dataframe_pcg` folder
- Run from the project root: `python main.py`

**Error: "FileNotFoundError"**
- Check your file paths
- Make sure you're in the correct directory

**Error: "Expected numeric value, got str"**
- You have strings in a numeric column
- Check your dtype.csv file
- Clean your data

## Tips

- Always run from the project root directory
- Keep `main.py` outside the `dataframe_pcg` folder
- Use correct data types in dtype.csv
- Check for missing values before computing statistics

## Author

fa3el kheer

## License

MIT License - Free to use and modify
