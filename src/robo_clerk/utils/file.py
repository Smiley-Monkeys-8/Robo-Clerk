from enum import Enum
import os

class FileType(Enum):
    DOCX = 'docx'
    PDF = 'pdf'
    TXT = 'txt'
    PNG = 'png'
    JSON = 'json'

def get_file_type(filename: str) -> FileType | None:
    ext = filename.lower().split('.')[-1]
    for filetype in FileType:
        if filetype.value == ext:
            return filetype
    return None


def list_folders_in_folder(folder_path: str):
    for entry in os.listdir(folder_path):
        full_path = os.path.join(folder_path, entry)
        if not os.path.isfile(full_path):
            yield full_path

def list_files_in_folder(folder_path: str):
    for entry in os.listdir(folder_path):
        full_path = os.path.join(folder_path, entry)
        if os.path.isfile(full_path):
            yield full_path

def get_file_name(file_path: str) -> str:
    return os.path.basename(file_path)