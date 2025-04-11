import requests
import base64
import os

def start_game(api_url, api_key, player_name, save_dir="downloads"):
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "player_name": player_name
    }

    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"API call failed: {response.status_code} - {response.text}")

    data = response.json()

    # Save files from client_data.data if present
    client_data = data.get("client_data", {}).get("data", {})
    if client_data:
        os.makedirs(save_dir, exist_ok=True)
        for filename, b64_content in client_data.items():
            try:
                file_path = os.path.join(save_dir, filename)
                with open(file_path, "wb") as f:
                    f.write(base64.b64decode(b64_content))
                print(f"Saved file: {file_path}")
            except Exception as e:
                print(f"Failed to save file {filename}: {e}")

    return data
