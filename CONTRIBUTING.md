Here’s the updated **CONTRIBUTING.md** with the additional setup instructions and contributing guidelines included:

---

# Contributing to Resume Enhancer

Thank you for considering contributing to Resume Enhancer! This guide provides instructions for setting up the development environment and guidelines for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#1-clone-the-repository)
  - [Install Required Dependencies](#2-install-required-dependencies)
  - [Running the CLI Tool Locally](#3-running-the-cli-tool-locally)
  - [Running formatter](#4-Formatter)
  - [Testing](#6-testing)
- [I Have a Question](#i-have-a-question)
- [I Want to Contribute](#i-want-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Improving the Documentation](#improving-the-documentation)
- [Styleguides](#styleguides)
  - [Commit Messages](#commit-messages)

## Code of Conduct

This project and everyone participating in it is governed by the Resume Enhancer Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers at [your-email@example.com].

## Setup Instructions

### Prerequisites

1. **Python3**: Ensure `Python` is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
2. **Git**: Ensure Git is installed on your system. You can download it from [git-scm.com](https://git-scm.com/).
3. **Groq API Key**: You need a Groq API key to use this tool. You can get an API Key from [Groq](https://console.groq.com/playground).

### 1. Clone the Repository

```bash
git clone https://github.com/hpatel292-seneca/ResumeEnhancer
cd ResumeEnhancer
```

### 2. Install Required Dependencies

Install the necessary Python packages using pip:

```bash
pip install -r requirements.txt
```

This will install all required dependencies.

### 3. Running the CLI Tool Locally

Once the dependencies are installed, you can run the tool locally.

```bash
python app/resume_enhancer.py --resume path_to_resume --description path_to_description --api_key groq_api_key
```

### 4. Formatter

you can run the formatter on your entire project with:

```bash
#Make the script executable:
chmod +x format.sh

./format.sh
```

### 5. Lint

you can run the Lint on your entire project with:

```bash
#Make the script executable:
chmod +x lint.sh

./lint.sh
```

### 6. Testing

#### Running a Single Test or Test File

To run the tests use `pytest`. Naming of the test file should follow the naming convention `test_filename.py` and test cases of a function should be code in class `test_functionName.py`.

1. **Run a Single Test File**:
   To run a specific test file:

   ```bash
   pytest tests/test_file.py
   ```

2. **Run a Specific Test Function in a File**:
   To run a single test function within a file:
   ```bash
   pytest tests/test_file.py::className::test_function_name
   ```
   This command allows you to focus on a particular test function.

### Automatically Run Tests on Code Changes

To rerun tests automatically whenever you modify code or tests, you can use the `pytest-xdist` plugin:

- **Run `pytest` in Watch Mode**:
  Use the `--looponfail` option to rerun only failing tests automatically whenever the code changes:
  ```bash
  pytest --looponfail
  ```
  This option will watch test file and source code, automatically rerunning tests each time a file is updated.

## I Have a Question

If you want to ask a question, please make sure to:

1. Read the available documentation.
2. Search for existing issues that might address your question.
3. If you still need help, open a new issue with your question, providing as much context as possible, including project and platform versions (e.g., Python, npm).

## I Want to Contribute

### Reporting Bugs

To submit a bug report:

1. Open an issue with a clear title and detailed description.
2. Explain the expected behavior versus the actual behavior.
3. Provide the reproduction steps, including code snippets if relevant.

The project team will label the issue accordingly, and it will be addressed once the issue is reproducible.

### Suggesting Enhancements

To suggest a new feature or improvement:

1. Verify that you are using the latest version.
2. Ensure the feature isn’t already covered in the documentation.
3. Perform a search to check if a similar enhancement has been suggested.
4. If it hasn’t, open an issue with a descriptive title and detailed steps outlining the enhancement. Describe:
   - The current behavior and the improvement you’d like to see.
   - Why this enhancement would benefit most users.
   - Screenshots or GIFs (optional) to illustrate your idea.

### Improving the Documentation

Documentation improvements are always welcome! If you find sections that are unclear or lacking information, you can submit a pull request with your proposed updates.

## Styleguides

### Commit Messages

Follow these guidelines for writing commit messages:

- Use the present tense (e.g., “Add feature” not “Added feature”).
- Keep messages concise but descriptive.
- Include context where relevant.

## Contributing Guidelines

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -am 'Add new feature'`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Create a new Pull Request.

---
