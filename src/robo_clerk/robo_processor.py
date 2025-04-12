import os
from robo_clerk.decider.judge import Decision
from robo_clerk.doc_processors.doc_master import process_documents
from robo_clerk.utils.file import get_file_name, list_files_in_folder, list_folders_in_folder


def get_result(client_id):
    if client_id % 1000 <= 500:
        return Decision.Accept
    return Decision.Reject

def get_client_id_from_folder(folder_name):
    id = folder_name.split("_")[-1]
    print(id)
    return int(id)

def process_test_data():
    for folder in list_folders_in_folder("./test_data"):
        client_id = get_client_id_from_folder(folder_name=folder)
        print(client_id, get_result(client_id=client_id).value)

        process_documents(folder, "out", output_file=f"client_data_{client_id}.json")
        
if __name__ == "__main__":
    process_test_data()