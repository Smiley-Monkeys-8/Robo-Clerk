from dataclasses import asdict
import json
import os
from robo_clerk.doc_processors.docx import DOCXProcessor
from robo_clerk.doc_processors.pdf import PDFProcessor
from robo_clerk.doc_processors.png import PNGProcessor
from robo_clerk.doc_processors.process_file_sambanova import TXTProcessorSambanova
from robo_clerk.doc_processors.text_extractor import TXTProcessor
from robo_clerk.doc_processors.types import Feature
from robo_clerk.utils.file import FileType, get_file_name, get_file_type, list_files_in_folder

# For simplicity define consts as the name of the docs

def get_document_processor(file_type: FileType):
    if (file_type == FileType.PDF):
        return PDFProcessor
    if (file_type == FileType.DOCX):
        return DOCXProcessor
    if (file_type == FileType.PNG):
        return PNGProcessor
    if (file_type == FileType.TXT):
        # return TXTProcessor   
        return TXTProcessorSambanova
    
    return None

def flatten(feature: Feature):  
    return {
        f"{feature.key}_{get_file_name(feature.source)}": feature.value
    }
    

def process_document(file_path: str, output_folder_path, output_file="client_data.json"):
    file_name =get_file_name(file_path)
    file_type = get_file_type(file_name)
    file_processor = get_document_processor(file_type)
    if file_processor is None:
        print(f"no file processor for {file_path}")
        return
    features = file_processor(file_path).run_pipeline()
    try:
        data = {f"{feature.key}_{get_file_name(feature.source)}": feature.value for feature in features}
    except:
        print("could not process features")
        return
    os.makedirs(output_folder_path, exist_ok=True)
    
    with open(os.path.join(output_folder_path, output_file), "r") as json_output:
      existing_data = json.load(json_output)
        
    with open(os.path.join(output_folder_path, output_file), "w") as json_output:
      data_pretty_json = json.dumps({**existing_data, **data}, indent=2)
      json_output.write(data_pretty_json)

def list_files_in_folder(folder_path: str):
    for entry in os.listdir(folder_path):
        full_path = os.path.join(folder_path, entry)
        if os.path.isfile(full_path):
            yield full_path

def get_file_name(file_path: str) -> str:
    return os.path.basename(file_path)

def process_documents(input_folder_path, output_folder_path, output_file="client_data.json"):
    os.makedirs(output_folder_path, exist_ok=True)

    with open(os.path.join(output_folder_path, output_file), "w") as output_json:
        output_json.write("{}")
    for file_path in list_files_in_folder(input_folder_path):
        process_document(file_path, output_folder_path, output_file=output_file)
