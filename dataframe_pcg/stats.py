def get_col_max(col: list):
    """
    Compute the maximum value of a numerical column.

    Args:
        col (list): A list of numerical values. `None` values are ignored.

    Returns:
        The maximum value in the column (numeric type).
        
    Raises:
        TypeError: If non-numeric values (except None) are found in the column.
        ValueError: If the column is empty or contains only None values.
    """
    if not col:
        raise ValueError("Cannot compute maximum of an empty list")
    
    max_val = None
    for val in col:
        if val is not None:
            # Check if value is numeric
            if not isinstance(val, (int, float)):
                raise TypeError(
                    f"Expected numeric value (int or float), got {type(val).__name__}: {val}"
                )
            
            if max_val is None or val > max_val:
                max_val = val
    
    if max_val is None:
        raise ValueError("Cannot compute maximum: all values are None")
    
    return max_val


def get_col_min(col: list):
    """
    Compute the minimum value of a numerical column.

    Args:
        col (list): A list of numerical values. `None` values are ignored.

    Returns:
        The minimum value in the column (numeric type).
        
    Raises:
        TypeError: If non-numeric values (except None) are found in the column.
        ValueError: If the column is empty or contains only None values.
    """
    if not col:
        raise ValueError("Cannot compute minimum of an empty list")
    
    min_val = None
    for val in col:
        if val is not None:
            # Check if value is numeric
            if not isinstance(val, (int, float)):
                raise TypeError(
                    f"Expected numeric value (int or float), got {type(val).__name__}: {val}"
                )
            
            if min_val is None or val < min_val:
                min_val = val
    
    if min_val is None:
        raise ValueError("Cannot compute minimum: all values are None")
    
    return min_val


def get_col_mean(col: list):
    """
    Compute the mean (average) value of a numerical column.

    Args:
        col (list): A list of numerical values. `None` values are ignored.

    Returns:
        float: The mean value of the column.
        
    Raises:
        TypeError: If non-numeric values (except None) are found in the column.
        ValueError: If the column is empty or contains only None values.
    """
    if not col:
        raise ValueError("Cannot compute mean of an empty list")
    
    sum_val = 0
    count = 0
    
    for val in col:
        if val is not None:
            # Check if value is numeric
            if not isinstance(val, (int, float)):
                raise TypeError(
                    f"Expected numeric value (int or float), got {type(val).__name__}: {val}"
                )
            
            sum_val += val
            count += 1
    
    if count == 0:
        raise ValueError("Cannot compute mean: all values are None")
    
    return sum_val / count


def get_col_median(col: list):
    """
    Compute the median value of a numerical column.

    Args:
        col (list): A list of numerical values. `None` values are ignored.

    Returns:
        The median value of the column (numeric type).
        
    Raises:
        TypeError: If non-numeric values (except None) are found in the column.
        ValueError: If the column is empty or contains only None values.
    """
    if not col:
        raise ValueError("Cannot compute median of an empty list")
    
    # Filter out None values and check for non-numeric types
    cleaned_col = []
    for val in col:
        if val is not None:
            # Check if value is numeric
            if not isinstance(val, (int, float)):
                raise TypeError(
                    f"Expected numeric value (int or float), got {type(val).__name__}: {val}"
                )
            cleaned_col.append(val)
    
    if not cleaned_col:
        raise ValueError("Cannot compute median: all values are None")
    
    sorted_col = sorted(cleaned_col)
    n = len(sorted_col)
    
    if n % 2 != 0:  # Odd number of elements
        return sorted_col[n // 2]
    else:  # Even number of elements
        # For even n, take average of middle two elements
        return (sorted_col[n // 2 - 1] + sorted_col[n // 2]) / 2


def get_col_mode(col: list):
    """
    Compute the mode (most frequent value) of a column.
    
    Note: This function accepts any data type (numeric or string).

    Args:
        col (list): A list of values. `None` values are ignored.

    Returns:
        The mode value of the column. If multiple values have the same
        frequency, the first encountered is returned.
        
    Raises:
        ValueError: If the column is empty or contains only None values.
    """
    if not col:
        raise ValueError("Cannot compute mode of an empty list")
    
    freq = {}
    for val in col:
        if val is not None:
            if val in freq:
                freq[val] += 1
            else:
                freq[val] = 1
    
    if not freq:
        raise ValueError("Cannot compute mode: all values are None")
    
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
        
    Raises:
        TypeError: If the function is called on non-numeric columns and the function requires numeric data.
        ValueError: If columns are empty or contain only None values.
    """
    result = {}
    errors = {}
    
    for col, vals in data.items():
        if dtypes.get(col) in ['int', 'float']:
            try:
                result[col] = function(vals)
            except (TypeError, ValueError) as e:
                print(f"Error processing column '{col}': {e}")
    
    return result