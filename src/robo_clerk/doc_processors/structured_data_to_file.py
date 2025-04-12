import json
import os


def export_feature_file(features: list, source_file_name: str, client_id: str, save_dir: str):
    # make sure this matches schema
    output_data = dict(
        source=source_file_name,
        client_id=client_id,
        features= features
    )
    with open(os.path.join(save_dir, f"{source_file_name}.json"), "w") as destination_file:
        output_data_pretty_json = json.dumps(output_data, indent=2)
        destination_file.write(output_data_pretty_json)