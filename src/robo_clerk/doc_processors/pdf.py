import os
import re
import unicodedata
from PyPDF2 import PdfReader
import pdfplumber

class PDFProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.pdf_paths = self.load_pdf_paths()
        self.text = ""
        self.form_fields = {}
        self.signature_found = False


  # 1. Loading PDF file paths from a folder
    def load_pdf_paths(self):
        return [
            os.path.join(self.folder_path, f)
            for f in os.listdir(self.folder_path)
            if f.lower().endswith(".pdf")
        ]

  # 2. Extracting text and form fields from PDF files
    def extract_text_and_fields(self):
        all_text = ""
        all_fields = {}

        for pdf_path in self.pdf_paths:
            reader = PdfReader(pdf_path)

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

        #print("Extracted client info:", self.form_fields)
        return client_info

    # 5. checking for signature
    def detect_signature_as_image(self):

        pdf_path = self.pdf_paths[0]
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[0]
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
