import csv

import pytest

from dataframe_pcg.file_handler import read_csv_file, read_dtype, write_file


# TEST_CASE_1
def test_read_csv_file_basic_with_none_and_types(tmp_path):
    # create a csv with some empty fields and mixed types
    file_path = tmp_path / "data.csv"
    content = "a,b,c\n1,2.5,hello\n,3.0,world\n4,,end\n"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    data = read_csv_file(str(file_path), {"a": "int", "b": "float", "c": "string"})

    assert data["a"] == [1, None, 4]
    assert data["b"][0] == pytest.approx(2.5)
    assert data["b"][1] == pytest.approx(3.0)
    assert data["b"][2] is None
    assert data["c"] == ["hello", "world", "end"]


# TEST_CASE_2
def test_read_csv_file_unsupported_dtype_raises(tmp_path):
    file_path = tmp_path / "data.csv"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("a\n")  # header only; will trigger dtype handling regardless of data

    with pytest.raises(ValueError) as excinfo:
        read_csv_file(str(file_path), {"a": "bool"})
    assert "Unsupported data type: bool for column: a" in str(excinfo.value)


# TEST_CASE_3
def test_read_dtype_basic(tmp_path):
    file_path = tmp_path / "types.csv"
    content = "column,dtype\ncol1,int\ncol2,float\ncol3,string\n"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    dtypes = read_dtype(str(file_path))
    assert dtypes == {"col1": "int", "col2": "float", "col3": "string"}


# TEST_CASE_4
def test_write_file_success_with_two_columns_and_rows(tmp_path):
    file_path = tmp_path / "out.csv"
    data = {
        "A": [1, 2],
        "B": ["x", "y"],
        "C": [None, 3],
    }

    write_file(str(file_path), data)

    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert rows[0] == ["A", "B", "C"]
    assert rows[1] == ["1", "x", ""]
    assert rows[2] == ["2", "y", "3"]


# TEST_CASE_5
def test_write_file_empty_data_raises(tmp_path):
    file_path = tmp_path / "empty.csv"
    with pytest.raises(ValueError) as excinfo:
        write_file(str(file_path), {})
    assert "No data to write" in str(excinfo.value)


# TEST_CASE_6
def test_write_file_mismatched_lengths_raises(tmp_path):
    file_path = tmp_path / "mismatch.csv"
    data = {
        "A": [1, 2],
        "B": [3],
    }
    with pytest.raises(ValueError) as excinfo:
        write_file(str(file_path), data)
    assert "All columns must have the same number of rows" in str(excinfo.value)
