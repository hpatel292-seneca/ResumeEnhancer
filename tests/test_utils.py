from utils import read_txt_file
from unittest import mock
import pytest

## Test read_txt_file from Utils.read_txt_file


class Test_read_txt_file:
    @mock.patch("utils.open", new_callable=mock.mock_open, read_data="file content")
    def test_read_txt_file_valid(self, mock_open):
        result = read_txt_file("dummy.txt")
        assert result == "file content"

    @mock.patch(
        "utils.open", side_effect=FileNotFoundError
    )  # side_effect will raise exception when open is called.
    def test_read_txt_file_not_found(self, mock_open):
        with pytest.raises(FileNotFoundError):
            read_txt_file("missing.txt")

    @mock.patch("utils.open", new_callable=mock.mock_open, read_data="")
    def test_read_txt_file_empty(self, mock_open):
        result = read_txt_file("empty.txt")
        assert result == ""
