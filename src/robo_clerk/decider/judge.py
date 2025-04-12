from enum import Enum
import json

class Decision(Enum):
    Accept="Accept"
    Reject="Reject"


def manual_decision():
    decision = input("Choose your action (Accept/Reject): ").strip()
    return Decision(decision)

import re
from datetime import datetime
from difflib import SequenceMatcher

def verify_personal_data_consistency(data):
    inconsistencies = []
    invalid_data = []

    def similar(a, b):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    def is_valid_date(date_str, formats):
        for fmt in formats:
            try:
                datetime.strptime(date_str.strip(), fmt)
                return True
            except ValueError:
                continue
        return False

    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def is_valid_passport_number(passport):
        return re.match(r"^[A-Z]{2}[0-9]{7}$", passport.strip().upper())

    def is_valid_phone_number(phone):
        return re.match(r"^\+[\d\s\-()]{7,}$", phone.strip())

    matches = [
        ("passport_number_account.pdf", "passport_number_passport.png", "passport_no_profile.docx"),
        ("name_account.pdf", "account_name_account.pdf"),
        ("account_holder_name_account.pdf", "first_name_profile.docx"),
        ("account_holder_surname_account.pdf", "last_name_profile.docx"),
        ("email_account.pdf", "email_profile.docx"),
        ("phone_number_account.pdf", "telephone_profile.docx"),
        ("birth_date_passport.png", "date_of_birth_profile.docx"),
        ("issue_date_passport.png", "id_issue_date_profile.docx"),
        ("expiry_date_passport.png", "id_expiry_date_profile.docx"),
    ]

    # 1. Check consistency of matched fields
    total_checks = 0
    consistent = 0

    for group in matches:
        values = [data.get(k, "").strip().lower() for k in group if k in data]
        if len(values) > 1:
            base = values[0]
            for other in values[1:]:
                if similar(base, other) < 0.9:
                    inconsistencies.append((group, base, other))
                else:
                    consistent += 1
                total_checks += 1

    # 2. Validate known formats
    date_fields = {
        "birth_date_passport.png": ["%d-%b-%Y"],
        "date_of_birth_profile.docx": ["%Y-%m-%d"],
        "issue_date_passport.png": ["%d-%b-%Y"],
        "expiry_date_passport.png": ["%d-%b-%Y"],
        "id_issue_date_profile.docx": ["%Y-%m-%d"],
        "id_expiry_date_profile.docx": ["%Y-%m-%d"],
    }
    for field, formats in date_fields.items():
        if field in data and not is_valid_date(data[field], formats):
            invalid_data.append((field, data[field], "Invalid date format"))

    if "email_account.pdf" in data and not is_valid_email(data["email_account.pdf"]):
        invalid_data.append(("email_account.pdf", data["email_account.pdf"], "Invalid email"))

    if "email_profile.docx" in data and not is_valid_email(data["email_profile.docx"]):
        invalid_data.append(("email_profile.docx", data["email_profile.docx"], "Invalid email"))

    if "passport_number_account.pdf" in data and not is_valid_passport_number(data["passport_number_account.pdf"]):
        invalid_data.append(("passport_number_account.pdf", data["passport_number_account.pdf"], "Invalid passport number"))

    if "phone_number_account.pdf" in data and not is_valid_phone_number(data["phone_number_account.pdf"]):
        invalid_data.append(("phone_number_account.pdf", data["phone_number_account.pdf"], "Invalid phone number"))

    # 3. Calculate consistency percentage
    consistency_percentage = round((consistent / total_checks) * 100, 2) if total_checks > 0 else 100.0

    return {
        "consistency_percentage": consistency_percentage,
        "potential_inconsistencies": inconsistencies,
        "invalid_data": invalid_data
    }


def handcrafted_decision(file_path: str):
    with open(file_path) as json_file:
        customer_data = json.load(json_file)
    with open("result.json", "w") as result_file:
        result = verify_personal_data_consistency(customer_data)
        result_file.write(json.dumps(result, indent=2))