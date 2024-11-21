# Resume Enhancer CLI Tool

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Usage](#usage)
- [Configuration File Usage](#configuration-file-usage)
- [Options](#options)
- [Error Handling](#error-handling)
- [Logging](#logging)
- [License](#license)

## Overview

The **Resume Enhancer** is a command-line interface (CLI) tool designed to optimize and tailor resumes based on specific job descriptions. By leveraging AI capabilities, this tool analyzes the content of a resume and compares it with a job description to suggest improvements, highlight relevant skills, and emphasize qualifications that match the desired role.

### Demo Video

[Demo](https://youtu.be/W5IWO4vnTKA)

## Features

- **Automated Resume Enhancement**: Analyzes resumes and job descriptions to provide tailored suggestions.
- **Multiple Input Formats**: Supports input files in various formats such as `.pdf`, `.txt`, `.docx`, and `.doc`.
- **Customizable AI Parameters**: Allows customization of AI model parameters like temperature, maximum tokens, and model choice.
- **Groq API Integration**: Uses the Groq API for chat-based AI model interactions.
- **Command-Line Options**: Includes various command-line options for ease of use, such as help, version, and output file specifications.

## Usage

You can use this tool by running it locally. Clone the repository and directly run the tool on your computer.

```bash
python app/resume_enhancer.py --resume path_to_resume --description path_to_description --api_key groq_api_key
```

### Configuration File Usage

This tool allows you to specify various settings through a configuration file, `~/.ResumeEnhancer.toml`, which can simplify your command-line usage and help manage your options in a centralized manner.

The configuration file should be created in your home directory and it is read upon execution. It allows you to set default values for various parameters such as the API key, paths to files, model options, and more.

#### Configuration File Format

The configuration file should be in TOML format. Below is an example of a configuration file (`~/.ResumeEnhancer.toml`):

```toml
api_key = "your_api_key_here"
resume = "path/to/your/resume.pdf"
description = "path/to/your/job_description.txt"
model = ["llama3-8b-8192"]
temperature = 0.5
maxTokens = 1024
output = "output/result.txt"
token_usage = true
stream = false
```

#### Specifying Paths

##### Absolute Paths

You can specify absolute paths in the configuration file. An absolute path points to a location in the file system from the root directory, which means it will always refer to the same file regardless of the current working directory.

**Example of an absolute path**:

```toml
resume = "/Users/username/Documents/my_resume.pdf"
description = "/Users/username/Documents/job_description.txt"
```

##### Relative Paths

You can also specify relative paths. A relative path points to a location relative to the current working directory from which you are running the tool. This can be useful for portability, allowing you to share your configuration without worrying about absolute paths that might differ between systems.

**Example of a relative path**:

```toml
resume = "documents/my_resume.pdf"
description = "documents/job_description.txt"
```

When using relative paths, ensure that the specified files are located in the correct directories relative to the directory from which you execute the tool.

### Options

| Option          | Shortcut | Type   | Description                                                                               | Default          |
| --------------- | -------- | ------ | ----------------------------------------------------------------------------------------- | ---------------- |
| `--version`     | `-v`     | Flag   | Print the version of the tool                                                             | -                |
| `--help`        | `-h`     | Flag   | Show the help message and exit                                                            | -                |
| `--resume`      | -        | PATH   | Path to the resume file (Required). Supports `.pdf`, `.txt`, `.docx`, or `.doc`.          | -                |
| `--description` | -        | PATH   | Path to the job description file (Required). Supports `.pdf`, `.txt`, `.docx`, or `.doc`. | -                |
| `--api_key`     | `-a`     | String | Groq API key (Required)                                                                   | -                |
| `--model`       | `-m`     | String | Model to be used for AI processing                                                        | `llama3-8b-8192` |
| `--output`      | `-o`     | PATH   | Specify an output file to save the response (Optional, accepts `.txt`)                    | None             |
| `--temperature` | `-t`     | Float  | Controls the randomness of the AI's responses (Optional)                                  | `0.5`            |
| `--maxTokens`   | `-mt`    | Int    | Maximum number of tokens for the AI response (Optional)                                   | `1024`           |
| `--models`      | -        | Flag   | List available models                                                                     | -                |
| `--token-usage` | `-tu`    | Flag   | Displays token usage statistics to the user via `stderr`                                  | -                |
| `--stream`      | `-s`     | Flag   | Allow Streaming of response                                                               | `No Streaming`   |

## Error Handling

- **Invalid Input Files**: The tool checks if the specified input files exist and are in the correct format.
- **API Key Validation**: If the API key is missing or invalid, the tool will prompt for correction.
- **Command-Line Errors**: Usage errors are reported with a helpful error message indicating the correct usage of the tool.

## Logging

The tool uses a logging system to track errors and important events. Logs are generated using the Python logging module and can be customized by modifying the `setup_logging()` function in the `utils` module.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/hpatel292-seneca/ResumeEnhancer/blob/main/LICENSE) file for details.

```

```
