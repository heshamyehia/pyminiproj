import csv

import pytest

from dataframe_pcg.file_handler import read_csv_file, read_dtype, write_file


# TEST_CASE_1
def test_read_csv_file_normal(tmp_path):
    path = tmp_path / "data.csv"
    content = "A,B,C\n1,2.5,x\n,3.0,y\n4,,z\n"
    path.write_text(content, encoding="utf-8")
    dtypes = {"A": "int", "B": "float", "C": "string"}
    result = read_csv_file(str(path), dtypes)
    expected = {"A": [1, None, 4], "B": [2.5, 3.0, None], "C": ["x", "y", "z"]}
    assert result == expected


# TEST_CASE_2
def test_read_csv_file_unsupported_dtype_raises(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("A,B\n1,2\n", encoding="utf-8")
    dtypes = {"A": "int", "B": "bool"}  # unsupported
    with pytest.raises(ValueError) as exc:
        read_csv_file(str(path), dtypes)
    assert "Unsupported data type" in str(exc.value)


# TEST_CASE_3
def test_read_csv_file_invalid_numeric_raises(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("A\nabc\n", encoding="utf-8")
    dtypes = {"A": "int"}
    with pytest.raises(ValueError):
        read_csv_file(str(path), dtypes)


# TEST_CASE_4
def test_read_dtype_basic(tmp_path):
    path = tmp_path / "dtypes.csv"
    content = "column,dtype\nA,int\nB,float\nC,string\n"
    path.write_text(content, encoding="utf-8")
    result = read_dtype(str(path))
    expected = {"A": "int", "B": "float", "C": "string"}
    assert result == expected


# TEST_CASE_6
def test_write_file_normal_roundtrip(tmp_path):
    path = tmp_path / "out.csv"
    data = {"A": [1, None, 3], "B": ["x", "y", None]}
    write_file(str(path), data)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    expected = [
        ["A", "B"],
        ["1", "x"],
        ["", "y"],
        ["3", ""],
    ]
    assert rows == expected


# TEST_CASE_7
def test_write_file_no_data_raises(tmp_path):
    path = tmp_path / "out_no_data.csv"
    with pytest.raises(ValueError) as exc:
        write_file(str(path), {})
    assert "No data to write" in str(exc.value)


# TEST_CASE_8
def test_write_file_mismatched_lengths_raises(tmp_path):
    path = tmp_path / "out_mismatch.csv"
    data = {"A": [1, 2], "B": ["x", "y", "z"]}
    with pytest.raises(ValueError) as exc:
        write_file(str(path), data)
    assert "All columns must have the same number of rows" in str(exc.value)
