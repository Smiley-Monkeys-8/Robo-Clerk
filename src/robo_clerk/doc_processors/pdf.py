import re
import unicodedata
from PyPDF2 import PdfReader
import pdfplumber

class PDFProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = ""
        self.form_fields = {}
        self.signature_found = False

    # 2. Extracting text and form fields from PDF files
    def extract_text_and_fields(self):
        all_text = ""
        all_fields = {}

        reader = PdfReader(self.file_path)

        # Extract text
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                all_text += page_text + "\n"

        # Extract form fields
        fields = reader.get_fields()
        if fields:
            for key, field in fields.items():
                value = field.get("/V")
                all_fields[key] = str(value) if value is not None else None

        self.text = all_text
        self.form_fields = all_fields

    # 3. Cleaning the text
    def clean_text(self):
        text = unicodedata.normalize("NFKD", self.text)
        text = re.sub(r"[^a-zA-Z0-9.,!?%€$-]", " ", text)
        text = text.lower()
        text = re.sub(r"\s+", " ", text).strip()
        text = re.sub(r"\.{5,}", " ", text)
        self.text = text

    # 4. Extracting and storing client info from cleaned text
    def extract_client_info(self):
        client_info = dict(self.form_fields)  # Making a copy of the form fields
        client_info["signature_image_found"] = self.signature_found

        return client_info

    # 5. checking for signature
    def detect_signature_as_image(self):
        with pdfplumber.open(self.file_path) as pdf:
            page = pdf.pages[0] # We look only at the first page
            images = page.images
            self.signature_found = bool(images)

            if images:
                print(f"Signature found.")
                return True
            else:
                print(f"No signature found.")
                return False

    def run_pipeline(self):
        self.extract_text_and_fields()
        self.clean_text()
        self.detect_signature_as_image()

        return {
            "client_info": self.extract_client_info()
        }
