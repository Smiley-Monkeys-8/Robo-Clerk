import json
import os
from dotenv import load_dotenv
from robo_clerk.decider.judge import Decision, manual_decision
from robo_clerk.doc_processors.pdf import PDFProcessor
from robo_clerk.jb_api import JB_send_decision, JB_start_game
import time

# Load the .env file from the project root
load_dotenv()

def make_decision(manual: bool = True) -> Decision:
    if manual:
        return manual_decision()

def process_pdf():
    input_folder_path = "downloads"
    output_folder_path = "data"
    processor = PDFProcessor(input_folder_path)
    data = processor.run_pipeline()
    print("\nAll steps completed. Data retrieved:")
    os.makedirs(output_folder_path, exist_ok=True)
    with open(os.path.join(output_folder_path, "account.pdf.json"), "w") as json_from_pdf:
      pdf_pretty_json = json.dumps(data, indent=2)
      json_from_pdf.write(pdf_pretty_json)
    print(data)

def process_documents():
    process_pdf()

def play_game():
    api_key = os.getenv("API_KEY")
    api_url = os.getenv("API_URL")
    game_session = JB_start_game(api_url=api_url, api_key=api_key, player_name="Smiling Monkeys")
    while True:
        process_documents()
        decision = make_decision()
        time.sleep(1)
        success = JB_send_decision(api_url, api_key, game_session, decision.value)
        if success:
            print("✅ Good move! Keep going...\n")
        else:
            print("❌ Wrong decision. Game over!")
            break

if __name__ == "__main__":
    play_game()
