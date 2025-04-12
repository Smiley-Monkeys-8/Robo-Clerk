#-------------------------------------------------------------------------------------------------

# # Fixed attempt 3 - improved
from typing import List
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

from robo_clerk.doc_processors.types import Feature

# Supported OCR languages — include English
TESS_LANG = "eng"


# Crop the image to remove the MRZ area
def preprocess_image(image_path):
    image = Image.open(image_path)
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


def crop_and_get_text(image, box):
    cropped_image = image.crop(box)
    # cropped_image.save("cropped.png")
    text = pytesseract.image_to_string(cropped_image)
    return text.strip()


# Main processing function
def process_passport_image(image_path, output_path="./data/passport_data.json"):
    image = preprocess_image(image_path)
    # image.save("test.png")
    
    box_mapping = {
        "country":(50, 0, image.width, 120),
        "surname":(50, 300, 300, 380),
        "given_name":(300, 300, 900, 380),
        "birth_date":(50, 420, 300, 480),
        "citizenship":(300, 420, 900, 480),
        "sex":(50, 540, 300, 600),
        "issue_date":(300, 540, 900, 600),
        "expiry_date":(300, 630, 800, 700),
        "passport_number":(700, 160, 1100, 200)
    }
    
    data = { key: crop_and_get_text(image, box) for key, box in box_mapping.items()}
    print(data)
    return data

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
