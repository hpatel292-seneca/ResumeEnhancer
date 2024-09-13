import sys
import argparse
import os
import requests
import json
from halo import Halo
from groq import Groq
from utils import *
from config import *

# Setup logger
logger=setup_logging()

def get_version():
    """
    Get the Version for cli tool using --version or -v

    Returns:
    str: version number
    """
    try:
        return (f"{TOOL_NAME} {VERSION}")
    except Exception as e:
        logger.error("Failed to get_version", e)

def get_help():
    """
    Get Help for cli tool
    Returns:
    str: help message
    """
    ascii_log= """
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
    """
    Generates a usage error message for incorrect command-line arguments.

    Returns:
    str: The usage error message.
    """
    try:
        return f"""
        Error: Incorrect usage of {TOOL_NAME}.

        Usage:
        py app/resume_enhancer.py [options]

        Options:
        -h, --help           Show this help message
        -v, --version        Print version
        --models             Print Avaliable Models
        --resume             Inputs Resume (Accepts pdf, txt, docx, or doc) (Required)
        --description        Inputs Job Description (Accepts pdf, txt, docx, or doc) (Required)
        -a, --api_key        Input Groq API key (Required)
        -m, --model          Input Model you want to use 
        -o, --output         Output response to provided file (Accepts .txt)
        -t, --temperature    Input Temperature to pass while making chat completion request.
        -mt, --maxTokens     Maximum number of Token.

        Example:
        py app/resume_enhancer.py --resume path/to/resume.docx --description path/to/description.txt --api_key api_key
        """
    except Exception as e:
        logger.error("Failed to usage_error", e)

def get_response(resume, description, api_key, model=None, temperature=0.5, max_token=1024, output=None):
    # Setup Halo
    spinner=Halo(text="Processing", spinner='dots')
    try:
        spinner.start() # Start Halo Spinner
        if api_key is None:
            raise ValueError("API key is required")

        if resume is None:
            raise ValueError("Resume is missing")

        if description is None:
            raise ValueError("Description is required")

        client=Groq(api_key=api_key,)

        system_message = {
            "role": "system",
            "content": "You are an AI assistant specializing in optimizing resumes to align with specific job descriptions. Your task is to analyze the provided resume and job description, highlight relevant skills, experiences, and keywords, and suggest improvements to tailor the resume for the job. If the resume lacks required experience, do not fabricate or add fake experience. Ensure that required skills are prominently displayed first in the relevant sections. Retain all certifications included in the resume, and suggest reordering or restructuring content to emphasize qualifications that match the job description."
        }

        user_message={
            "role": "user",
            "content": f"""
                Resume:
                {resume}

                Job Description:
                {description}

                Please review the resume and suggest changes to better match the job description, including adjustments to the summary, skills, experience, and any relevant sections.

            """
        }

        chat_completion=client.chat.completions.create(
            messages=[
                system_message,
                user_message,
            ],
            model= model if model else "llama3-8b-8192",
            temperature=temperature,
            max_tokens=max_token,
            stream=True,
        )
        content=""
        for chunk in chat_completion:
            chunk_content = chunk.choices[0].delta.content  # Store the content in a variable
            if chunk_content:  # Check if chunk_content is not None or empty
                if output is None:
                    print(chunk_content, end="")
                else:
                    content += chunk_content  # Append content for writing to file
        if output is not None:
            write_to_file(output, content)

        # return chat_completion.choices[0].message.content
    except Exception as e:
        spinner.fail("Error in get_response")
        logger.error(f"Error in get_response: {e}")
    finally:
        spinner.stop()

def check_models(api_key):
    url = "https://api.groq.com/openai/v1/models"
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response=requests.get(url, headers=headers)
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
    # Create the parser
    parser = argparse.ArgumentParser(description="Enhance resume with description", add_help=False)

    # Add the arguments
    parser.add_argument('--help','-h', action='store_true')
    parser.add_argument('--version','-v', action='store_true')
    parser.add_argument('--resume', help='Path to the resume file')
    parser.add_argument('--description', help='Path to the description file')
    parser.add_argument('--api_key', '-a', help='API key required for accessing external services')
    parser.add_argument('--model', '-m', help='Model to send requests to')
    parser.add_argument('--output', '-o', help='allow the user to specify an output file')
    parser.add_argument('--temperature', '-t', help='allow to Controls randomness: lowering results in less random completions')
    parser.add_argument('--maxTokens', '-mt', help='The maximum number of tokens to generate')
    parser.add_argument('--models', action='store_true', help='List available models')

    args=parser.parse_args()

    if args.help:
        print(get_help())
        return

    # Check if the version Flag is present
    if args.version:
        print(get_version())
        return
    
    if args.models:
        if not args.api_key:
            logger.error("You must specify a api key")
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

    # Access the arguments
    resume_path = args.resume
    description_path = args.description
    api_key = args.api_key
    temperature = args.temperature
    maxTokens = args.maxTokens
    if temperature:
        temperature = float(args.temperature)
    
    if maxTokens:
        maxTokens = int(args.maxTokens)
    
    if not os.path.exists(resume_path):
        logger.error("Could not find resume file at provided path")
        return

    if not os.path.exists(description_path):
        logger.error("Could not find description file at provided path")
        return
    
    try:
        resume_content = read_file(resume_path)
        description_content = read_file(description_path)

        
        get_response(resume=resume_content, description=description_content, api_key=api_key, model=args.model, temperature=temperature, max_token=maxTokens, output=args.output)
    except Exception as e:
        logger.error(f"Error: {e}")




if __name__ == '__main__':
    main()