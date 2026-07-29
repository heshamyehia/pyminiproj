import csv

import pytest

from dataframe_pcg.file_handler import read_csv_file, read_dtype, write_file


# TEST_CASE_1
def test_read_csv_file_basic_conversion_and_none(tmp_path):
    path = tmp_path / "data.csv"
    content = "id,int_col,flt_col,str_col\n1,2,3.5,hello\n,,4.0,world\n3,,,\n"
    path.write_text(content, encoding="utf-8")

    dtypes = {"id": "int", "int_col": "int", "flt_col": "float", "str_col": "string"}
    data = read_csv_file(str(path), dtypes)

    assert data["id"][0] == 1
    assert data["id"][1] is None
    assert data["id"][2] == 3

    assert data["int_col"][0] == 2
    assert data["int_col"][1] is None
    assert data["int_col"][2] is None

    assert data["flt_col"][0] == pytest.approx(3.5)
    assert data["flt_col"][1] == pytest.approx(4.0)
    assert data["flt_col"][2] is None

    assert data["str_col"][0] == "hello"
    assert data["str_col"][1] == "world"
    assert data["str_col"][2] is None


# TEST_CASE_2
def test_read_csv_file_raises_on_invalid_int_value(tmp_path):
    path = tmp_path / "data.csv"
    content = "id,val\nabc,1\n"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(ValueError):
        read_csv_file(str(path), {"id": "int", "val": "int"})


# TEST_CASE_3
def test_read_dtype_duplicate_last_wins(tmp_path):
    path = tmp_path / "dtype.csv"
    content = "column,dtype\n a,int\n a,float\n".replace(
        " a", "a"
    )  # ensure clean content
    path.write_text(content, encoding="utf-8")

    result = read_dtype(str(path))
    assert result == {"a": "float"}


# TEST_CASE_4
def test_read_dtype_missing_headers_keyerror(tmp_path):
    path = tmp_path / "dtype_bad.csv"
    # Missing the required 'column' header
    content = "dtype\nint\nfloat\n"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(KeyError):
        read_dtype(str(path))


# TEST_CASE_5
def test_write_file_writes_header_and_rows_with_none(tmp_path):
    path = tmp_path / "out.csv"
    data = {"col1": [1, None], "col2": ["x", "y"]}
    write_file(str(path), data)

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert rows[0] == ["col1", "col2"]
    assert rows[1] == ["1", "x"]
    assert rows[2] == ["", "y"]


# TEST_CASE_6
def test_write_file_no_data_to_write_raises(tmp_path):
    path = tmp_path / "no_data.csv"
    with pytest.raises(ValueError, match="No data to write"):
        write_file(str(path), {})


# TEST_CASE_7
def test_write_file_inconsistent_lengths_raises(tmp_path):
    path = tmp_path / "inconsistent.csv"
    data = {"a": [1, 2], "b": [3]}
    with pytest.raises(
        ValueError, match="All columns must have the same number of rows"
    ):
        write_file(str(path), data)
