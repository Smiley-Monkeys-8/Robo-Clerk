import json
import requests
import base64
import os
from dataclasses import dataclass

@dataclass
class GameSession:
    session_id: str
    player_id: str
    client_id: str

def detect_file_extension(decoded_bytes):
    if decoded_bytes.startswith(b'\x89PNG'):
        return '.png'
    elif decoded_bytes.startswith(b'PK') and b'word/' in decoded_bytes:
        return '.docx'
    elif decoded_bytes.startswith(b'%PDF'):
        return '.pdf'
    elif all(chr(b).isprintable() or chr(b).isspace() for b in decoded_bytes[:100]):
        return '.txt'
    else:
        return ''  # Unknown extension

def JB_start_game(api_url, api_key, player_name, save_dir="downloads"):
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "player_name": player_name
    }

    response = requests.post(f"{api_url}/start", json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"API call failed: {response.status_code} - {response.text}")

    data = response.json()
    with open("response.json", "w") as response_file:
      json.dump(data, response_file)

    # Save files from client_data.data if present
    client_data = data.get("client_data", {})
    if client_data:
        os.makedirs(save_dir, exist_ok=True)
        for base_filename, b64_content in client_data.items():
            try:
                decoded = base64.b64decode(b64_content)
                ext = detect_file_extension(decoded)
                filename = f"{base_filename}{ext}" if not base_filename.endswith(ext) else base_filename
                file_path = os.path.join(save_dir, filename)
                with open(file_path, "wb") as f:
                    f.write(decoded)
                print(f"Saved file: {file_path}")
            except Exception as e:
                print(f"Failed to save file {base_filename}: {e}")

    return GameSession(
        session_id=data.get("session_id", ""),
        player_id=data.get("player_id", ""),
        client_id=data.get("client_id", "")
    )

def JB_send_decision(api_url, api_key, game_session: GameSession, decision: str):
    headers = {
      "x-api-key": api_key,
      "Content-Type": "application/json"
    }
    payload = {
      "decision": decision,
      "session_id": game_session.session_id,
      "client_id": game_session.client_id
    }

    response = requests.post(f"{api_url}/decision", json=payload, headers=headers)
    data = response.json()
    print(data)
    return data.get("status", '') is not "gameover"