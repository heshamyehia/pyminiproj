import pytest

from dataframe_pcg.file_handler import read_csv_file, read_dtype, write_file


# TEST_CASE_2
def test_read_csv_file_unsupported_dtype_raises(tmp_path):
    file_path = tmp_path / "data.csv"
    file_path.write_text("id\n1\n", encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        read_csv_file(str(file_path), {"id": "invalid"})
    assert "Unsupported data type" in str(exc.value)


# TEST_CASE_3
def test_read_csv_file_numeric_conversion_error_raises(tmp_path):
    file_path = tmp_path / "data.csv"
    file_path.write_text("id\nabc\n", encoding="utf-8")
    with pytest.raises(ValueError):
        read_csv_file(str(file_path), {"id": "int"})


# TEST_CASE_5
def test_read_dtype_missing_headers_raises(tmp_path):
    file_path = tmp_path / "bad.csv"
    file_path.write_text("col1,col2\nid,int\n", encoding="utf-8")
    with pytest.raises(KeyError):
        read_dtype(str(file_path))


# TEST_CASE_7
def test_write_file_no_data_to_write_raises(tmp_path):
    file_path = tmp_path / "out.csv"
    with pytest.raises(ValueError) as exc:
        write_file(str(file_path), {})
    assert "No data to write" in str(exc.value)


# TEST_CASE_8
def test_write_file_mismatched_lengths_raises(tmp_path):
    file_path = tmp_path / "out2.csv"
    data = {"a": [1, 2], "b": [3]}
    with pytest.raises(ValueError) as exc:
        write_file(str(file_path), data)
    assert "All columns must have the same number of rows" in str(exc.value)
