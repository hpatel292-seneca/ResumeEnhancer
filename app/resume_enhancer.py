import sys
import argparse
import os

from utils import *

## Main Function
def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Enhance resume with description")

    # Add the arguments
    parser.add_argument('--resume', required=True, help='Path to the resume file')
    parser.add_argument('--description', required=True, help='Path to the description file')

    args=parser.parse_args()

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
        print("Resume or job description not exist")




if __name__ == '__main__':
    main()