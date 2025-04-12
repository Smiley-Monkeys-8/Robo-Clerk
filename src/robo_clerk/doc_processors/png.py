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
    # image = image.crop((left, upper, right, lower))

    # Convert to grayscale
    image = image.convert("L")

    # Enhance contrast
    image = ImageEnhance.Contrast(image).enhance(2)

    # Apply sharpen filter
    new_size = (1200, 900)  # e.g., (300, 200)

    # Resize image
    image = image.resize(new_size)  # ANTIALIAS gives better quality
    # image = image.filter(ImageFilter.GaussianBlur)
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

def crop_and_get_text(image, box):
    cropped_image = image.crop(box)
    cropped_image.save("cropped.png")
    text = pytesseract.image_to_string(cropped_image)
    return text.strip()


# Main processing function
def process_passport_image(image_path, output_path="./data/passport_data.json"):
    image = preprocess_image(image_path)
    image.save("test.png")
    
    # box_mapping = {
    #     "country":(50, 0, image.width, 120),
    #     "surname":
    #     "given_name"
    #     "birth_date"
    #     "citizenship"
    #     "sex"
    #     "issue_date"
    #     "expiry_date"
    #     "passport_number"
    # }
    
    # get country
    country_crop = (50, 0, image.width, 120)
    country = crop_and_get_text(image, country_crop)
    print(country)
    # get surname
    surname_crop = (50, 300, 300, 380)
    surname = crop_and_get_text(image, surname_crop)
    print(surname)
    # get given name
    given_name_crop = (300, 300, 900, 380)
    given_name = crop_and_get_text(image, given_name_crop)
    print(given_name)   
    # birth date
    birth_date_crop = (50, 420, 300, 480)
    birth_date = crop_and_get_text(image, birth_date_crop)
    print(birth_date)
    # citizenship
    citizenship_crop = (300, 420, 900, 480)
    citizenship = crop_and_get_text(image, citizenship_crop)
    print(citizenship)
    # get sex
    sex_crop = (50, 540, 300, 600)
    sex = crop_and_get_text(image, sex_crop)
    print(sex)
    # get issue data
    issue_date_crop = (300, 540, 900, 600)
    issue_date = crop_and_get_text(image, issue_date_crop)
    print(issue_date)
    # get expiry date
    expiry_date_crop = (300, 630, 800, 700)
    expiry_date = crop_and_get_text(image, expiry_date_crop)
    print(expiry_date)
    # passport number
    passport_number_crop = (700, 160, 1100, 200)
    passport_number = crop_and_get_text(image, passport_number_crop)
    print(passport_number)
    
    
    return {
        
    }

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
