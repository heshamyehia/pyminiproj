def get_col_max(col: list):
    """
    Compute the maximum value of a numerical column.




    Args:
        col (list): A list of numerical values. `None` values are ignored.

    Returns:
        The maximum value in the column (numeric type).
    """
    max_val = None
    for val in col:
        if val is not None and (max_val is None or val < max_val):
            max_val = val
    return max_val


def get_col_min(col: list):
    """
    Compute the minimum value of a numerical column.

    Args:
        col (list): A list of numerical values. `None` values are ignored.

    Returns:
        The minimum value in the column (numeric type).
    """
    min_val = None
    for val in col:
        if val is not None and (min_val is None or val < min_val):
            min_val = val
    return min_val


def get_col_mean(col: list):
    """
    Compute the mean (average) value of a numerical column.

    Args:
        col (list): A list of numerical values. `None` values are ignored.

    Returns:
        The mean value of the column (float).
    """
    sum = 0
    count = 0
    for val in col:
        if val is not None:
            sum += val
            count += 1
    if count == 0:
        return None
    return sum / count


def get_col_median(col: list):
    """
    Compute the median value of a numerical column.

    Args:
        col (list): A list of numerical values. `None` values are ignored.

    Returns:
        The median value of the column (numeric type).
    """
    cleaned_col = [val for val in col if val is not None]
    sorted_col = sorted(cleaned_col)
    n = len(sorted_col)
    if n == 0:
        return None
    elif n % 2 != 0:
        return sorted_col[n // 2]
    elif n % 2 == 0:
        return (sorted_col[n // 2] + sorted_col[(n // 2) + 1]) / 2


def get_col_mode(col: list):
    """
    Compute the mode (most frequent value) of a column.

    Args:
        col (list): A list of values. `None` values are ignored.

    Returns:
        The mode value of the column. If multiple values have the same
        frequency, the first encountered is returned.
    """
    freq = {}
    for val in col:
        if val is not None:
            if val in freq:
                freq[val] += 1
            else:
                freq[val] = 1
    mode = None
    max_freq = -1

    for key, val in freq.items():
        if val > max_freq:
            max_freq = val
            mode = key
    return mode


def get_stat(data: dict, dtypes: dict, function):
    """
    Apply a statistical function to all numerical columns in a dataset.

    Args:
        data (dict): Dictionary where keys are column names and values are lists of column values.
        dtypes (dict): Dictionary where keys are column names and values are data types ('int', 'float', 'string').
        function (function): A function to apply to each numerical column (e.g., get_col_max, get_col_mean).

    Returns:
        dict: A dictionary where keys are column names and values are the result
        of applying the function to that column. Only numerical columns are processed.
    """
    result = {}
    for col, vals in data.items():
        if dtypes.get(col) in ["int", "float"]:
            result[col] = function(vals)
    return result
