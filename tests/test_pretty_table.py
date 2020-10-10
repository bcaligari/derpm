import pytest
from common import pretty_table

table_null = []
table_null_out_csv = []
table_null_out_ascii = []
table_null_colnames = ["id", "desc"]

table_just_headers_out_csv = ["id,desc"]

table_just_headers_out_ascii = [
    "id | desc",
    "-- | ----",
]


def test_table_0_csv():
    assert pretty_table(table_null) == table_null_out_csv


def test_table_0_ascii():
    assert pretty_table(table_null, fmt="ascii") == table_null_out_ascii


def test_table_just_headers_csv():
    assert (
        pretty_table(table_null, colnames=table_null_colnames)
        == table_just_headers_out_csv
    )


def test_table_just_headers_ascii():
    assert (
        pretty_table(table_null, fmt="ascii", colnames=table_null_colnames)
        == table_just_headers_out_ascii
    )


table_3x1 = [["line0"], ["line1"], ["line2"]]

table_3x1_colnames = ["whatever"]

table_3x1_no_header = ["line0", "line1", "line2"]

table_3x1_csv_header = ["whatever", "line0", "line1", "line2"]

table_3x1_ascii_header = ["whatever", "--------", "line0", "line1", "line2"]


def test_table_3x1_no_header_csv():
    assert pretty_table(table_3x1) == table_3x1_no_header


def test_table_3x1_no_header_ascii():
    assert pretty_table(table_3x1, fmt="ascii") == table_3x1_no_header


def test_table_3x1_header_csv():
    assert pretty_table(table_3x1, colnames=table_3x1_colnames) == table_3x1_csv_header


def test_table_3x1_header_ascii():
    assert (
        pretty_table(table_3x1, colnames=table_3x1_colnames, fmt="ascii")
        == table_3x1_ascii_header
    )


def test_table_wrong_column_count_more():
    with pytest.raises(IndexError):
        pretty_table(table_3x1, colnames=["zero", "one"])


table_3x2 = [[0, "line0"], [1, "line1"], [2, "line2"]]

table_3x2_colnames = ["meh", "blah"]

table_3x2_no_header = ["0,line0", "1,line1", "2,line2"]

table_3x2_csv_header = ["meh,blah", "0,line0", "1,line1", "2,line2"]

table_3x2_ascii_header = [
    "meh | blah",
    "--- | -----",
    "0   | line0",
    "1   | line1",
    "2   | line2",
]

table_3x2_ascii_no_header = ["0 | line0", "1 | line1", "2 | line2"]


def test_table_wrong_column_count_less():
    with pytest.raises(IndexError):
        pretty_table(table_3x2, colnames=["oops"])


def test_table_3x2_no_header_csv():
    assert pretty_table(table_3x2) == table_3x2_no_header


def test_table_3x2_no_header_ascii():
    assert pretty_table(table_3x2, fmt="ascii") == table_3x2_ascii_no_header


def test_table_3x2_header_csv():
    assert pretty_table(table_3x2, colnames=table_3x2_colnames) == table_3x2_csv_header


def test_table_3x2_header_ascii():
    assert (
        pretty_table(table_3x2, colnames=table_3x2_colnames, fmt="ascii")
        == table_3x2_ascii_header
    )


table_2x5 = [[0, "meh", 2, 65535, 666], [1, "blah", 10, 500, 17]]

table_2x5_colnames = ["id", "description", "min", "max", "median"]

table_2x5_ascii_header = [
    "id | description | min | max   | median",
    "-- | ----------- | --- | ----- | ------",
    "0  | meh         | 2   | 65535 | 666",
    "1  | blah        | 10  | 500   | 17",
]


def test_table_2x5_header_ascii():
    assert (
        pretty_table(table_2x5, colnames=table_2x5_colnames, fmt="ascii")
        == table_2x5_ascii_header
    )
