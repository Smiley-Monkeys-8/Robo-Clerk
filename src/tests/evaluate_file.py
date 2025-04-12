import os
from robo_clerk.decider import judge
from robo_clerk.robo_processor import get_result
from robo_clerk.utils.file import list_files_in_folder
import json


def get_client_id_from_file(file_name):
    id = file_name.split("_")[-1].split(".")[0]
    print(id)
    return int(id)

def write_results(result, destination_path):
    with open(destination_path, "w") as result_file:
        result_file.write(json.dumps(result, indent=2))

correct = 0
false_positive = 0
false_negative = 0
false_negative_folder = "out_false_negative"
false_positive_folder = "out_false_positive"
os.makedirs(false_negative_folder, exist_ok=True)
os.makedirs(false_positive_folder, exist_ok=True)

for file_name in list_files_in_folder("out"):
    print(file_name)
    client_id = get_client_id_from_file(file_name)
    decision, result = judge.handcrafted_decision(file_name)
    
    negative_result = decision == judge.Decision.Reject
    
    known_result = get_result(client_id)
    if known_result == judge.Decision.Reject and negative_result:
        print(f"{client_id}: True negative")
        correct += 1 
    if known_result == judge.Decision.Reject and not negative_result:
        print(f"{client_id}: False positive")
        false_positive += 1
        write_results(result=result, destination_path=os.path.join(false_positive_folder, f"result_{client_id}.json"))
    if known_result == judge.Decision.Accept and not negative_result:
        print(f"{client_id}: True positive")
        correct += 1 
    if known_result == judge.Decision.Accept and negative_result:
        print(f"{client_id}: False negative")
        false_negative += 1
        write_results(result=result, destination_path=os.path.join(false_negative_folder, f"result_{client_id}.json"))
        
print(f"Correct: {correct}")
print(f"False positive: {false_positive}")
print(f"False negative: {false_negative}")

print(f"percentage: {(correct*100)/(correct+false_negative+false_positive)}%")