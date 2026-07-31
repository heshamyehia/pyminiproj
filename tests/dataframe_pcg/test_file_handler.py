import csv

import pytest

from dataframe_pcg.file_handler import read_csv_file, read_dtype, write_file


# TEST_CASE_1
def test_read_csv_file_basic_types_and_none(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text(
        "id,name,value\n1,Alice,3.0\n2,Bob,\n,Carol,7.5\n", encoding="utf-8"
    )
    dtypes = {"id": "int", "value": "float", "name": "string"}
    data = read_csv_file(str(path), dtypes)

    assert data["id"] == [1, 2, None]
    assert data["name"] == ["Alice", "Bob", "Carol"]
    assert data["value"][0] == pytest.approx(3.0)
    assert data["value"][1] is None
    assert data["value"][2] == pytest.approx(7.5)


# TEST_CASE_2
def test_read_csv_file_ignore_missing_in_dtypes(tmp_path):
    path = tmp_path / "data2.csv"
    path.write_text("a,b\n5,X\n7,Y\n", encoding="utf-8")
    data = read_csv_file(str(path), {"a": "int", "c": "float"})

    assert data["a"] == [5, 7]
    assert data["b"] == ["X", "Y"]


# TEST_CASE_3
def test_read_csv_file_unsupported_dtype_raises(tmp_path):
    path = tmp_path / "data3.csv"
    path.write_text("col\n1\n", encoding="utf-8")
    with pytest.raises(ValueError) as excinfo:
        read_csv_file(str(path), {"col": "unsupported"})
    assert "Unsupported data type" in str(excinfo.value)


# TEST_CASE_4
def test_read_dtype_basic(tmp_path):
    path = tmp_path / "types.csv"
    path.write_text(
        "column,dtype\ncol1,int\ncol2,float\ncol3,string\n", encoding="utf-8"
    )
    dtypes = read_dtype(str(path))
    assert dtypes == {"col1": "int", "col2": "float", "col3": "string"}


# TEST_CASE_5
def test_read_dtype_empty_file(tmp_path):
    path = tmp_path / "empty_types.csv"
    path.write_text("", encoding="utf-8")
    dtypes = read_dtype(str(path))
    assert dtypes == {}


# TEST_CASE_6
def test_write_file_basic(tmp_path):
    path = tmp_path / "out.csv"
    data = {"a": [1, 2], "b": [3, 4]}
    write_file(str(path), data)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    assert rows == [["a", "b"], ["1", "3"], ["2", "4"]]


# TEST_CASE_7
def test_write_file_none_values_written_as_empty(tmp_path):
    path = tmp_path / "out_none.csv"
    data = {"col": [1, None, 3]}
    write_file(str(path), data)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    assert rows == [["col"], ["1"], [""], ["3"]]


# TEST_CASE_8
def test_write_file_raises_on_no_data(tmp_path):
    path = tmp_path / "out_empty.csv"
    with pytest.raises(ValueError) as excinfo:
        write_file(str(path), {})
    assert "No data to write" in str(excinfo.value)
