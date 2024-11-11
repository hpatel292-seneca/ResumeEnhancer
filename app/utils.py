import logging
import os

import tomllib
from colorama import Fore, Style
from docx import Document  # type: ignore
from pypdf import PdfReader  # type: ignore
from config import TOOL_NAME


# Custom formatter for colorized logging
class ColoredFormatter(logging.Formatter):
    COLORS = {
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, Fore.WHITE)
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"


def write_to_file(file_path, content):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".txt":
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    elif extension == "":
        with open(file_path + ".txt", "w", encoding="utf-8") as f:
            f.write(content)
    else:
        raise ValueError(
            f"Unsupported outfile type: {extension}, only .txt files are supported"
        )


def read_txt_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return content


def read_pdf_file(file_path):
    content = ""
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        for page in range(len(reader.pages)):
            content += reader.pages[page].extract_text()
    return content


def read_word_file(file_path):
    doc = Document(file_path)
    content = "\n".join([para.text for para in doc.paragraphs])
    return "Hello" + content


def read_file(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".txt":
        return read_txt_file(file_path)
    elif extension == ".pdf":
        return read_pdf_file(file_path)
    elif extension in [".doc", ".docx"]:
        return read_word_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {extension}")


# set up logger
def setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Check if handlers are already present to avoid duplication
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger


# Setup logger
logger = setup_logging()


# Read configuration from TOML file
def read_toml_config(config_path):
    logger = setup_logging()

    try:
        with open(config_path, "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        logger.warning(
            f"Configuration file not found at {config_path}. Using default settings."
        )
        return {}
    except Exception as e:
        logger.error(f"Failed to read config file: {e}")
        return {}


def get_help():
    ascii_log = r"""
 ____                                _____       _
|  _ \ ___  ___ _   _ _ __ ___   ___| ____|_ __ | |__   __ _ _ __   ___ ___ _ __
| |_) / _ \/ __| | | | '_ ` _ \ / _ \  _| | '_ \| '_ \ / _` | '_ \ / __/ _ \ '__|
|  _ <  __/\__ \ |_| | | | | | |  __/ |___| | | | | | | (_| | | | | (_|  __/ |
|_| \_\___||___/\__,_|_| |_| |_|\___|_____|_| |_|_| |_|\__,_|_| |_|\___\___|_|
    """
    try:
        return f"""
        {ascii_log}

        {TOOL_NAME} - A CLI tool for enhancing resumes based on job descriptions

        Usage:
        py app/resume_enhancer.py [options]

        Options:
        -h, --help            Show this help message
        -v, --version         Print version
        --models              List available models
        --resume              Input resume (pdf, txt, docx, doc) (Required)
        --description         Input job description (pdf, txt, docx, doc) (Required)
        --api_key, -a         Input Groq API key (Required)
        -m, --model           Specify model to use
        -o, --output          Output to specified file (txt or json)
        -t, --temperature     Set completion randomness (default 0.5)
        -mt, --maxTokens      Maximum number of tokens (default 1024)
        --token-usage         Print token usage information

        Examples:
        1. Basic Usage:
           py app/resume_enhancer.py --resume resume.docx --description description.txt --api_key YOUR_API_KEY

        2. Specify Model and Output:
           py app/resume_enhancer.py --resume resume.pdf --description description.pdf --api_key YOUR_API_KEY --model llama3-8b-8192 --output output.txt

        Note: Get your Groq API key from https://groq.com/developers
        """

    except Exception as e:
        logger.error("Failed to get_help", e)


def usage_error():
    try:
        return f"""
        Error: Incorrect usage of {TOOL_NAME}.

        Usage:
        py app/resume_enhancer.py [options]
        """
    except Exception as e:
        logger.error("Failed to usage_error", e)
