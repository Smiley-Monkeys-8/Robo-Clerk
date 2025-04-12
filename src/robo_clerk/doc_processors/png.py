import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import regex as rex
import json

# Language model for Tesseract (using English only for simplicity)
TESS_LANG = "eng"

# Preprocessing function to enhance the image for better OCR
def preprocess_image(image_path):
    image = Image.open(image_path)
    image = image.convert("L")  # Convert to grayscale
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Adjust contrast to improve text clarity
    image = image.filter(ImageFilter.SHARPEN)  # Sharpen the image for better detail
    return image

# Simpler function to extract basic fields like passport number, surname, etc.
def extract_fields(text):
    # Simpler regex patterns
    fields = {
        "surname": r"([A-Z]+)",  # Assuming surname is all uppercase letters (simple)
        "passport_number": r"([A-Z0-9]{8,})",  # Match passport numbers
        "birth_date": r"(\d{2}-[A-Za-z]{3}-\d{4})",  # Birth date in DD-MMM-YYYY format
        "sex": r"(M|F)",  # Gender - Male or Female
        "citizenship": r"([A-Za-z\s]+)",  # Citizenship (could be a country name)
        "issue_date": r"(\d{2}-[A-Za-z]{3}-\d{4})",  # Issue date in DD-MMM-YYYY format
        "expiry_date": r"(\d{2}-[A-Za-z]{3}-\d{4})",  # Expiry date in DD-MMM-YYYY format
    }

    # Store extracted fields in a dictionary
    extracted_data = {}

    for key, pattern in fields.items():
        match = rex.search(pattern, text)
        if match:
            extracted_data[key] = match.group(1).strip()

    return extracted_data

# Main function to process passport image and extract data
def process_passport_image(image_path, output_path="./data/passport_data.json"):
    # Preprocess the image for better OCR results
    image = preprocess_image(image_path)
    
    # Perform OCR to extract text from the image
    text = pytesseract.image_to_string(image, lang=TESS_LANG)

    # Debugging: Print the raw OCR text
    print("Extracted Text:")
    print(text)

    # Extract relevant fields (e.g., surname, passport number)
    extracted_data = extract_fields(text)

    # If no data was extracted, notify the user
    if not extracted_data:
        print("⚠️ No valid fields were extracted.")
    
    # Save extracted data to JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4, ensure_ascii=False)

    print(f"✅ Extracted data saved to {output_path}")
    return extracted_data

# Example usage
image_path = "./downloads/passport.png"  # Update with the correct image path
data = process_passport_image(image_path)

# Show the result
print("\n📋 Extracted Passport Data:")
print(json.dumps(data, indent=4, ensure_ascii=False))