#-------------------------------------------------------------------------------------------------

# # Fixed attempt 3 - improved
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re
import json

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

# Example usage
if __name__ == "__main__":
    image_path = "./downloads/passport.png"
    process_passport_image(image_path)

#-------------------------------------------------------------------------------------
# # Fixed attempt 2 - improved
# from PIL import Image, ImageEnhance, ImageFilter
# import pytesseract
# import json
# import re

# TESS_LANG = "eng+dan"

# # Common field labels to ignore
# FIELD_LABELS = {"PASNUMMER", "PASSPORT", "KONGERIGET", "DANMARK", "KINGDOM", "OF", "DENMARK", "DANSK"}

# def preprocess_image(image_path):
#     image = Image.open(image_path)
#     image = image.convert("L")
#     image = ImageEnhance.Contrast(image).enhance(2.0)
#     image = image.filter(ImageFilter.SHARPEN)
#     return image

# def is_probable_name(text):
#     return bool(re.match(r"^[A-ZÆØÅÄÖÜ][A-ZÆØÅÄÖÜ\- ]{2,}$", text)) and text.upper() not in FIELD_LABELS

# def extract_fields(text):
#     lines = [line.strip() for line in text.splitlines() if line.strip()]
#     full_text = "\n".join(lines)

#     extracted = {}

#     # Extract birth date
#     birth = re.search(r"\b(\d{2}-[A-Za-z]{3}-\d{4})\b", full_text)
#     if birth:
#         extracted["birth_date"] = birth.group(1)

#     # Get all date-like values
#     dates = re.findall(r"\b(\d{2}-[A-Za-z]{3}-\d{4})\b", full_text)
#     if len(dates) >= 2:
#         extracted["issue_date"] = dates[-2]
#         extracted["expiry_date"] = dates[-1]

#     # Passport number (alphanumeric block, ignore labels)
#     for line in lines:
#         if re.match(r"^[A-Z0-9]{7,10}$", line) and line.upper() not in FIELD_LABELS:
#             extracted["passport_number"] = line
#             break

#     # Citizenship
#     for line in lines:
#         if "DNK" in line or "Danish" in line:
#             extracted["citizenship"] = "DNK"
#             break

#     # Names
#     probable_names = [l for l in lines if is_probable_name(l)]
#     if probable_names:
#         extracted["surname"] = probable_names[0].title()
#         if len(probable_names) > 1:
#             extracted["given_names"] = " ".join(n.title() for n in probable_names[1:])

#     # Sex
#     for line in lines:
#         if re.match(r"\b[MF]\b", line.strip()):
#             extracted["sex"] = line.strip()
#             break

#     return extracted

# def process_passport(image_path, output_path="./data/passport_data.json"):
#     image = preprocess_image(image_path)
#     text = pytesseract.image_to_string(image, lang=TESS_LANG)

#     print("\nExtracted Text:\n" + text + "\n")

#     extracted_data = extract_fields(text)

#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(extracted_data, f, indent=4, ensure_ascii=False)

#     print("📋 Extracted Passport Data:")
#     print(json.dumps(extracted_data, indent=4, ensure_ascii=False))
#     return extracted_data

# # Run
# image_path = "./downloads/passport.png"
# process_passport(image_path)

#---------------------------------------------------------------
# Fixed attempt 1 - improved
# from PIL import Image, ImageEnhance, ImageFilter
# import pytesseract
# import json
# import re

# TESS_LANG = "eng+dan"

# def preprocess_image(image_path):
#     image = Image.open(image_path)
#     image = image.convert("L")
#     image = ImageEnhance.Contrast(image).enhance(2.0)
#     image = image.filter(ImageFilter.SHARPEN)
#     return image

# def clean(text):
#     return re.sub(r"[^a-zA-Z0-9\-\s]", "", text).strip()

# def extract_fields(text):
#     lines = [line.strip() for line in text.splitlines() if line.strip()]
#     extracted = {}

#     # Join lines for date-based regex
#     full_text = "\n".join(lines)

#     # Birth Date
#     birth_match = re.search(r"\b(\d{2}-[A-Za-z]{3}-\d{4})\b", full_text)
#     if birth_match:
#         extracted["birth_date"] = birth_match.group(1)

#     # Issue Date and Expiry Date
#     dates = re.findall(r"\b(\d{2}-[A-Za-z]{3}-\d{4})\b", full_text)
#     if len(dates) >= 2:
#         extracted["issue_date"] = dates[-2]
#         extracted["expiry_date"] = dates[-1]

