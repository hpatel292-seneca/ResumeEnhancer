from utils import read_txt_file, read_pdf_file
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


# Test read_pdf_file function
class Test_read_pdf_file:
    @mock.patch("utils.open", new_callable=mock.mock_open, read_data=b"%PDF-1.4")
    @mock.patch("utils.PdfReader")
    def test_read_pdf_file_valid(self, mock_pdf_reader, mock_open):
        # Mocking PdfReader to simulate PDF content
        mock_reader_instance = mock_pdf_reader.return_value
        mock_reader_instance.pages = [
            mock.Mock(extract_text=mock.Mock(return_value="Page content"))
        ]

        result = read_pdf_file("dummy.pdf")
        assert result == "Page content"

    @mock.patch("utils.open", side_effect=FileNotFoundError)
    def test_read_pdf_file_not_found(self, mock_open):
        with pytest.raises(FileNotFoundError):
            read_pdf_file("missing.pdf")
