import pytesseract
from PIL import Image
import re as rex
import json
from datetime import datetime

TESS_LANG = "eng+deu+fra+spa+ita+pol+rus"

# Date formatting helper
def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%d-%b-%Y").strftime("%d-%b-%Y")
    except:
        return date_str

# MRZ date formatting (YYMMDD → DD-MMM-YYYY)
def format_date_mrz(d):
    try:
        year = int(d[0:2])
        year += 2000 if year < 50 else 1900
        date_obj = datetime.strptime(f"{year}{d[2:]}", "%Y%m%d")
        return date_obj.strftime("%d-%b-%Y")
    except:
        return None

# Try to extract data from MRZ
def extract_mrz(text):
    mrz_lines = [line.strip() for line in text.splitlines() if "<<" in line and len(line) > 40]
    if len(mrz_lines) >= 2:
        line1, line2 = mrz_lines[-2], mrz_lines[-1]
        return parse_mrz(line1, line2)
    return {}

def parse_mrz(line1, line2):
    result = {}
    try:
        parts = line1.split("<<")
        surname_part = parts[0][5:]
        given_part = parts[1].replace("<", " ").strip()
        result["surname"] = surname_part.replace("<", "")
        result["given_names"] = given_part

        result["passport_number"] = line2[0:9].strip("<")
        result["citizenship"] = line2[10:13]
        result["birth_date"] = format_date_mrz(line2[13:19])
        result["sex"] = line2[20]
        result["expiry_date"] = format_date_mrz(line2[21:27])
    except Exception as e:
        print("⚠️ MRZ parsing failed:", e)
    return result

# Extract additional fields from OCR
def extract_labeled_fields(text):
    fields = {
        "citizenship": r"Citizenship\s*[:\-]?\s*([^\n]+)",
        "issue_date": r"Issue Date\s*[:\-]?\s*(\d{2}-[A-Za-z]{3}-\d{4})",
        "expiry_date": r"Expiry Date\s*[:\-]?\s*(\d{2}-[A-Za-z]{3}-\d{4})",
        "signature": r"Signature\s*[:\-]?\s*([A-Za-zÀ-ÿ\s\-]+)"
    }
    data = {}
    for key, pattern in fields.items():
        match = rex.search(pattern, text, rex.IGNORECASE | rex.UNICODE)
        if match:
            data[key] = match.group(1).strip()
    return data

# Main parser
def process_passport_image(image_path, output_path="./data/passport_data.json"):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang=TESS_LANG)

    # Initialize with default values
    extracted = {
        "surname": None,
        "given_names": None,
        "passport_number": None,
        "birth_date": None,
        "sex": None,
        "citizenship": None,
        "issue_date": None,
        "expiry_date": None,
        "signature": None
    }

    # Fill from MRZ
    extracted.update(extract_mrz(text))

    # Fill from labels if available
    extracted.update({k: v for k, v in extract_labeled_fields(text).items() if v})

    # Format final JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(extracted, f, indent=4, ensure_ascii=False)

    print(f"✅ Passport data extracted and saved to {output_path}")
    return extracted

# Use it on your uploaded image
image_path = "./downloads/passport.png"
data = process_passport_image(image_path)

# Show result
print(json.dumps(data, indent=4, ensure_ascii=False))
