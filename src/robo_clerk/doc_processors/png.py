#-------------------------------------------------------------------------------------------------

# # Fixed attempt 3 - improved
from typing import List
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re
import json

from robo_clerk.doc_processors.types import Feature

# Supported OCR languages — include English
TESS_LANG = "eng"

# Labels to ignore when parsing names or numbers
FIELD_LABELS = [
    "PASSPORT", "PASNUMMER", "PAS NO", "PAS"
    # , "DANMARK",     "KONGERIGET", "DANISH", "DANSK", "<<", "<"
]

# Crop the image to remove the MRZ area
def preprocess_image(image_path):
    image = Image.open(image_path)
    
    # Define the coordinates for cropping (adjust based on your image)
    left = 0
    upper = 35
    right = image.width
    lower = image.height - 60 # crop the last 100 pixels (MRZ area)

    # Crop the image
    image = image.crop((left, upper, right, lower))

    # Convert to grayscale
    image = image.convert("L")

    # Enhance contrast
    image = ImageEnhance.Contrast(image).enhance(2)

    # Apply sharpen filter
    image = image.filter(ImageFilter.SHARPEN)
    
    return image


# Helper to detect probable name lines
def is_probable_name(line):
    return (
        bool(re.fullmatch(r"[A-Za-zÆØÅæøåÄÖÜäöü\- ]+", line.strip())) and
        not any(label in line.upper() for label in FIELD_LABELS)
    )

# Extract fields using OCR text analysis
def extract_passport_data(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    extracted = {}

    # Extract birth date
    for line in lines:
        match = re.search(r"(\d{2}-[A-Za-z]{3}-\d{4})", line)
        if match:
            extracted["birth_date"] = match.group(1)
            break

    # Extract issue/expiry dates
    date_matches = re.findall(r"(\d{2}-[A-Za-z]{3}-\d{4})", text)
    if len(date_matches) >= 3:
        extracted["issue_date"] = date_matches[1]
        extracted["expiry_date"] = date_matches[2]

    # Extract citizenship (e.g., DNK)
    for line in lines:
        if re.fullmatch(r"[A-Z]{3}", line):
            extracted["citizenship"] = line
            break

    # Extract passport number (7–10 uppercase alphanumeric, not a name)
    for line in lines:
        line_clean = line.strip().replace(" ", "")
        if re.fullmatch(r"[A-Z0-9]{7,10}", line_clean) and line_clean.upper() not in FIELD_LABELS and not is_probable_name(line_clean):
            extracted["passport_number"] = line_clean
            break

    # Extract names
    probable_names = [l for l in lines if is_probable_name(l)]
    if probable_names:
        extracted["surname"] = probable_names[0].title()
        given_candidates = probable_names[1:]
        extracted["given_names"] = " ".join(n.title() for n in given_candidates if n.upper() not in FIELD_LABELS and not n.isdigit())

    return extracted

# Main processing function
def process_passport_image(image_path, output_path="./data/passport_data.json"):
    image = preprocess_image(image_path)
    text = pytesseract.image_to_string(image, lang=TESS_LANG)

    print("\nExtracted Text:")
    print(text)

    extracted_data = extract_passport_data(text)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4, ensure_ascii=False)

    print("\n✅ Extracted data saved to", output_path)
    print("\n📋 Extracted Passport Data:")
    print(json.dumps(extracted_data, indent=4, ensure_ascii=False))
    return extracted_data

class PNGProcessor:
    def __init__(self, file_path):
        self.file_path = file_path


    def extract_client_info(self) -> List[Feature]:
        data = process_passport_image(self.file_path)
        features: List[Feature] = [Feature(key=key, value=value, source=self.file_path) for key, value in data.items()]
        return features
        
    # Run all steps
    def run_pipeline(self) -> List[Feature]:
        return self.extract_client_info()


# Example usage for debug
if __name__ == "__main__":
    image_path = "./downloads/passport.png"
    process_passport_image(image_path)
