import random
import time

def start_game():
    print("🎮 Welcome to the Decision Quest!")
    print("Make the right choices or the game ends.")
    print("-" * 40)

def make_decision():
    decision = input("Choose your action (accept/reject): ").strip().lower()
    return decision

def send_decision_to_server(decision):
    """Simulate server logic. Let's say only 'accept' is valid."""
    valid_decisions = ['accept']
    print(f"Sending decision '{decision}' to server...")
    time.sleep(1)
    return decision in valid_decisions

def play_game():
    start_game()
    while True:
        decision = make_decision()
        success = send_decision_to_server(decision)
        if success:
            print("✅ Good move! Keep going...\n")
        else:
            print("❌ Wrong decision. Game over!")
            break

if __name__ == "__main__":
    play_game()
