"""
File Processing Script

This script:
1. Takes a description.txt file from 'downloads' folder
2. Extracts client information from it
3. Saves the JSON result to 'data' folder as description.txt.json
"""

import os
import json
import sys
from text_extractor import extract_client_info_from_text


def process_description_file(input_folder_path, output_folder_path):
    """
    Process a description.txt file from the input folder and save
    the extracted information as JSON in the output folder.

    Args:
        input_folder_path: Path to the folder containing description.txt
        output_folder_path: Path to save the resulting JSON file

    Returns:
        True if successful, False otherwise
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
    # Default folder paths
    input_folder_path = "downloads"
    output_folder_path = "data"

    # Allow overriding paths from command line
    if len(sys.argv) >= 3:
        input_folder_path = sys.argv[1]
        output_folder_path = sys.argv[2]

    # Process the file
    success = process_description_file(input_folder_path, output_folder_path)

    # Exit with appropriate code
    sys.exit(0 if success else 1)