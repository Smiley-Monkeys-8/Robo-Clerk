import json
import os
from robo_clerk.doc_processors.pdf import PDFProcessor


def process_pdf(input_folder_path, output_folder_path):
    """Process pdf document

    Args:
        input_folder_path (path): the path of the docs to be processed
        output_folder_path (_type_): destination folder
    """
    processor = PDFProcessor(input_folder_path)
    data = processor.run_pipeline()
    print("\nAll steps completed. Data retrieved:")
    os.makedirs(output_folder_path, exist_ok=True)
    with open(os.path.join(output_folder_path, "account.pdf.json"), "w") as json_from_pdf:
      pdf_pretty_json = json.dumps(data, indent=2)
      json_from_pdf.write(pdf_pretty_json)
    print(data)