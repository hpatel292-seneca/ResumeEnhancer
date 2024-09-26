import argparse
import json
import os
import sys

import requests
from config import *
from groq import Groq
from halo import Halo
from utils import *

# Setup logger
logger = setup_logging()


def get_version():
    try:
        return f"{TOOL_NAME} {VERSION}"
    except Exception as e:
        logger.error("Failed to get_version", e)


def get_help():
    ascii_log = """
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


# Using Halo as a decorator
# Ref Doc: https://github.com/manrajgrover/halo?tab=readme-ov-file#usage
# @Halo(text="Processing...", spinner="dots")
def get_response(
    resume,
    description,
    api_key,
    model=None,
    temperature=0.5,
    max_token=1024,
    output=None,
    token_usage=False,
    stream=False
):
    spinner=Halo(text="Processing", spinner='dots')
    try:
        spinner.start()
        if api_key is None:
            raise ValueError("API key is required")

        if resume is None:
            raise ValueError("Resume is missing")

        if description is None:
            raise ValueError("Description is required")

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
            model=model if model else "llama3-8b-8192",
            temperature=temperature,
            max_tokens=max_token,
            stream=True,
        )
        content = ""
        spinner.stop()
        print("\n")
        for chunk in chat_completion:
            chunk_content = chunk.choices[0].delta.content
            if chunk_content:
                if output or stream==False:
                    content += chunk_content
                else:
                    print(chunk_content, end="")

        if output:
            write_to_file(output, content)
        elif stream==False:
        # Print all the fetched content on the screen
            print("\n\n", content)

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


def prompt_for_missing_args(args):
    if not args.api_key:
        args.api_key = input("Please enter your API key: ")

    if not args.resume:
        args.resume = input("Please enter the path to the resume file: ")

    if not args.description:
        args.description = input("Please enter the path to the job description file: ")

    return args


## Main Function
def main():
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
    parser.add_argument("--model", "-m", help="Model to send requests to")
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
    parser.add_argument(
        "--stream", "-s", action="store_true", help="Allow streaming"
    )
    args = parser.parse_args()

    if args.help:
        print(get_help())
        return

    if args.version:
        print(get_version())
        return

    if args.models:
        if not args.api_key:
            logger.error("You must specify an API key")
            return
        check_models(args.api_key)
        return

    args = prompt_for_missing_args(args)

    if not args.resume:
        logger.error("You must provide a resume path for processing")
        return

    if not args.description:
        logger.error("You must provide a job description file path for processing")
        return

    if not os.path.exists(args.resume):
        logger.error("Could not find resume file at provided path")
        return

    if not os.path.exists(args.description):
        logger.error("Could not find description file at provided path")
        return

    try:
        resume_content = read_file(args.resume)
        description_content = read_file(args.description)

        get_response(
            resume=resume_content,
            description=description_content,
            api_key=args.api_key,
            model=args.model,
            temperature=args.temperature,
            max_token=args.maxTokens,
            output=args.output,
            token_usage=args.token_usage,
            stream=args.stream
        )
    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == "__main__":
    main()
