from enum import Enum

class Decision(Enum):
    Accept="Accept"
    Reject="Reject"


def manual_decision():
    decision = input("Choose your action (Accept/Reject): ").strip()
    return Decision(decision)