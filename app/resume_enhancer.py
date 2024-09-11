import sys
import argparse
import os
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
    try:
        return f"""
        {TOOL_NAME} - A simple CLI tool for Enhancing your Resume based on job description

        Usage:
        py app/resume_enhancer.py [options]

        Options:
        -h, --help     show this help message
        -v, --version  print version
        --resume       Inputs Resume (Accepts pdf, txt, docx, or doc) (Required)
        --description  Inputs Job Description (Accepts pdf, txt, docx, or doc) (Required)
        --api_key, -a    Input Groq API key (Required)
        -m, --model          Input Model you want to use 
        -o, --output         Output response to provided file (Accepts .txt)
        -t, --temperature    Input Temperature to pass while making chat completion request.
        -mt, --maxTokens     Maximum number of Token.
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

def get_response(resume, description, api_key, model=None, temperature=0.5, max_token=1024):
    try:
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
            
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error in get_response: {e}")


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


    args=parser.parse_args()

    if args.help:
        print(get_help())
        return

    # Check if the version Flag is present
    if args.version:
        print(get_version())
        logger.info(get_version())
        return

    if not args.resume or not args.description or not args.api_key:
        print(usage_error(), file=sys.stderr)
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


    if os.path.exists(resume_path) and os.path.exists(description_path):
        try:
            resume_content = read_file(resume_path)
            description_content = read_file(description_path)
            response=get_response(resume=resume_content, description=description_content, api_key=api_key, model=args.model, temperature=temperature, max_token=maxTokens)
            if args.output:
                write_to_file(args.output, response)
            else:
                print(response)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Resume or job description at the given path does not exist")




if __name__ == '__main__':
    main()