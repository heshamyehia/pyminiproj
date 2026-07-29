import csv

import pytest

from dataframe_pcg.file_handler import read_csv_file, read_dtype, write_file


# TEST_CASE_1
def test_read_csv_file_basic_types_and_missing_values(tmp_path):
    content = "a,b,c\n1,2.5,foo\n,4.0,\n3,,baz\n"
    file_path = tmp_path / "test1.csv"
    file_path.write_text(content, encoding="utf-8")

    result = read_csv_file(str(file_path), {"a": "int", "b": "float", "c": "string"})

    assert result["a"] == [1, None, 3]
    assert result["b"] == [2.5, 4.0, None]
    assert result["c"] == ["foo", None, "baz"]


# TEST_CASE_2
def test_read_csv_file_extra_dtype_column_ignored(tmp_path):
    content = "x,y\n1,2\n3,4\n"
    file_path = tmp_path / "test2.csv"
    file_path.write_text(content, encoding="utf-8")

    result = read_csv_file(str(file_path), {"x": "int", "z": "float"})

    assert result["x"] == [1, 3]
    assert result["y"] == ["2", "4"]


# TEST_CASE_3
def test_read_csv_file_unsupported_dtype_raises(tmp_path):
    content = "a,b\n1,2\n"
    file_path = tmp_path / "test3.csv"
    file_path.write_text(content, encoding="utf-8")

    with pytest.raises(ValueError) as excinfo:
        read_csv_file(str(file_path), {"a": "bool"})

    assert "Unsupported data type: bool for column: a" in str(excinfo.value)


# TEST_CASE_4
def test_read_dtype_basic_and_last_wins(tmp_path):
    content = "column,dtype\na,int\nb,float\na,string\n"
    file_path = tmp_path / "types.csv"
    file_path.write_text(content, encoding="utf-8")

    result = read_dtype(str(file_path))

    assert result == {"a": "string", "b": "float"}


# TEST_CASE_5
def test_read_dtype_missing_keys_raises_keyerror(tmp_path):
    content = "colx,dtype\nx,integer\n"
    file_path = tmp_path / "bad_types.csv"
    file_path.write_text(content, encoding="utf-8")

    with pytest.raises(KeyError):
        read_dtype(str(file_path))


# TEST_CASE_6
def test_write_file_writes_expected_csv(tmp_path):
    data = {
        "a": [1, None, 3],
        "b": ["x", "y", None],
        "c": [None, 7, 8],
    }
    file_path = tmp_path / "out6.csv"
    write_file(str(file_path), data)

    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert rows[0] == ["a", "b", "c"]
    assert rows[1] == ["1", "x", ""]
    assert rows[2] == ["", "y", "7"]
    assert rows[3] == ["3", "", "8"]


# TEST_CASE_7
def test_write_file_no_data_raises(tmp_path):
    file_path = tmp_path / "out7.csv"
    with pytest.raises(ValueError) as excinfo:
        write_file(str(file_path), {})
    assert "No data to write" in str(excinfo.value)


# TEST_CASE_8
def test_write_file_mismatched_lengths_raises(tmp_path):
    file_path = tmp_path / "out8.csv"
    data = {"a": [1, 2], "b": [3]}
    with pytest.raises(ValueError) as excinfo:
        write_file(str(file_path), data)
    assert "All columns must have the same number of rows" in str(excinfo.value)
