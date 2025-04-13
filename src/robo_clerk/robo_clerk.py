import os
from dotenv import load_dotenv
from robo_clerk.decider.judge import Decision, handcrafted_decision, manual_decision
from robo_clerk.doc_processors.doc_master import process_documents
from robo_clerk.jb_api import JB_send_decision, JB_start_game
import time

# Load the .env file from the project root
load_dotenv()

def make_decision(manual: bool = True) -> Decision:
    if manual:
        return manual_decision()

def get_in_out_folders(suffix=""):
    return  f"downloads{suffix}", f"data{suffix}"

def play_game():
    api_key = os.getenv("API_KEY")
    api_url = os.getenv("API_URL")
    input_folder_path, output_folder_path = get_in_out_folders()
    game_session = JB_start_game(api_url=api_url, api_key=api_key, player_name="Smiling Monkeys", save_dir=input_folder_path)
    while True:
        process_documents(input_folder_path, output_folder_path)
        input_folder_path, output_folder_path = get_in_out_folders()
        decision, _ = handcrafted_decision("data/client_data.json")
        # decision = manual_decision()
        # time.sleep(1)
        print(f"DECISION: {decision.value}")
        print(game_session)
        success, client_id = JB_send_decision(api_url, api_key, game_session, decision=decision.value, save_dir=input_folder_path)
        game_session.client_id = client_id
        if success:
            print("✅ Good move! Keep going...\n")
        else:
            print("❌ Wrong decision. Game over!")
            break

if __name__ == "__main__":
    play_game()
