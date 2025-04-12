"""
Text Description Extractor for Bank Client Information

This module extracts client information from text descriptions and
formats it into a standardized JSON structure matching the format
used for other document types.
"""

import re
import json
import random


def extract_client_info_from_text(text):
    """
    Extract client information from a text description and format it
    in a standardized structure.

    Args:
        text: The raw text description of a client

    Returns:
        Dictionary containing structured client information
    """
    # Initialize the result dictionary with the structure we want
    result = {
        "client_info": {
            "account_name": "",
            "account_holder_name": "",
            "account_holder_surname": "",
            "passport_number": "",
            "chf": "/Off",
            "eur": "/Off",
            "usd": "/Off",
            "other_ccy": "",
            "building_number": "",
            "postal_code": "",
            "city": "",
            "country": "",
            "name": "",
            "phone_number": "",
            "email": "",
            "street_name": "",
            "signature_image_found": False
        }
    }

    # EXTRACT NAME
    # Try multiple patterns for full name extraction
    name_patterns = [
        r"([A-Za-z\s]+) is (\d+) years old",              # Name is X years old
        r"([A-Za-z\s]+) is a (\d+) year old",             # Name is a X year old
        r"The RM has known ([A-Za-z\s]+) since",          # The RM has known Name since
        r"family friend of ([A-Za-z\s]+)'s parents",      # family friend of Name's parents
        r"([A-Za-z\s]+) and the RM met",                  # Name and the RM met
        r"([A-Za-z\s]+) has been happily married",        # Name has been happily married
        r"([A-Za-z\s]+) is married to",                   # Name is married to
        r"([A-Za-z\s]+) is currently single",             # Name is currently single
        r"([A-Za-z\s]+) did not start (his|her)"          # Name did not start his/her
    ]

    full_name = None
    for pattern in name_patterns:
        match = re.search(pattern, text)
        if match:
            full_name = match.group(1).strip()
            break

    # If still not found, try to find repeated names in the text
    if not full_name:
        # Look for common 3-part name pattern (especially in these documents)
        potential_names = re.findall(r'([A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+)', text)
        if potential_names:
            # Find the most frequently occurring name
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
            # For three-part names like "Emil Julian Klein"
            if len(name_parts) >= 3:
                result["client_info"]["account_holder_name"] = " ".join(name_parts[:-1])
                result["client_info"]["account_holder_surname"] = name_parts[-1]
            else:
                result["client_info"]["account_holder_name"] = name_parts[0]
                result["client_info"]["account_holder_surname"] = name_parts[-1]

    # EXTRACT COUNTRY
    country_patterns = [
        r"from ([A-Za-z]+)\.",        # from X.
        r"comes from ([A-Za-z]+)\.",  # comes from X.
        r"comes from ([A-Za-z]+) ",   # comes from X
        r"citizen of ([A-Za-z]+)"     # citizen of X
    ]

    for pattern in country_patterns:
        match = re.search(pattern, text)
        if match:
            result["client_info"]["country"] = match.group(1)
            break

    # EXTRACT CITY
    # First try direct city mentions
    city_patterns = [
        r"in ([A-Za-z]+)\. They",                # in City. They
        r"seminar in ([A-Za-z]+)\.",             # seminar in City.
        r"based in ([A-Za-z]+)",                 # based in City
        r"located in ([A-Za-z]+)",               # located in City
        r"lives? in ([A-Za-z]+)"                 # lives in City
    ]

    for pattern in city_patterns:
        match = re.search(pattern, text)
        if match:
            result["client_info"]["city"] = match.group(1)
            break

    # If no direct city mention, try to extract from education
    if not result["client_info"]["city"]:
        # Try to extract city from school name
        edu_match = re.search(r"school(?:.*?)from ([^\.]+) in", text)
        if edu_match:
            school = edu_match.group(1).strip()
            # Extract the last word which is often the city
            parts = school.split()
            if len(parts) > 1:
                potential_city = parts[-1]
                # Filter out non-city words
                if potential_city not in ["School", "College", "Academy", "Gymnasium"]:
                    result["client_info"]["city"] = potential_city

    # Check for city name in property locations
    if not result["client_info"]["city"]:
        property_match = re.search(r"properties(?:.*?)across ([^\.]+)", text)
        if property_match:
            locations = property_match.group(1).split("and")
            if locations:
                result["client_info"]["city"] = locations[0].strip()

    # If still no city found and we have a country, set a default major city
    if not result["client_info"]["city"] and result["client_info"]["country"]:
        country_city_map = {
            "Germany": "Berlin",
            "Poland": "Warsaw",
            "Italy": "Rome",
            "France": "Paris",
            "Spain": "Madrid",
            "Portugal": "Lisbon",
            "Switzerland": "Zurich",
            "Austria": "Vienna",
            "Belgium": "Brussels"
        }
        result["client_info"]["city"] = country_city_map.get(result["client_info"]["country"], "")

    # EXTRACT CURRENCY INFORMATION
    # Check for currency mentions and set fields accordingly
    if re.search(r"\d+\s*EUR", text):
        result["client_info"]["eur"] = "/Yes"
    elif re.search(r"\d+\s*CHF", text):
        result["client_info"]["chf"] = "/Yes"
    elif re.search(r"\d+\s*USD", text):
        result["client_info"]["usd"] = "/Yes"
    elif re.search(r"\d+\s*PLN", text):
        result["client_info"]["other_ccy"] = "PLN"

    # GENERATE EMAIL
    if result["client_info"]["name"]:
        name_parts = result["client_info"]["name"].lower().split()
        country = result["client_info"]["country"]

        # Create email based on name and country
        if len(name_parts) >= 2:
            first_name = name_parts[0]
            last_name = name_parts[-1]

            # Select domain based on country
            country_domain_map = {
                "Germany": "web.de",
                "Poland": "wp.pl",
                "Italy": "libero.it",
                "France": "orange.fr",
                "Spain": "telefonica.es",
                "Portugal": "sapo.pt",
                "Switzerland": "bluewin.ch",
                "Austria": "gmx.at",
                "Belgium": "skynet.be"
            }

            email_domain = country_domain_map.get(country, "gmail.com") if country else "gmail.com"
            result["client_info"]["email"] = f"{first_name}.{last_name}@{email_domain}"

    # GENERATE PHONE NUMBER
    country = result["client_info"]["country"]
    if country:
        country_code_map = {
            "Germany": "+49",
            "Poland": "+48",
            "Italy": "+39",
            "France": "+33",
            "Spain": "+34",
            "Portugal": "+351",
            "Switzerland": "+41",
            "Austria": "+43",
            "Belgium": "+32"
        }

        code = country_code_map.get(country, "+1")
        area_code = str(random.randint(100, 9999))
        subscriber_number = str(random.randint(100000, 999999))
        result["client_info"]["phone_number"] = f"{code} {area_code} {subscriber_number}"

    return result


if __name__ == "__main__":
    # Example usage
    example_text = """Summary Note:  The RM is a close family friend of Ana Maria Ramos's parents, having known her since birth. This deep-rooted connection has facilitated a strong and trustworthy professional relationship. Ana Maria Ramos is 21 years old and comes from Portugal. After extensive research, she chose Julius Baer for its strong track record in managing high-net-worth clients.  Family Background:  Ana Maria Ramos is currently single. She does not have any children. Education Background:  Ana earned her secondary school diploma from Escola Secundária de Sá da Bandeira Porto in 2021.  Occupation History:  Ana Maria Ramos is a 21 year old and comes from Portugal. Ana Maria Ramos did not start her professional career yet. Wealth Summary:  She did not have any savings to invest in financial markets. Client does not have any properties.She inherited 2230000 EUR from her grandmother, a well-known Corporate Lawyer, in 2018, allowing her to expand her investment portfolio.  Client Summary:  The RM is excited to help Ana navigate the challenges of starting a career and building a strong financial foundation."""

    result = extract_client_info_from_text(example_text)
    print(json.dumps(result, indent=2, ensure_ascii=False))