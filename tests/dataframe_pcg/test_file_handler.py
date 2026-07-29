import csv

import pytest

from dataframe_pcg.file_handler import read_csv_file, read_dtype, write_file


# TEST_CASE_1
def test_read_csv_file_normal_and_none(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("id,value,name\n1,2.5,alice\n,3.1,bob\n", encoding="utf-8")
    data = read_csv_file(str(path), {"id": "int", "value": "float", "name": "string"})

    assert data["id"] == [1, None]
    assert data["name"] == ["alice", "bob"]
    assert data["value"] == [pytest.approx(2.5), pytest.approx(3.1)]


# TEST_CASE_2
def test_read_csv_file_unsupported_dtype_raises(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("a,b\n1,2\n", encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        read_csv_file(str(path), {"a": "int", "b": "boolean"})
    assert "Unsupported data type: boolean for column: b" in str(exc.value)


# TEST_CASE_3
def test_read_csv_file_header_only(tmp_path):
    path = tmp_path / "header_only.csv"
    path.write_text("col1,col2\n", encoding="utf-8")
    data = read_csv_file(str(path), {"col1": "int", "col2": "string"})
    assert data == {"col1": [], "col2": []}


# TEST_CASE_4
def test_read_dtype_overrides(tmp_path):
    path = tmp_path / "types.csv"
    path.write_text(
        "column,dtype\nid,int\nvalue,float\nname,string\nvalue,string\n",
        encoding="utf-8",
    )
    dtypes = read_dtype(str(path))
    assert dtypes == {"id": "int", "value": "string", "name": "string"}


# TEST_CASE_5
def test_write_file_normal_and_none(tmp_path):
    path = tmp_path / "out.csv"
    data = {"a": [1, None, 3], "b": ["x", "y", None]}
    write_file(str(path), data)

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert rows[0] == ["a", "b"]
    assert rows[1] == ["1", "x"]
    assert rows[2] == ["", "y"]
    assert rows[3] == ["3", ""]


# TEST_CASE_6
def test_read_dtype_empty_file(tmp_path):
    path = tmp_path / "empty_types.csv"
    path.write_text("column,dtype\n", encoding="utf-8")
    dtypes = read_dtype(str(path))
    assert dtypes == {}


# TEST_CASE_7
def test_read_csv_file_invalid_data_in_numeric_column_raises(tmp_path):
    path = tmp_path / "bad_data.csv"
    path.write_text("a,b\nabc,1.0\n", encoding="utf-8")
    with pytest.raises(ValueError):
        read_csv_file(str(path), {"a": "int", "b": "float"})
