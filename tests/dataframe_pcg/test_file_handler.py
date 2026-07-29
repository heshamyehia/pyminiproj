import csv

import pytest

from dataframe_pcg.file_handler import read_csv_file, read_dtype, write_file


# TEST_CASE_1
def test_read_csv_file_basic_integers(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("a,b\n1,2\n3,4\n", encoding="utf-8")
    dtypes = {"a": "int", "b": "int"}
    result = read_csv_file(str(path), dtypes)
    assert result == {"a": [1, 3], "b": [2, 4]}


# TEST_CASE_2
def test_read_csv_file_none_and_string(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("a,b\n7,\n", encoding="utf-8")  # second column empty -> None
    dtypes = {"a": "int", "b": "string"}
    result = read_csv_file(str(path), dtypes)
    assert result == {"a": [7], "b": [None]}


# TEST_CASE_4
def test_read_csv_file_empty_data(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("a,b\n", encoding="utf-8")
    result = read_csv_file(str(path), {"a": "int", "b": "int"})
    assert result == {"a": [], "b": []}


# TEST_CASE_5
def test_read_dtype_basic(tmp_path):
    path = tmp_path / "dtype.csv"
    path.write_text("column,dtype\nage,int\nscore,float\n", encoding="utf-8")
    result = read_dtype(str(path))
    assert result == {"age": "int", "score": "float"}


# TEST_CASE_6
def test_read_dtype_missing_keys_raises(tmp_path):
    path = tmp_path / "dtype_bad.csv"
    path.write_text("colname,type\nx,int\n", encoding="utf-8")
    with pytest.raises(KeyError):
        read_dtype(str(path))


# TEST_CASE_7
def test_write_file_normal(tmp_path):
    path = tmp_path / "out.csv"
    data = {"a": [1, None], "b": ["x", "y"]}
    write_file(str(path), data)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    assert rows[0] == ["a", "b"]
    assert rows[1] == ["1", "x"]
    assert rows[2] == ["", "y"]


# TEST_CASE_8
def test_write_file_empty_data_raises(tmp_path):
    path = tmp_path / "empty_out.csv"
    with pytest.raises(ValueError):
        write_file(str(path), {})
