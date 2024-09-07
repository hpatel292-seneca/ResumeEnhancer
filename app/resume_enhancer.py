import sys
import argparse
import os

from utils import *
from config import *

def get_version():
    """
    Get the Version for cli tool using --version or -v

    Returns:
    str: version number
    """
    return (f"Resume Enhancer Tool {VERSION}")
    

## Main Function
def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Enhance resume with description")

    # Add the arguments
    parser.add_argument('--resume', help='Path to the resume file')
    parser.add_argument('--description', help='Path to the description file')

    # Add version arguments
    parser.add_argument('--version','-v', action='store_true')


    args=parser.parse_args()

    if args.version:
        print(get_version())
        return

    # Access the arguments
    resume_path = args.resume
    description_path = args.description

    if os.path.exists(resume_path) and os.path.exists(description_path):
        try:
            resume_content = read_file(resume_path)
            description_content = read_file(description_path)

            print("Resume Content: \n" + resume_content)
            print("Description: \n" + description_content)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Resume or job description at the given path does not exist")




if __name__ == '__main__':
    main()