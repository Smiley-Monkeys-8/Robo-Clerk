import os
import re
from docx import Document
import unicodedata

class DOCXProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = ""
        self.cleaned_text = ""
        self.extracted_info = {}
        self.tickable_info = {}

    # 1. Extracting raw text
    def extract_text(self):
        try:
            doc = Document(self.file_path)
        except Exception as e:
            print(f"Error reading DOCX file: {e}")
            return

        all_text = []

        for i, table in enumerate(doc.tables):
            for row in table.rows:
                for cell in row.cells:
                    cell_text = cell.text.strip()
                    if cell_text:
                        all_text.append(cell_text)

        self.text = "\n".join(all_text)

    # 2. Cleaning text (adjusting to keep important characters like punctuation and removing unnecessary spaces)
    def clean_text(self):
        text = unicodedata.normalize("NFKD", self.text)
        text = re.sub(r"[^a-zA-Z0-9.,!?%€$-:\n\s]", " ", text)  # Keep punctuation for dates, phone numbers, etc.
        text = text.lower()
        text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
        self.cleaned_text = text
        #print("Cleaned text:\n", self.cleaned_text, "\n")

    # 3. Extracting key-value and tickable options
    def extract_info(self):
        # Horrible Regex patterns (thanks chatGPT)
        tickable_patterns = {
            "gender": r"gender.*?\b(female|male)\b",
            "pep": r"politically exposed person.*?\b(no|yes)\b",
            "marital_status": r"marital status.*?\b(divorced|married|single|widowed)\b",
            "employment_status": r"(?:current employment and function|employment status).*?\b(employee|self-employed|currently not employed)\b",
            "previous_profession": r"previous profession.*?\b(retired|homemaker/housewife|student|diplomat|military representative|other|unknown)\b",
            "total_wealth": r"total wealth estimated.*?\b(< eur 1\.5m|eur 1\.5m-5m|eur 5m-10m|eur 10m.-20m|eur 20m.-50m|> eur 50m)\b",
            "origin_of_wealth": r"origin of wealth.*?\b(employment|inheritance|business|investments|sale of real estate|retirement package|other)\b",
            "estimated_assets": r"estimated assets.*?\b(real estate|business|investments|deposits|equity|fixed income|structured products|alternative investments|investment funds|insurance|other investments)\b",
            "estimated_income": r"estimated total income.*?\b(< eur 250,000|eur 250,000 - 500,000|eur 500,000 – 1m|> eur 1m)\b",
            "commercial_account": r"commercial account.*?\b(yes|no)\b",
            "investment_risk_profile": r"investment risk profile.*?\b(low|moderate|considerable|high)\b",
            "mandate_type": r"type of mandate.*?\b(advisory|discretionary)\b",
            "investment_experience": r"investment experience.*?\b(inexperienced|experienced|expert)\b",
            "investment_horizon": r"investment horizon.*?\b(short|medium|long-term)\b",
        }

        personal_info_patterns = {
            "last_name": r"last name\s*([\w\-]+)(?=\s*(first/ middle name \(s\)|address|country of domicile|date of birth|nationality|passport no|id type|id issue date|id expiry date))",
            "first_middle_name": r"first/ middle name \(s\)\s*([\w\s]+)(?=\s*(address|country of domicile|date of birth|nationality|passport no|id type|id issue date|id expiry date))",
            "address": r"address\s*([\w\s,.-]+?)(?=\s*(country of domicile|date of birth|nationality|passport no|id type|id issue date|id expiry date))",
            "country_of_domicile": r"country of domicile\s*([\w\s]+)(?=\s*(date of birth|nationality|passport no|id type|id issue date|id expiry date))",
            "date_of_birth": r"date of birth\s*(\d{4}-\d{2}-\d{2})(?=\s*(nationality|passport no|id type|id issue date|id expiry date))",
            "nationality": r"nationality\s*([\w\s]+)(?=\s*(passport no|id type|id issue date|id expiry date))",
            "passport_no": r"passport no/ unique id\s*([\w\d]+)(?=\s*(id type|id issue date|id expiry date))",
            "id_type": r"id type\s*([\w\s]+)(?=\s*(id issue date|id expiry date))",
            "id_issue_date": r"id issue date\s*(\d{4}-\d{2}-\d{2})(?=\s*id expiry date)",
            "id_expiry_date": r"id expiry date\s*(\d{4}-\d{2}-\d{2})",
        }

        # Extracting tickable fields
        tickable_results = {}
        for key, pattern in tickable_patterns.items():
            match = re.search(pattern, self.cleaned_text)
            if match:
                tickable_results[key] = match.group(1)
                print(f"  Tickable field '{key}': {match.group(1)}")

        # Extracting personal information fields
        personal_info = {}
        for key, pattern in personal_info_patterns.items():
            match = re.search(pattern, self.cleaned_text)
            if match:
                if key == "first_middle_name":
                    full_name = match.group(1).strip()
                    names = full_name.split()
                    personal_info["first_name"] = names[0]
                    personal_info["middle_name"] = " ".join(names[1:]) if len(names) > 1 else ""
                else:
                    personal_info[key] = match.group(1)
                print(f"  Personal info '{key}': {personal_info.get(key, '')}")

        # Combine personal info with other extracted information
        self.extracted_info = {**personal_info, **tickable_results}

        self.tickable_info = tickable_results

    # Run all steps
    def run_pipeline(self):
        self.extract_text()
        self.clean_text()
        self.extract_info()
        return {
            "text": self.text,
            "cleaned_text": self.cleaned_text,
            "info": self.extracted_info,
            "tickables": self.tickable_info
        }
