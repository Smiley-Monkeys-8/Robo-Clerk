from dataclasses import asdict, dataclass
from enum import Enum
import json
import os
from robo_clerk.doc_processors.docx import DOCXProcessor
from robo_clerk.doc_processors.pdf import PDFProcessor
from robo_clerk.doc_processors.png import PNGProcessor
from robo_clerk.doc_processors.text_extractor import TXTProcessor

# For simplicity define consts as the name of the docs

class FileType(Enum):
    DOCX = 'docx'
    PDF = 'pdf'
    TXT = 'txt'
    PNG = 'png'

def get_file_type(filename: str) -> FileType | None:
    ext = filename.lower().split('.')[-1]
    for filetype in FileType:
        if filetype.value == ext:
            return filetype
    return None

def get_document_processor(file_type: FileType):
    if (file_type == FileType.PDF):
        return PDFProcessor
    if (file_type == FileType.DOCX):
        return DOCXProcessor
    if (file_type == FileType.PNG):
        return PNGProcessor
    if (file_type == FileType.TXT):
        return TXTProcessor   
    
    return None

def list_files_in_folder(folder_path: str):
    for entry in os.listdir(folder_path):
        full_path = os.path.join(folder_path, entry)
        if os.path.isfile(full_path):
            yield full_path

def get_file_name(file_path: str) -> str:
    return os.path.basename(file_path)

def process_document(file_path: str, output_folder_path):
    file_name =get_file_name(file_path)
    file_type = get_file_type(file_name)
    file_processor = get_document_processor(file_type)
    if file_processor is None:
        print(f"no file processor for {file_path}")
        return
    features = file_processor(file_path).run_pipeline()
    data = [asdict(feature) for feature in features]
    os.makedirs(output_folder_path, exist_ok=True)
    
    with open(os.path.join(output_folder_path, f"{file_name}.json"), "w") as json_from_pdf:
      data_pretty_json = json.dumps(data, indent=2)
      json_from_pdf.write(data_pretty_json)

def list_files_in_folder(folder_path: str):
    for entry in os.listdir(folder_path):
        full_path = os.path.join(folder_path, entry)
        if os.path.isfile(full_path):
            yield full_path

def get_file_name(file_path: str) -> str:
    return os.path.basename(file_path)

def process_document(file_path: str, output_folder_path):
    file_name =get_file_name(file_path)
    file_type = get_file_type(file_name)
    file_processor = get_document_processor(file_type)
    if file_processor is None:
        print(f"no file processor for {file_path}")
        return
    features = file_processor(file_path).run_pipeline()
    data = [asdict(feature) for feature in features]
    os.makedirs(output_folder_path, exist_ok=True)
    
    with open(os.path.join(output_folder_path, f"{file_name}.json"), "w") as json_from_pdf:
      data_pretty_json = json.dumps(data, indent=2)
      json_from_pdf.write(data_pretty_json)


def process_documents(input_folder_path, output_folder_path):
    for file_path in list_files_in_folder(input_folder_path):
        process_document(file_path, output_folder_path)
