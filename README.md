![Resume Enhancer Logo](https://github.com/hpatel292-seneca/ResumeEnhancer/blob/main/assets/logo.png)

# Resume Enhancer CLI Tool

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Usage](#usage)
  - [Options](#options)
  - [Example](#example)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Error Handling](#error-handling)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)

## Overview

The **Resume Enhancer** is a command-line interface (CLI) tool designed to optimize and tailor resumes based on specific job descriptions. By leveraging AI capabilities, this tool analyzes the content of a resume and compares it with a job description to suggest improvements, highlight relevant skills, and emphasize qualifications that match the desired role.

## Features

- **Automated Resume Enhancement**: Analyzes resumes and job descriptions to provide tailored suggestions.
- **Multiple Input Formats**: Supports input files in various formats such as `.pdf`, `.txt`, `.docx`, and `.doc`.
- **Customizable AI Parameters**: Allows customization of AI model parameters like temperature, maximum tokens, and model choice.
- **Groq API Integration**: Uses the Groq API for chat-based AI model interactions.
- **Command-Line Options**: Includes various command-line options for ease of use, such as help, version, and output file specifications.

## Usage

You can use this tool by running it locally. Clone the repository and directly on your computer.

### Prerequisties
1. **Python3**: Ensure `Python` is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
2. **Git**: Ensure Git is installed on your system. You can download it from [git-scm.com](https://git-scm.com/).
3. **groq API Key**: You need groq API key to use this tool. You can get API Key from [groq](https://console.groq.com/playground)

### Setup Instructions
#### 1. Clone the Repository.
```bash
git clone https://github.com/hpatel292-seneca/ResumeEnhancer
cd ResumeEnhancer
```

#### 2. Install Required Dependencies
Install the necessary Python packges using pip

```bash
pip install -r requirements.txt
```
This will install all required dependencies

#### 3. Running the CLI tool locally
Once the dependencies are installed, you can run the tool locally.

```bash
python app/resume_enhancer.py --resume path_to_resume --description path_to_description --api_key groq_api_key
```

### Options
| Option             | Shortcut   | Type   | Description                                                                 | Default                |
|--------------------|------------|--------|-----------------------------------------------------------------------------|-------------------------|
| `--version`        | `-v`       | Flag   | Print the version of the tool                                               |  -                      |
| `--help`           | `-h`       | Flag   | Show the help message and exit                                              |  -                      |
| `--resume`         |  -         | PATH   | Path to the resume file (Required). Supports `.pdf`, `.txt`, `.docx`, or `.doc`. |  -                      |
| `--description`    |  -         | PATH   | Path to the job description file (Required). Supports `.pdf`, `.txt`, `.docx`, or `.doc`. |  -                      |
| `--api_key`        | `-a`       | String | Groq API key (Required)                                                     |  -                      |
| `--model`          | `-m`       | String | Model to be used for AI processing                                          | `llama3-8b-8192`        |
| `--output`         | `-o`       | PATH   | Specify an output file to save the response (Optional, accepts `.txt`)       | None                    |
| `--temperature`    | `-t`       | Float  | Controls the randomness of the AI's responses (Optional)                    | `0.5`                   |
| `--maxTokens`      | `-mt`      | Int    | Maximum number of tokens for the AI response (Optional)                     | `1024`                  |
