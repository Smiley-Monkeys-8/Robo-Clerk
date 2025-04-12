from enum import Enum
import json
import re
from datetime import datetime
from difflib import SequenceMatcher
import unicodedata
from nltk.corpus import wordnet as wn

class Decision(Enum):
    Accept="Accept"
    Reject="Reject"


def manual_decision():
    decision = input("Choose your action (Accept/Reject): ").strip()
    return Decision(decision)


def verify_personal_data_consistency(data):
    inconsistencies = []
    invalid_data = []

    def similar(a, b):
        if a in b or b in a:
            return 1.00
        
        # check for all synonyms
        max_ratio = 0
        
        return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()


    def normalize_name(name):
        name = name.strip().lower()
        name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode()
        return name

    def normalize_date(value):
        if not value:
            return None
        value = value.strip()
        value = re.sub(r'\s+', ' ', value)  # normalize whitespace
        formats = [
            "%d-%b-%Y", "%d-%B-%Y", "%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%d.%m.%Y",
            "%d %b %Y", "%d %B %Y", "%Y %b %d", "%Y %B %d"
        ]
        for fmt in formats:
            try:
                return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        # try to manually fix common lowercase month issues
        try:
            return datetime.strptime(value.title(), "%d-%b-%Y").strftime("%Y-%m-%d")
        except:
            return None

    def normalize(key, value):
        if "date" in key:
            return normalize_date(value)
        if "name" in key:
            return normalize_name(value)
        return value.lower().strip()

    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email.strip())

    def is_valid_passport_number(passport):
        return re.match(r"^[A-Z]{2}[0-9]{7}$", passport.strip().upper())

    def is_valid_phone_number(phone):
        return re.match(r"^\+[\d\s\-()]{7,}$", phone.strip())

    # Pairs or groups of keys we expect to be consistent
    matches = [
        ("passport_number_account.pdf", "passport_number_passport.png", "passport_no_profile.docx"),
        ("name_account.pdf", "account_name_account.pdf"),
        ("account_holder_name_account.pdf", "first_name_profile.docx"),
        ("account_holder_surname_account.pdf", "last_name_profile.docx"),
        ("email_account.pdf", "email_profile.docx"),
        # ("phone_number_account.pdf", "telephone_profile.docx"),
        ("birth_date_passport.png", "date_of_birth_profile.docx"),
        ("issue_date_passport.png", "id_issue_date_profile.docx"),
        ("expiry_date_passport.png", "id_expiry_date_profile.docx"),
        ("country_account.pdf", "country_of_domicile_profile.docx"),
        ("citizenship_passport.png", "nationality_profile.docx"),
    ]

    total_checks = 0
    consistent = 0

    for group in matches:
        values = [(k, data.get(k, "")) for k in group if k in data]
        if len(values) > 1:
            base_key, base_val = values[0]
            base_val_norm = normalize(base_key, base_val)
            for other_key, other_val in values[1:]:
                other_val_norm = normalize(other_key, other_val)
                if base_val_norm and other_val_norm and similar(base_val_norm, other_val_norm) >= 0.8:
                    consistent += 1
                else:
                    inconsistencies.append((group, base_val, other_val))
                total_checks += 1

    # Validate known formats
    date_fields = [
        "birth_date_passport.png",
        "date_of_birth_profile.docx",
        "issue_date_passport.png",
        "expiry_date_passport.png",
        "id_issue_date_profile.docx",
        "id_expiry_date_profile.docx",
    ]
    for field in date_fields:
        if field in data and not normalize_date(data[field]):
            invalid_data.append((field, data[field], "Invalid date format"))

    if "email_account.pdf" in data and not is_valid_email(data["email_account.pdf"]):
        invalid_data.append(("email_account.pdf", data["email_account.pdf"], "Invalid email"))

    if "email_profile.docx" in data and not is_valid_email(data["email_profile.docx"]):
        invalid_data.append(("email_profile.docx", data["email_profile.docx"], "Invalid email"))

    if "passport_number_account.pdf" in data and not is_valid_passport_number(data["passport_number_account.pdf"]):
        invalid_data.append(("passport_number_account.pdf", data["passport_number_account.pdf"], "Invalid passport number"))

    # if "phone_number_account.pdf" in data and not is_valid_phone_number(data["phone_number_account.pdf"]):
    #     invalid_data.append(("phone_number_account.pdf", data["phone_number_account.pdf"], "Invalid phone number"))

    consistency_percentage = round((consistent / total_checks) * 100, 2) if total_checks > 0 else 100.0

    return {
        "consistency_percentage": consistency_percentage,
        "potential_inconsistencies": inconsistencies,
        "invalid_data": invalid_data
    }

def handcrafted_decision(file_path: str):
    with open(file_path) as json_file:
        customer_data = json.load(json_file)
        result = verify_personal_data_consistency(customer_data)
        negative_result = result["consistency_percentage"] < 95 or len(result["invalid_data"]) > 0
        print(result["invalid_data"], len(result["invalid_data"]))
        decision = Decision.Reject if negative_result else Decision.Accept
        return decision, result
