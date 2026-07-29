import pytest

from dataframe_pcg.file_handler import read_csv_file, read_dtype, write_file


# TEST_CASE_1
def test_read_csv_file_converts_supported_types_and_preserves_missing_values(tmp_path):
    file_path = tmp_path / "data.csv"
    file_path.write_text(
        "id,score,name,note\n1,2.5,Ada,\n-3,,Bob,unchanged\n",
        encoding="utf-8",
    )

    result = read_csv_file(
        file_path,
        {"id": "int", "score": "float", "name": "string"},
    )

    assert list(result) == ["id", "score", "name", "note"]
    assert result["id"] == [1, -3]
    assert result["score"][0] == pytest.approx(2.5)
    assert result["score"][1] is None
    assert result["name"] == ["Ada", "Bob"]
    assert result["note"] == [None, "unchanged"]


# TEST_CASE_2
def test_read_csv_file_ignores_dtype_for_absent_column_and_handles_duplicate_headers(
    tmp_path,
):
    file_path = tmp_path / "duplicate_headers.csv"
    file_path.write_text("a,a\n1,2\n", encoding="utf-8")

    result = read_csv_file(
        file_path,
        {"a": "int", "missing": "unsupported"},
    )

    assert result == {"a": [2, 2]}


# TEST_CASE_3
def test_read_csv_file_raises_for_unsupported_dtype_on_present_column(tmp_path):
    file_path = tmp_path / "data.csv"
    file_path.write_text("active\ntrue\n", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match=r"^Unsupported data type: boolean for column: active$",
    ):
        read_csv_file(file_path, {"active": "boolean"})


# TEST_CASE_4
def test_read_csv_file_empty_file_raises_type_error(tmp_path):
    file_path = tmp_path / "empty.csv"
    file_path.write_text("", encoding="utf-8")

    with pytest.raises(TypeError, match="NoneType"):
        read_csv_file(file_path, {})


# TEST_CASE_5
def test_read_dtype_overwrites_duplicates_and_preserves_unvalidated_values(tmp_path):
    file_path = tmp_path / "dtypes.csv"
    file_path.write_text(
        "column,dtype\nid,int\nactive,boolean\nid,string\nmissing,\n",
        encoding="utf-8",
    )

    result = read_dtype(file_path)

    assert result == {
        "id": "string",
        "active": "boolean",
        "missing": "",
    }


# TEST_CASE_6
def test_read_dtype_empty_file_returns_empty_dictionary(tmp_path):
    file_path = tmp_path / "empty.csv"
    file_path.write_text("", encoding="utf-8")

    result = read_dtype(file_path)

    assert result == {}


# TEST_CASE_7
def test_write_file_writes_header_rows_quoted_values_and_empty_none(tmp_path):
    file_path = tmp_path / "output.csv"
    data = {
        "id": [1, 2],
        "name": ["Ada, Jr.", None],
        "score": [1.5, -2.0],
    }

    result = write_file(file_path, data)

    assert result is None
    assert file_path.read_text(encoding="utf-8") == (
        'id,name,score\n1,"Ada, Jr.",1.5\n2,,-2.0\n'
    )


# TEST_CASE_8
def test_write_file_rejects_empty_and_unequal_columns_before_touching_target(
    tmp_path,
):
    file_path = tmp_path / "output.csv"
    file_path.write_text("existing content", encoding="utf-8")

    with pytest.raises(ValueError, match=r"^No data to write$"):
        write_file(file_path, {})

    assert file_path.read_text(encoding="utf-8") == "existing content"

    with pytest.raises(
        ValueError,
        match=r"^All columns must have the same number of rows$",
    ):
        write_file(file_path, {"a": [1], "b": [2, 3]})

    assert file_path.read_text(encoding="utf-8") == "existing content"
