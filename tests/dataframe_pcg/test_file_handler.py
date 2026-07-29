import csv

import pytest

from dataframe_pcg.file_handler import read_csv_file, read_dtype, write_file


# TEST_CASE_1
def test_read_csv_file_basic_types(tmp_path):
    p = tmp_path / "data.csv"
    p.write_text("a,b,c\n1,2.5,alpha\n,3.0,\n", encoding="utf-8")
    data = read_csv_file(str(p), {"a": "int", "b": "float", "c": "string"})
    assert data["a"] == [1, None]
    assert data["b"][0] == pytest.approx(2.5)
    assert data["b"][1] == pytest.approx(3.0)
    assert data["c"] == ["alpha", None]


# TEST_CASE_2
def test_read_csv_file_unsupported_dtype_raises(tmp_path):
    p = tmp_path / "data.csv"
    p.write_text("a\n1\n", encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        read_csv_file(str(p), {"a": "bool"})
    assert "Unsupported data type" in str(exc.value)


# TEST_CASE_3
def test_read_dtype_basic(tmp_path):
    p = tmp_path / "types.csv"
    p.write_text("column,dtype\ncol1,int\ncol2,float\n", encoding="utf-8")
    dtypes = read_dtype(str(p))
    assert dtypes == {"col1": "int", "col2": "float"}


# TEST_CASE_4
def test_read_dtype_empty_file(tmp_path):
    p = tmp_path / "empty.csv"
    p.write_text("", encoding="utf-8")
    dtypes = read_dtype(str(p))
    assert dtypes == {}


# TEST_CASE_5
def test_write_file_normal(tmp_path):
    p = tmp_path / "out.csv"
    data = {"col1": [1, None, 3], "col2": ["a", "b", None]}
    write_file(str(p), data)
    with open(p, newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))
    expected = [["col1", "col2"], ["1", "a"], ["", "b"], ["3", ""]]
    assert reader == expected
