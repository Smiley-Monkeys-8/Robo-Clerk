import time
import os
from dotenv import load_dotenv
from robo_clerk.jb_api import JB_send_decision, JB_start_game

# Load the .env file from the project root
load_dotenv()

def make_decision():
    decision = input("Choose your action (Accept/Reject): ").strip()
    return decision

def play_game():
    api_key = os.getenv("API_KEY")
    api_url = os.getenv("API_URL")
    game_session = JB_start_game(api_key=api_key, api_url=api_url, player_name="Smiling Monkeys")
    while True:
        decision = make_decision()
        success = JB_send_decision(api_key, api_url, game_session, decision)
        if success:
            print("✅ Good move! Keep going...\n")
        else:
            print("❌ Wrong decision. Game over!")
            break

if __name__ == "__main__":
    play_game()
