import csv

import pytest

from dataframe_pcg.file_handler import read_csv_file, read_dtype, write_file


# TEST_CASE_1
def test_read_csv_file_basic_and_none_conversions(tmp_path):
    csv_path = tmp_path / "data1.csv"
    csv_path.write_text(
        "col1,col2,col3\n1,2.5,foo\n,3.0,bar\n3,,baz\n", encoding="utf-8"
    )
    data = read_csv_file(
        str(csv_path), {"col1": "int", "col2": "float", "col3": "string"}
    )

    assert data["col1"][0] == 1
    assert data["col1"][1] is None
    assert data["col1"][2] == 3

    assert data["col2"][0] == pytest.approx(2.5)
    assert data["col2"][1] == pytest.approx(3.0)
    assert data["col2"][2] is None

    assert data["col3"][0] == "foo"
    assert data["col3"][1] == "bar"
    assert data["col3"][2] == "baz"


# TEST_CASE_2
def test_read_csv_file_ignores_extra_dtype_mapping(tmp_path):
    csv_path = tmp_path / "data2.csv"
    csv_path.write_text(
        "col1,col2,col3\n1,2.5,foo\n,3.0,bar\n3,,baz\n", encoding="utf-8"
    )
    data = read_csv_file(
        str(csv_path), {"col1": "int", "col2": "float", "col3": "string", "col4": "int"}
    )

    # extra dtype mapping for a non-existent column should be ignored
    assert "col4" not in data

    assert data["col1"][0] == 1
    assert data["col1"][1] is None
    assert data["col1"][2] == 3

    assert data["col2"][0] == pytest.approx(2.5)
    assert data["col2"][1] == pytest.approx(3.0)
    assert data["col2"][2] is None

    assert data["col3"][0] == "foo"
    assert data["col3"][1] == "bar"
    assert data["col3"][2] == "baz"


# TEST_CASE_3
def test_read_csv_file_unsupported_dtype_raises(tmp_path):
    csv_path = tmp_path / "data3.csv"
    csv_path.write_text("col1,col2,col3\n1,2.5,foo\n", encoding="utf-8")
    with pytest.raises(ValueError):
        read_csv_file(
            str(csv_path), {"col1": "bool", "col2": "float", "col3": "string"}
        )


# TEST_CASE_4
def test_read_dtype_basic(tmp_path):
    csv_path = tmp_path / "dtype1.csv"
    csv_path.write_text(
        "column,dtype\ncolA,int\ncolB,float\ncolC,string\n", encoding="utf-8"
    )
    dtypes = read_dtype(str(csv_path))
    assert dtypes == {"colA": "int", "colB": "float", "colC": "string"}


# TEST_CASE_6
def test_write_file_writes_header_and_rows(tmp_path):
    out_path = tmp_path / "out.csv"
    data = {"A": [1, None, 3], "B": ["x", "y", None], "C": [None, 0, 5]}
    write_file(str(out_path), data)

    with open(out_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert rows[0] == ["A", "B", "C"]
    assert rows[1] == ["1", "x", ""]
    assert rows[2] == ["", "y", "0"]
    assert rows[3] == ["3", "", "5"]


# TEST_CASE_7
def test_write_file_no_data_raises(tmp_path):
    out_path = tmp_path / "out_no_data.csv"
    with pytest.raises(ValueError, match="No data to write"):
        write_file(str(out_path), {})


# TEST_CASE_8
def test_write_file_mismatched_lengths_raises(tmp_path):
    out_path = tmp_path / "out_bad.csv"
    data = {"A": [1, 2], "B": [3]}
    with pytest.raises(
        ValueError, match="All columns must have the same number of rows"
    ):
        write_file(str(out_path), data)
