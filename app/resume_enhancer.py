import argparse
import json
import os
import sys

import requests  # type: ignore
from config import TOOL_NAME, VERSION
from groq import Groq  # type: ignore
from halo import Halo  # type: ignore
from utils import write_to_file, read_file, setup_logging, read_toml_config, get_help

# Setup logger
logger = setup_logging()

# Path for the configuration file
CONFIG_PATH = os.path.expanduser("~/.ResumeEnhancer.toml")


def get_version():
    try:
        return f"{TOOL_NAME} {VERSION}"
    except Exception as e:
        logger.error("Failed to get_version", e)


# Using Halo as a decorator
# Ref Doc: https://github.com/manrajgrover/halo?tab=readme-ov-file#usage
# @Halo(text="Processing...", spinner="dots")
def get_response(
    resume,
    description,
    api_key,
    models=None,
    temperature=0.5,
    max_token=1024,
    output=None,
    token_usage=False,
    stream=False,
):
    spinner = Halo(text="Processing", spinner="dots")

    if api_key is None:
        raise ValueError("API key is required")

    if resume is None:
        raise ValueError("Resume is missing")

    if description is None:
        raise ValueError("Description is required")

    if not models:
        models = ["llama3-8b-8192"]

    for model in models:
        print(f"Processing with model: {model}")
        spinner.start()
        try:
            client = Groq(api_key=api_key)

            system_message = {
                "role": "system",
                "content": "You are an AI assistant specializing in optimizing resumes to align with specific job descriptions...",
            }

            user_message = {
                "role": "user",
                "content": f"""
                    Resume:
                    {resume}

                    Job Description:
                    {description}
                """,
            }

            chat_completion = client.chat.completions.create(
                messages=[system_message, user_message],
                model=model,
                temperature=temperature,
                max_tokens=max_token,
                stream=True,
            )
            content = ""
            spinner.stop()
            print("\n")
            if not output:
                print(f"\n\nModel: {model}")
            for chunk in chat_completion:
                chunk_content = chunk.choices[0].delta.content
                if chunk_content:
                    if output or stream is False:
                        content += chunk_content
                    else:
                        print(chunk_content, end="")

            if output:
                if len(output) == 1:
                    write_to_file(f"{output[0]}_{model}.txt", content)
                else:
                    write_to_file(f"{output[0]}_{model}.{output[1]}", content)
            elif stream is False:
                # Print all the fetched content on the screen
                print(content)

            # Print colored token usage info
            # Ref Doc: https://codehs.com/tutorial/andy/ansi-colors
            if token_usage:
                usage = chunk.x_groq.usage

                formatted_usage = (
                    "\n\033[92m"
                    "Token Usage:\n"
                    "-------------\n"
                    f"- Completion Tokens: {usage.completion_tokens}\n"
                    f"- Prompt Tokens: {usage.prompt_tokens}\n"
                    f"- Total Tokens: {usage.total_tokens}\n\n"
                    "Timing:\n"
                    "-------\n"
                    f"- Completion Time: {usage.completion_time:.3f} seconds\n"
                    f"- Prompt Time: {usage.prompt_time:.3f} seconds\n"
                    f"- Queue Time: {usage.queue_time:.3f} seconds\n"
                    f"- Total Time: {usage.total_time:.3f} seconds\n"
                    "\033[0m"
                )

                print(formatted_usage, file=sys.stderr)

        except Exception as e:
            logger.error(f"Error in get_response: {e}")


def check_models(api_key):
    url = "https://api.groq.com/openai/v1/models"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    print(json.dumps(response.json(), indent=4))


def prompt_for_missing_args(cli_arguments, config):
    if not cli_arguments.api_key and not config.get("api_key"):
        cli_arguments.api_key = input("Please enter your API key: ")

    if not cli_arguments.resume and not config.get("resume"):
        cli_arguments.resume = input("Please enter the path to the resume file: ")

    if not cli_arguments.description and not config.get("description"):
        cli_arguments.description = input(
            "Please enter the path to the job description file: "
        )

    return cli_arguments


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Enhance resume with description", add_help=False
    )

    # Add the arguments
    parser.add_argument("--help", "-h", action="store_true")
    parser.add_argument("--version", "-v", action="store_true")
    parser.add_argument("--resume", help="Path to the resume file")
    parser.add_argument("--description", help="Path to the description file")
    parser.add_argument(
        "--api_key", "-a", help="API key required for accessing external services"
    )
    parser.add_argument(
        "--model", "-m", nargs="+", help="Specify one or more models to use"
    )
    parser.add_argument(
        "--output", "-o", help="allow the user to specify an output file"
    )
    parser.add_argument(
        "--temperature", "-t", help="Controls randomness of completions", type=float
    )
    parser.add_argument(
        "--maxTokens", "-mt", help="The maximum number of tokens to generate", type=int
    )
    parser.add_argument("--models", action="store_true", help="List available models")
    parser.add_argument(
        "--token-usage", "-tu", action="store_true", help="Show token usage"
    )
    parser.add_argument("--stream", "-s", action="store_true", help="Allow streaming")
    return parser.parse_args()


## Main Function
def main():
    # Load configuration from the TOML file
    config = read_toml_config(CONFIG_PATH)

    # Get CLI cli_arguments
    cli_arguments = parse_arguments()

    if cli_arguments.help:
        print(get_help())
        return

    if cli_arguments.version:
        print(get_version())
        return

    # Apply configuration from TOML file if CLI arguments are not provided
    api_key = cli_arguments.api_key or config.get("api_key")
    resume = cli_arguments.resume or config.get("resume")
    description = cli_arguments.description or config.get("description")
    models = cli_arguments.model or config.get("model", ["llama3-8b-8192"])
    temperature = cli_arguments.temperature or config.get("temperature", 0.5)
    max_tokens = cli_arguments.maxTokens or config.get("maxTokens", 1024)
    output = cli_arguments.output or config.get("output", None)
    token_usage = cli_arguments.token_usage or config.get("token_usage", False)
    stream = cli_arguments.stream or config.get("stream", False)

    if cli_arguments.models:
        if not api_key:
            logger.error("You must specify an API key")
            return
        check_models(api_key)
        return

    cli_arguments = prompt_for_missing_args(cli_arguments, config)

    if not resume:
        logger.error("You must provide a resume path for processing")
        return

    if not description:
        logger.error("You must provide a job description file path for processing")
        return

    if not os.path.exists(resume):
        logger.error("Could not find resume file at provided path")
        return

    if not os.path.exists(description):
        logger.error("Could not find description file at provided path")
        return

    try:
        parsed_resume_content = read_file(resume)
        parsed_job_description = read_file(description)
        if output:
            output = output.split(".")
        else:
            output = None

        get_response(
            resume=parsed_resume_content,
            description=parsed_job_description,
            api_key=api_key,
            models=models,
            temperature=temperature,
            max_token=max_tokens,
            output=output,
            token_usage=token_usage,
            stream=stream,
        )
    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == "__main__":
    main()
