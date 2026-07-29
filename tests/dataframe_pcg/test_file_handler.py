import pytest

from dataframe_pcg.file_handler import read_csv_file, read_dtype, write_file


# TEST_CASE_1
def test_read_dtype_basic(tmp_path):
    path = tmp_path / "dtype.csv"
    path.write_text("column,dtype\nage,int\nname,string\n", encoding="utf-8")
    result = read_dtype(str(path))
    assert result == {"age": "int", "name": "string"}


# TEST_CASE_2
def test_read_csv_file_basic_typing_and_none(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("id,name,score\n1,Alice,10\n2,Bob,\n3,Carol,20\n", encoding="utf-8")
    dtypes = {"id": "int", "score": "float", "name": "string"}
    data = read_csv_file(str(path), dtypes)
    assert data["id"] == [1, 2, 3]
    assert data["name"] == ["Alice", "Bob", "Carol"]
    assert data["score"][0] == pytest.approx(10.0)
    assert data["score"][1] is None
    assert data["score"][2] == pytest.approx(20.0)


# TEST_CASE_3
def test_read_csv_file_unsupported_dtype_raises(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("id\n1\n2\n", encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        read_csv_file(str(path), {"id": "bool"})
    assert "Unsupported data type: bool for column: id" in str(exc.value)


# TEST_CASE_4
def test_write_file_basic_roundtrip_and_none_writes_empty_cells(tmp_path):
    data = {"A": [1, None], "B": ["x", "y"], "C": [3.5, None]}
    out_path = tmp_path / "out.csv"
    write_file(str(out_path), data)
    import csv

    with open(out_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    assert rows[0] == ["A", "B", "C"]
    assert rows[1] == ["1", "x", "3.5"]
    assert rows[2] == ["", "y", ""]


# TEST_CASE_5
def test_write_file_no_data_raises(tmp_path):
    with pytest.raises(ValueError) as exc:
        write_file(str(tmp_path / "out.csv"), {})
    assert "No data to write" in str(exc.value)


# TEST_CASE_6
def test_write_file_mismatched_lengths_raises(tmp_path):
    data = {"A": [1, 2], "B": [3]}
    with pytest.raises(ValueError) as exc:
        write_file(str(tmp_path / "out.csv"), data)
    assert "All columns must have the same number of rows" in str(exc.value)


# TEST_CASE_7
def test_read_dtype_empty_file_returns_empty_dict(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("", encoding="utf-8")
    assert read_dtype(str(path)) == {}


# TEST_CASE_8
def test_read_csv_file_extra_columns_not_in_dtypes_left_as_strings(tmp_path):
    path = tmp_path / "extra.csv"
    path.write_text("id,name,score\n1,A,1.5\n2,B,2.5\n", encoding="utf-8")
    data = read_csv_file(str(path), {"id": "int", "score": "float"})
    assert data["id"] == [1, 2]
    assert data["score"] == [pytest.approx(1.5), pytest.approx(2.5)]
    assert data["name"] == ["A", "B"]
