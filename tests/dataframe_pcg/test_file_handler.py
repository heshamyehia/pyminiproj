import pytest

from dataframe_pcg.file_handler import read_csv_file, read_dtype, write_file


# TEST_CASE_1
def test_read_csv_file_basic_conversion(tmp_path):
    file = tmp_path / "data.csv"
    content = "a,b,c\n1,2.5,foo\n3,,bar\n"
    file.write_text(content, encoding="utf-8")

    dtypes = {"a": "int", "b": "float", "c": "string"}
    result = read_csv_file(str(file), dtypes)

    assert result["a"] == [1, 3]
    assert result["b"][0] == pytest.approx(2.5)
    assert result["b"][1] is None
    assert result["c"] == ["foo", "bar"]


# TEST_CASE_3
def test_read_dtype_basic(tmp_path):
    file = tmp_path / "types.csv"
    content = "column,dtype\nage,int\nheight,float\nname,string\n"
    file.write_text(content, encoding="utf-8")

    result = read_dtype(str(file))
    assert result == {"age": "int", "height": "float", "name": "string"}


# TEST_CASE_4
def test_write_file_normal_roundtrip(tmp_path):
    data = {"col1": [1, None, 3], "col2": ["a", "b", "c"], "col3": [1.5, None, 2.5]}
    out = tmp_path / "out.csv"
    write_file(str(out), data)

    # Read back without importing csv module (to adhere to test constraints)
    content = out.read_text(encoding="utf-8").splitlines()
    expected_lines = [
        "col1,col2,col3",
        "1,a,1.5",
        ",b,",
        "3,c,2.5",
    ]
    assert content == expected_lines


# TEST_CASE_5
def test_write_file_no_data_raises(tmp_path):
    out = tmp_path / "empty.csv"
    with pytest.raises(ValueError) as excinfo:
        write_file(str(out), {})
    assert "No data to write" in str(excinfo.value)


# TEST_CASE_6
def test_write_file_unequal_lengths_raises(tmp_path):
    data = {"a": [1, 2], "b": [3]}
    out = tmp_path / "bad.csv"
    with pytest.raises(ValueError) as excinfo:
        write_file(str(out), data)
    assert "All columns must have the same number of rows" in str(excinfo.value)
