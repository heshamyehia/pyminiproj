import csv


def read_csv_file(file_path, dtypes: dict):
    """
    Read a CSV file and convert each column to the specified data type.

    Args:
        file_path (str): Path to the CSV data file.
        dtypes (dict): Dictionary mapping column names to data types ('int', 'float', 'string').

    Returns:
        dict: A dictionary where keys are column names and values are lists of column values.
              Missing values (empty strings) are replaced with None.



    """
    data = {}

    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # initialize keys
        for col in reader.fieldnames:
            data[col] = []

        # read rows
        for row in reader:
            for col in reader.fieldnames:
                val = row[col]
                data[col].append(val if val != "" else None)
    # convert data types
    for col, dtype in dtypes.items():
        if col in data:
            if dtype == "int":
                data[col] = [int(x) if x is not None else None for x in data[col]]
            elif dtype == "float":
                data[col] = [float(x) if x is not None else None for x in data[col]]
            elif dtype == "string":
                data[col] = [str(x) if x is not None else None for x in data[col]]
            else:
                raise ValueError(f"Unsupported data type: {dtype} for column: {col}")

    return data


def read_dtype(file_path):
    """
    Read a CSV file containing column names and their data types.

    Args:
        file_path (str): Path to the CSV file containing column names and types.

    Returns:
        dict: A dictionary where keys are column names and values are data types ('int', 'float', 'string').
    """
    dtypes = {}

    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            col_name = row["column"]
            col_type = row["dtype"]
            dtypes[col_name] = col_type

    return dtypes


def write_file(file_path, data: dict):
    """
    Write a data dictionary to a CSV file.

    Args:
        file_path (str): Path to the output CSV file.
        data (dict): Dictionary where keys are column names and values are lists of column values.

    Returns:
        None
    """

    if not data:
        raise ValueError("No data to write")

    fieldnames = list(data.keys())
    lengths = [len(v) for v in data.values()]
    if not lengths:
        raise ValueError("No columns to write")
    if any(l != lengths[0] for l in lengths):
        raise ValueError("All columns must have the same number of rows")

    n_rows = lengths[0]

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)

        for i in range(n_rows):
            row = []
            for col in fieldnames:
                val = data[col][i]
                row.append("" if val is None else val)
            writer.writerow(row)