#     # Passport Number – usually alphanumeric, often 8–10 chars
#     for line in lines:
#         if re.match(r"^[A-Z0-9]{7,10}$", line):
#             extracted["passport_number"] = line
#             break

#     # Citizenship – search for DNK or similar
#     for line in lines:
#         if "DNK" in line or "Danish" in line:
#             extracted["citizenship"] = line
#             break

#     # Surname and Given Names – try to infer from uppercase names
#     name_lines = [l for l in lines if re.match(r"^[A-Z][A-Z\s\-]+$", l)]
#     if name_lines:
#         extracted["surname"] = name_lines[0].title()
#         if len(name_lines) > 1:
#             extracted["given_names"] = name_lines[1].title()

#     # Sex – Look for 'M' or 'F'
#     for line in lines:
#         if re.match(r"\b[MF]\b", line):
#             extracted["sex"] = line
#             break

#     return extracted

# def process_passport(image_path, output_path="./data/passport_data.json"):
#     image = preprocess_image(image_path)
#     text = pytesseract.image_to_string(image, lang=TESS_LANG)

#     print("\nExtracted Text:\n" + text + "\n")
    
#     data = extract_fields(text)

#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=4, ensure_ascii=False)

#     print("📋 Extracted Passport Data:")
#     print(json.dumps(data, indent=4, ensure_ascii=False))
#     return data

# # Run the processor
# image_path = "./downloads/passport.png"
# process_passport(image_path)



#------------------------------------------------------------------------------------------------------
# from typing import List
# import pytesseract
# from PIL import Image, ImageEnhance, ImageFilter
# import regex as rex
# import json

# from robo_clerk.doc_processors.types import Feature

# # Language model for Tesseract (using English only for simplicity)
# TESS_LANG = "eng"

# # Preprocessing function to enhance the image for better OCR
# def preprocess_image(image_path):
#     image = Image.open(image_path)
#     image = image.convert("L")  # Convert to grayscale
#     enhancer = ImageEnhance.Contrast(image)
#     image = enhancer.enhance(2)  # Adjust contrast to improve text clarity
#     image = image.filter(ImageFilter.SHARPEN)  # Sharpen the image for better detail
#     return image

# # Simpler function to extract basic fields like passport number, surname, etc.
# def extract_fields(text):
#     # Simpler regex patterns
#     fields = {
#         "surname": r"([A-Z]+)",  # Assuming surname is all uppercase letters (simple)
#         "passport_number": r"([A-Z0-9]{8,})",  # Match passport numbers
#         "birth_date": r"(\d{2}-[A-Za-z]{3}-\d{4})",  # Birth date in DD-MMM-YYYY format
#         "sex": r"(M|F)",  # Gender - Male or Female
#         "citizenship": r"([A-Za-z\s]+)",  # Citizenship (could be a country name)
#         "issue_date": r"(\d{2}-[A-Za-z]{3}-\d{4})",  # Issue date in DD-MMM-YYYY format
#         "expiry_date": r"(\d{2}-[A-Za-z]{3}-\d{4})",  # Expiry date in DD-MMM-YYYY format
#     }

#     # Store extracted fields in a dictionary
#     extracted_data = {}

#     for key, pattern in fields.items():
#         match = rex.search(pattern, text)
#         if match:
#             extracted_data[key] = match.group(1).strip()

#     return extracted_data

# # Main function to process passport image and extract data
# def process_passport_image(image_path):
#     # Preprocess the image for better OCR results
#     image = preprocess_image(image_path)
    
#     # Perform OCR to extract text from the image
#     text = pytesseract.image_to_string(image, lang=TESS_LANG)

#     # Debugging: Print the raw OCR text
#     print("Extracted Text:")
#     print(text)

#     # Extract relevant fields (e.g., surname, passport number)
#     extracted_data = extract_fields(text)

#     # If no data was extracted, notify the user
#     if not extracted_data:
#         print("⚠️ No valid fields were extracted.")
    
#     return extracted_data

# class PNGProcessor:
#     def __init__(self, file_path):
#         self.file_path = file_path


#     def extract_client_info(self) -> List[Feature]:
#         data = process_passport_image(self.file_path)
#         features: List[Feature] = [Feature(key=key, value=value, coordinates={}) for key, value in data.items()]
#         return features
        
#     # Run all steps
#     def run_pipeline(self) -> List[Feature]:
#         return self.extract_client_info()


# # Example usage for debug
# if __name__ == "__main__":
#     image_path = "./downloads/passport.png"  # Update with the correct image path
#     data = process_passport_image(image_path)

#     # Show the result
#     print("\n📋 Extracted Passport Data:")
#     print(json.dumps(data, indent=4, ensure_ascii=False))
