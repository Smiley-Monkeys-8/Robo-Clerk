"""
Usage from project root:
    poetry run python3 src/robo_clerk/doc_processors/process_file.py
"""

import os
import json
import sys
from text_extractor import extract_client_info_from_text


def process_description_file(input_folder_path, output_folder_path):
    """
    Process a description.txt file from the input folder and save
    the extracted information as JSON in the output folder.
    """
    # Ensure folders exist
    if not os.path.exists(input_folder_path):
        print(f"Error: Input folder '{input_folder_path}' does not exist.")
        return False

    if not os.path.exists(output_folder_path):
        print(f"Creating output folder '{output_folder_path}'...")
        os.makedirs(output_folder_path)

    # Define file paths
    input_file_path = os.path.join(input_folder_path, "description.txt")
    output_file_path = os.path.join(output_folder_path, "description.txt.json")

    # Check if input file exists
    if not os.path.exists(input_file_path):
        print(f"Error: Input file '{input_file_path}' not found.")
        return False

    try:
        # Read input file
        with open(input_file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()

        # Extract client information
        client_info = extract_client_info_from_text(text_content)

        # Save JSON output
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(client_info, file, indent=2, ensure_ascii=False)

        print(f"Success: Processed '{input_file_path}' and saved result to '{output_file_path}'")

        return True

    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return False


if __name__ == "__main__":
    # Default paths based on your project structure
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    default_input_path = os.path.join(project_root, "downloads")
    default_output_path = os.path.join(project_root, "data")

    # Allow overriding paths from command line
    if len(sys.argv) >= 3:
        input_folder_path = sys.argv[1]
        output_folder_path = sys.argv[2]
    else:
        input_folder_path = default_input_path
        output_folder_path = default_output_path

    # Print paths for verification
    print(f"Processing files from: {input_folder_path}")
    print(f"Saving results to: {output_folder_path}")

    # Process the file
    success = process_description_file(input_folder_path, output_folder_path)

    # Exit with appropriate code
    sys.exit(0 if success else 1)