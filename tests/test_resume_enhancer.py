from resume_enhancer import get_response, get_version  # type: ignore
from config import TOOL_NAME, VERSION  # type: ignore
from unittest import mock
from io import StringIO
import pytest  # type: ignore


## Test get_response from resume_enhancer.get_response


class Test_GetResponse:

    def setup_method(self):
        # Mock the Groq client and its completions method
        self.patcher = mock.patch("resume_enhancer.Groq")
        self.mock_groq = self.patcher.start()  # Start the patch

        self.mock_client_instance = mock.Mock()
        self.mock_groq.return_value = self.mock_client_instance
        self.mock_client_instance.chat.completions.create.return_value = [
            mock.Mock(
                choices=[mock.Mock(delta=mock.Mock(content="Mocked response content"))],
                x_groq=mock.Mock(
                    usage=mock.Mock(
                        completion_tokens=100,
                        prompt_tokens=50,
                        total_tokens=150,
                        comTestpletion_time=0.35,
                        prompt_time=0.15,
                        queue_time=0.1,
                        total_time=0.6,
                    )
                ),
            )
        ]

    def teardown_method(self):
        self.patcher.stop()  # Stop all patches after each test

    def test_get_response_valid(self):
        # Capture stdout to check the printed output
        with mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            get_response(
                resume="Sample Resume",
                description="Sample Job Description",
                api_key="test_api_key",
            )
            output = mock_stdout.getvalue()
        # Assert that the expected content is printed in the output
        assert "Mocked response content" in output

    def test_get_response_no_api_key(self):
        # Test that missing API key raises ValueError
        with pytest.raises(ValueError, match="API key is required"):
            get_response(
                resume="Sample Resume",
                description="Sample Job Description",
                api_key=None,
            )

    def test_get_response_no_resume(self):
        # Test that missing resume raises ValueError
        with pytest.raises(ValueError, match="Resume is missing"):
            get_response(
                description="Sample Job Description",
                api_key="test_api_key",
                resume=None,
            )

    def test_get_response_no_description(self):
        # Test that missing description raises ValueError
        with pytest.raises(ValueError, match="Description is required"):
            get_response(
                resume="Sample Resume", api_key="test_api_key", description=None
            )

    def test_get_response_default_model(self):
        # Test that it uses the default model when none is specified
        with mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            get_response(
                resume="Sample Resume",
                description="Sample Job Description",
                api_key="test_api_key",
            )

            output = mock_stdout.getvalue()

        assert "Processing with model: llama3-8b-8192" in output

    def test_get_response_multiple_model(self):
        # Test that it uses the default model when none is specified
        with mock.patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            get_response(
                resume="Sample Resume",
                description="Sample Job Description",
                api_key="test_api_key",
                models=["model1", "model2"],
            )

            output = mock_stdout.getvalue()

        assert "Processing with model: model1" in output
        assert "Processing with model: model2" in output

    def test_get_response_with_output(self):
        # Test with output specified, should call write_to_file
        with mock.patch("resume_enhancer.write_to_file") as mock_write:
            get_response(
                resume="Sample Resume",
                description="Sample Job Description",
                api_key="test_api_key",
                output=["output_filename"],
            )
            file_name = "output_filename_llama3-8b-8192.txt"
            mock_write.assert_called_once_with(file_name, "Mocked response content")

    def test_get_response_multiple_model_with_output(self):
        # Patch the write_to_file function
        with mock.patch("resume_enhancer.write_to_file") as mock_write:
            get_response(
                resume="Sample Resume",
                description="Sample Job Description",
                api_key="test_api_key",
                models=["model1", "model2"],
                output=["output_filename"],
            )

            # Define the expected file names and calls
            file_name_model1 = "output_filename_model1.txt"
            file_name_model2 = "output_filename_model2.txt"
            expected_calls = [
                mock.call(file_name_model1, "Mocked response content"),
                mock.call(file_name_model2, "Mocked response content"),
            ]

            # Use assert_has_calls to check for multiple calls in order
            mock_write.assert_has_calls(expected_calls, any_order=False)

    def test_get_response_with_token_usage(self):
        # Capture stderr to check for token usage info
        with mock.patch("sys.stderr", new_callable=StringIO) as mock_stderr:

            get_response(
                resume="Sample Resume",
                description="Sample Job Description",
                api_key="test_api_key",
                token_usage=True,
            )

            # Check if the token usage details were printed in stderr
            stderr_output = mock_stderr.getvalue()

        assert "Token Usage:" in stderr_output
        assert "- Completion Tokens: 100" in stderr_output
        assert "- Prompt Tokens: 50" in stderr_output
        assert "- Total Tokens: 150" in stderr_output
        assert "- Completion Time: 0.350 seconds" in stderr_output
        assert "- Prompt Time: 0.150 seconds" in stderr_output
        assert "- Queue Time: 0.100 seconds" in stderr_output
        assert "- Total Time: 0.600 seconds" in stderr_output

    def test_get_version(self):
        # Test that the version is returned correctly
        assert TOOL_NAME == "Resume Enhancer Tool"
        assert VERSION == "0.1.0"
        assert get_version() == f"{TOOL_NAME} {VERSION}"
