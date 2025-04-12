import re
import json
from typing import List

from robo_clerk.doc_processors.types import Feature


def extract_client_info_from_text(text):
    result = {
        "client_info": {
            "account_name": "",
            "account_holder_name": "",
            "account_holder_surname": "",
            "chf": "/Off",
            "eur": "/Off",
            "usd": "/Off",
            "other_ccy": "",
            "city": "",
            "country": "",
            "name": "",
            "signature_image_found": False,

            # Personal information
            "age": "",
            "occupation": "",
            "marital_status": "",
            "children": [],

            # Financial information
            "last_salary": {
                "amount": "",
                "currency": ""
            },
            "savings": {
                "amount": "",
                "currency": ""
            },
            "real_estate": [],
            "inheritance_details": {
                "amount": "",
                "currency": "",
                "year": "",
                "relation": "",
                "relative_occupation": ""
            },

            # Education information
            "education": {
                "secondary_school": "",
                "secondary_graduation_year": "",
                "university": [],
                "university_graduation_years": []
            },

            # Career information
            "career_history": []
        }
    }

    # EXTRACT NAME
    # Try multiple patterns for full name extraction
    name_patterns = [
        r"([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) is (\d+) years old",
        r"([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) and the RM",
        r"([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) and (\w+) have been",
        r"The RM (?:is|was|has) .* ([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+)'s",
        r"introduced to ([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) at",
        r"([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) brings a wealth of",
        r"([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) is currently",
        r"([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) has been",
        r"([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) crossed paths",
        r"([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) launched his career"
    ]

    full_name = None
    for pattern in name_patterns:
        match = re.search(pattern, text)
        if match:
            full_name = match.group(1).strip()
            break

    # If still not found, try to find repeated names in the text
    if not full_name:
        # Look for common 3-part name pattern
        potential_names = re.findall(r'([A-Z][a-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż]+ [A-Z][a-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż]+ [A-Z][a-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż]+)', text)
        if potential_names:
            # Find the most frequently occurring name
            name_counts = {}
            for name in potential_names:
                name_counts[name] = name_counts.get(name, 0) + 1
            full_name = max(name_counts, key=name_counts.get)
        else:
            # Try 2-part names
            potential_names = re.findall(r'([A-Z][a-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż]+ [A-Z][a-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż]+)(?!\w)', text)
            if potential_names:
                name_counts = {}
                for name in potential_names:
                    name_counts[name] = name_counts.get(name, 0) + 1
                full_name = max(name_counts, key=name_counts.get)

    if full_name:
        result["client_info"]["account_name"] = full_name
        result["client_info"]["name"] = full_name

        # Split name into first and last names
        name_parts = full_name.split()
        if len(name_parts) >= 2:
            # For multi-part names
            if len(name_parts) >= 3:
                result["client_info"]["account_holder_name"] = " ".join(name_parts[:-1])
                result["client_info"]["account_holder_surname"] = name_parts[-1]
            else:
                result["client_info"]["account_holder_name"] = name_parts[0]
                result["client_info"]["account_holder_surname"] = name_parts[-1]

    # EXTRACT AGE
    age_patterns = [
        r"is (\d+) years old",
        r"is a (\d+) year old",
        r"is a (\d+)-year-old",
        r"is a (\d+) year old \w+",
        r"(\d+) year old \w+ from"
    ]

    for pattern in age_patterns:
        match = re.search(pattern, text)
        if match:
            result["client_info"]["age"] = match.group(1)
            break

    # EXTRACT COUNTRY
    country_patterns = [
        r"from ([A-Za-z\s]+)\.(?!\w)",
        r"comes from ([A-Za-z\s]+)\.(?!\w)",
        r"comes from ([A-Za-z\s]+)(?=\s)",
        r"from ([A-Za-z\s]+)(?=\s|\.|$)",
        r"(\d+) year old .+ from ([A-Za-z\s]+)"
    ]

    for pattern in country_patterns:
        match = re.search(pattern, text)
        if match:
            if "year old" in pattern and len(match.groups()) > 1:
                country = match.group(2).strip()
            else:
                country = match.group(1).strip()

            # Standardize country names
            country_standardization = {
                "Czech": "Czech Republic",
                "USA": "United States",
                "UK": "United Kingdom",
                "UAE": "United Arab Emirates"
            }
            result["client_info"]["country"] = country_standardization.get(country, country)
            break

    # EXTRACT CITY
    # Try to find cities from property locations first
    property_city_matches = re.findall(r"(?:apartment|property|townhouse|flat|house|condo|villa) (?:located |situated |)in ([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+?)(?:,|\.|\s|$)", text)
    property_cities = [city.strip() for city in property_city_matches]

    # Also look for cities mentioned in location lists
    location_matches = re.findall(r"locations across ([^\.]+)", text)
    for match in location_matches:
        # Split by 'and' or commas
        locations = re.split(r' and |, ', match)
        property_cities.extend([loc.strip() for loc in locations])

    # If we found property cities, use the first one as the client's city
    if property_cities:
        result["client_info"]["city"] = property_cities[0]
    else:
        # Otherwise try direct city mentions
        city_patterns = [
            r"retreat in ([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+)[,\.]",
            r"conference in ([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+)[,\.]",
            r"in ([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+)\. They",
            r"lives in ([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+)",
            r"residing in ([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+)"
        ]

        for pattern in city_patterns:
            match = re.search(pattern, text)
            if match:
                result["client_info"]["city"] = match.group(1).strip()
                break

    # EXTRACT MARITAL STATUS
    if re.search(r"currently divorced", text, re.IGNORECASE):
        result["client_info"]["marital_status"] = "Divorced"
    elif re.search(r"currently widowed", text, re.IGNORECASE):
        result["client_info"]["marital_status"] = "Widowed"
    elif re.search(r"(married|tied the knot|have been married)", text, re.IGNORECASE):
        result["client_info"]["marital_status"] = "Married"
    elif re.search(r"currently single", text, re.IGNORECASE):
        result["client_info"]["marital_status"] = "Single"

    # EXTRACT CHILDREN
    children_pattern1 = re.search(r"(?:has|have) (\d+) (?:kids|children)", text)
    if children_pattern1:
        # Try to find child names
        child_names_match = re.search(r"called ([^\.]+)", text)
        if child_names_match:
            names_text = child_names_match.group(1)
            # Split names by 'and' or commas
            names = re.split(r' and |, ', names_text)
            result["client_info"]["children"] = [name.strip() for name in names]
        else:
            # Just record the number
            result["client_info"]["children"] = [f"Child {i+1}" for i in range(int(children_pattern1.group(1)))]
    elif "parents of" in text.lower():
        children_match = re.search(r"parents of (\d+) children: ([^\.]+)", text)
        if children_match:
            names_text = children_match.group(2)
            # Split names by 'and' or commas
            names = re.split(r' and |, ', names_text)
            result["client_info"]["children"] = [name.strip() for name in names]
    elif "does not have any children" in text.lower():
        result["client_info"]["children"] = []

    # EXTRACT EDUCATION
    # Secondary education
    secondary_edu_patterns = [
        r"(?:received|earned|completed) (?:his|her) secondary (?:school|education) (?:diploma |)from ([^\.]+) in (\d{4})",
        r"graduated from ([^\.]+) in (\d{4})",
        r"finished secondary school at ([^\.]+) in (\d{4})"
    ]

    for pattern in secondary_edu_patterns:
        match = re.search(pattern, text)
        if match:
            result["client_info"]["education"]["secondary_school"] = match.group(1).strip()
            result["client_info"]["education"]["secondary_graduation_year"] = match.group(2)
            break

    # University education - multiple universities possible
    university_patterns = [
        r"earned (?:his|her) (?:degree|additionally degree) from ([^\.]+) in (\d{4})",
        r"graduated from ([^\.]+) (?:with|in) .* in (\d{4})",
        r"study at ([^\.]+) until (\d{4})",
        r"attended ([^,\.]+) (?:and|until|which he|which she) graduated in (\d{4})"
    ]

    # Find all universities
    for pattern in university_patterns:
        for match in re.finditer(pattern, text):
            university = match.group(1).strip()
            year = match.group(2)

            # Only add if not already in the list
            if university not in result["client_info"]["education"]["university"]:
                result["client_info"]["education"]["university"].append(university)
                result["client_info"]["education"]["university_graduation_years"].append(year)

    # EXTRACT OCCUPATION
    # Try to find current/last occupation
    occupation_patterns = [
        r"retired ([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) from",
        r"(\d+) year old retired ([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) from",
        r"(\d+) year old ([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) from",
        r"position of ([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) (?:at|from) ([^,\.]+).*?from (\d{4}) to (\d{4}|\w+)",
        r"role of ([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) at"
    ]

    for pattern in occupation_patterns:
        match = re.search(pattern, text)
        if match and not result["client_info"]["occupation"]:
            if "year old retired" in pattern:
                result["client_info"]["occupation"] = match.group(2).strip()
            elif "year old" in pattern and "retired" not in pattern:
                result["client_info"]["occupation"] = match.group(2).strip()
            else:
                result["client_info"]["occupation"] = match.group(1).strip()

    # EXTRACT CAREER HISTORY
    # Look for all job positions mentioned
    position_patterns = [
        r"as (?:a|an) ([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) at ([^,\.]+).*?from (\d{4}) to (\d{4}|\w+)",
        r"position of ([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) (?:at|from) ([^,\.]+).*?from (\d{4}) to (\d{4}|\w+)",
        r"worked as (?:a|an) ([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) (?:at|from) ([^,\.]+).*?from (\d{4}) to (\d{4}|\w+)"
    ]

    career_entries = []

    for pattern in position_patterns:
        for match in re.finditer(pattern, text):
            position = match.group(1).strip()
            company = match.group(2).strip()
            start_year = match.group(3)
            end_year = match.group(4)

            career_entries.append({
                "position": position,
                "company": company,
                "start_year": start_year,
                "end_year": end_year if end_year.isdigit() else "present"
            })

    # Also check for positions without explicit years
    simpler_patterns = [
        r"worked as (?:a|an) ([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) at ([^,\.]+)",
        r"position of ([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) at ([^,\.]+)",
        r"role as (?:a|an) ([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) at ([^,\.]+)"
    ]

    for pattern in simpler_patterns:
        for match in re.finditer(pattern, text):
            position = match.group(1).strip()
            company = match.group(2).strip()

            # Only add if we don't already have this position
            if not any(entry["position"] == position and entry["company"] == company for entry in career_entries):
                career_entries.append({
                    "position": position,
                    "company": company,
                    "start_year": "",
                    "end_year": ""
                })

    # Add career entries to result
    if career_entries:
        result["client_info"]["career_history"] = career_entries

    # EXTRACT LAST SALARY
    salary_match = re.search(r"(?:earned|remuneration of|compensated with|salary of) (\d+) ([A-Z]{3}) p\.A\.", text)
    if salary_match:
        result["client_info"]["last_salary"]["amount"] = salary_match.group(1)
        result["client_info"]["last_salary"]["currency"] = salary_match.group(2)

    # EXTRACT SAVINGS
    savings_patterns = [
        r"saved (?:approximately |)(\d+) ([A-Z]{3})",
        r"saving (\d+) ([A-Z]{3})",
        r"saved[^0-9]+(\d+) ([A-Z]{3})"
    ]

    for pattern in savings_patterns:
        match = re.search(pattern, text)
        if match:
            result["client_info"]["savings"]["amount"] = match.group(1)
            result["client_info"]["savings"]["currency"] = match.group(2)
            break

    # EXTRACT REAL ESTATE
    # Method 1: Look for properties with locations and values
    property_patterns = [
        r"(?:has|purchased|owns|bought) (?:a |)([a-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+) (?:located |situated |)in ([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+),?[^,\.]+?(?:worth|valued at) ([0-9,.]+) ([A-Z]{3})"
    ]

    for pattern in property_patterns:
        for match in re.finditer(pattern, text):
            property_type = match.group(1).strip()
            location = match.group(2).strip()
            value = match.group(3).replace(',', '')
            currency = match.group(4)

            result["client_info"]["real_estate"].append({
                "type": property_type,
                "location": location,
                "value": value,
                "currency": currency
            })

    # Method 2: Look for the "stunning properties" pattern
    property_count_match = re.search(r"comprises (\d+) stunning properties[^\.]+ across ([^\.]+)", text)
    if property_count_match:
        count = int(property_count_match.group(1))
        locations_text = property_count_match.group(2)

        # Split locations by 'and' or commas
        locations = re.split(r' and |, ', locations_text)

        for i, location in enumerate(locations[:count]):  # Limit to the number mentioned
            result["client_info"]["real_estate"].append({
                "type": "Property",
                "location": location.strip(),
                "value": "",
                "currency": ""
            })

    # EXTRACT INHERITANCE DETAILS
    inheritance_patterns = [
        r"(?:inheritance|inherited|received) (?:a |an |of |)(?:significant sum of |sum of |)(\d+) ([A-Z]{3}) from (?:her|his) (?:late |)([a-z]+),\s*(?:a |an |)(?:renowned |respected |prominent |well-known |)([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+?)[,\.].*?in (\d{4})",
        r"inheritance of (\d+) ([A-Z]{3}) from (?:her|his) (?:late |)([a-z]+).*?([A-Za-zÀ-ÖØ-öø-ÿĄąĆćĘęŁłŃńÓóŚśŹźŻż\s]+?)(?:,|\.) in (\d{4})"
    ]

    for pattern in inheritance_patterns:
        match = re.search(pattern, text)
        if match:
            result["client_info"]["inheritance_details"]["amount"] = match.group(1)
            result["client_info"]["inheritance_details"]["currency"] = match.group(2)
            result["client_info"]["inheritance_details"]["relation"] = match.group(3)
            result["client_info"]["inheritance_details"]["relative_occupation"] = match.group(4).strip()
            result["client_info"]["inheritance_details"]["year"] = match.group(5)
            break

    # Check for no inheritance statement
    if "does not have any inheritances" in text:
        result["client_info"]["inheritance_details"] = {
            "amount": "0",
            "currency": "",
            "year": "",
            "relation": "",
            "relative_occupation": ""
        }

    # EXTRACT CURRENCY INFORMATION (EUR/CHF/USD)
    if any(result["client_info"]["last_salary"]["currency"] == currency or
           result["client_info"]["savings"]["currency"] == currency or
           (result["client_info"]["inheritance_details"].get("currency") == currency and
            int(result["client_info"]["inheritance_details"].get("amount", 0)) > 0) or
           any(prop["currency"] == currency for prop in result["client_info"]["real_estate"])
           for currency in ["EUR", "CHF", "USD"]):

        if "EUR" in [result["client_info"]["last_salary"]["currency"],
                     result["client_info"]["savings"]["currency"],
                     result["client_info"]["inheritance_details"].get("currency")] or \
           any(prop["currency"] == "EUR" for prop in result["client_info"]["real_estate"]):
            result["client_info"]["eur"] = "/Yes"

        if "CHF" in [result["client_info"]["last_salary"]["currency"],
                     result["client_info"]["savings"]["currency"],
                     result["client_info"]["inheritance_details"].get("currency")] or \
           any(prop["currency"] == "CHF" for prop in result["client_info"]["real_estate"]):
            result["client_info"]["chf"] = "/Yes"

        if "USD" in [result["client_info"]["last_salary"]["currency"],
                     result["client_info"]["savings"]["currency"],
                     result["client_info"]["inheritance_details"].get("currency")] or \
           any(prop["currency"] == "USD" for prop in result["client_info"]["real_estate"]):
            result["client_info"]["usd"] = "/Yes"

    # Check for other currencies
    all_currencies = [
        result["client_info"]["last_salary"]["currency"],
        result["client_info"]["savings"]["currency"],
        result["client_info"]["inheritance_details"].get("currency", "")
    ]

    all_currencies.extend([prop["currency"] for prop in result["client_info"]["real_estate"] if "currency" in prop])

    # Set other_ccy if any non-standard currency is found
    for currency in all_currencies:
        if currency and currency not in ["", "EUR", "CHF", "USD"]:
            result["client_info"]["other_ccy"] = currency
            break

    # Clean up empty structures
    if not any(result["client_info"]["education"].values()):
        result["client_info"]["education"] = {}

    if not any(result["client_info"]["inheritance_details"].values()):
        result["client_info"]["inheritance_details"] = {}

    if not result["client_info"]["last_salary"]["amount"]:
        result["client_info"]["last_salary"] = {}

    if not result["client_info"]["savings"]["amount"]:
        result["client_info"]["savings"] = {}

    if not result["client_info"]["real_estate"]:
        result["client_info"]["real_estate"] = []

    if not result["client_info"]["career_history"]:
        result["client_info"]["career_history"] = []

    return result


def process_text_file(file_path):
    """
    Process a text file and extract client information.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
        return extract_client_info_from_text(text_content)
    except Exception as e:
        print(f"Error processing text file: {e}")
        return {"error": str(e)}

class TXTProcessor:
    def __init__(self, file_path):
        self.file_path = file_path


    def extract_client_info(self) -> List[Feature]:
        data = process_text_file(self.file_path)
        features: List[Feature] = [Feature(key=key, value=value, coordinates={}) for key, value in data.items()]
        return features
        
    # Run all steps
    def run_pipeline(self) -> List[Feature]:
        return self.extract_client_info()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        result = process_text_file(file_path)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Usage: python text_extractor.py [path_to_text_file]")
        print("This script extracts client information from a text description.")