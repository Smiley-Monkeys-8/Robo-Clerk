import os
import json
import re
from dotenv import load_dotenv
import openai


class ClientInfoExtractor:
    def __init__(self, project_root):
        # Load environment variables
        load_dotenv()

        # Determine the absolute paths for input and output
        self.project_root = os.path.abspath(os.path.join(project_root, '..', '..', '..'))
        self.default_input_path = os.path.join(self.project_root, "downloads")
        self.default_output_path = os.path.join(self.project_root, "data")

        # Ensure output directory exists
        os.makedirs(self.default_output_path, exist_ok=True)

        # Initialize SambaNova API client
        sambanova_api_key = os.getenv("SAMBANOVA_API_KEY")
        if not sambanova_api_key:
            raise ValueError("SAMBANOVA_API_KEY not found in environment variables")

        self.sambanova_client = openai.OpenAI(
            api_key=sambanova_api_key,
            base_url="https://api.sambanova.ai/v1"
        )

    def create_extraction_prompt(self, client_description):
        """
        Create a detailed prompt for extracting comprehensive client information
        """
        return f"""
        Extract comprehensive and precise client information from the following description. 
        Provide a JSON-formatted response with maximum detail and accuracy.

        CRITICAL EXTRACTION GUIDELINES:
        1. Extract ALL possible details precisely
        2. Use exact values from the text
        3. Ensure no information is missed
        4. Flatten the JSON structure where possible
        5. Keep all numerical values as strings to preserve exact representation

        Client Description:
        {client_description}

        Extraction Rules:
        - Full Name: Exact full name
        - Split Name: First name and surname
        - Preserve ALL specific details about education, career, finances
        - Include ALL family details
        - Extract EXACT values for salaries, savings, inheritance
        - Capture ALL career positions with precise years
        
          Output Format:
        {{
            "full_name": "Full Name",
            "first_name": "First Name",
            "surname": "Last Name",
            "age": "Age as string",
            "age_numeric": null,
            "nationality": "Nationality",
            "country_of_origin": "Country",
            "current_city": "City",
            "current_country": "Country",
            
            "marital_status": "Marital Status",
            "spouse_name": "Spouse Name",
            "marriage_year": "Marriage Year",
            
            "children_names": ["Child1", "Child2"],
            "children_count": null,
            
            "current_occupation": "Occupation",
            "career_total_years": "Career Years",
            
            "education_secondary_school": "Secondary School Name",
            "education_secondary_graduation_year": "Secondary Graduation Year",
            "education_universities": ["University Names"],
            "education_university_graduation_years": ["Graduation Years"],
            
            "career_history": [
                {{
                    "position": "Job Position",
                    "company": "Company Name",
                    "start_year": "Start Year",
                    "end_year": null
                }}
            ],
            
            "financial_details": {{
                "last_salary": {{
                    "amount": "Salary Amount",
                    "currency": "Salary Currency"
                }},
                "savings": {{
                    "amount": "Total Savings",
                    "currency": "Savings Currency"
                }},
                "real_estate": [
                    {{
                        "location": "Property Location",
                        "value": "Property Value",
                        "currency": "Currency",
                        "type": "Property Type"
                    }}
                ],
                "inheritance": {{
                    "amount": "Inheritance Amount",
                    "currency": "Inheritance Currency",
                    "year": "Inheritance Year",
                    "relation": "Relation",
                    "relative_occupation": "Relative's Occupation"
                }}
            }},
            
            "currency_preferences": {{
                "chf": "/Currency Preference",
                "eur": "/Currency Preference",
                "usd": "/Currency Preference"
            }},
            
            "relationship_manager_notes": "Initial Contact and Acquisition Notes"
        }}

        """

    def extract_client_info(self, client_description):
        """
        Use SambaNova API to extract structured client information
        """
        try:
            # Create extraction prompt
            prompt = self.create_extraction_prompt(client_description)

            # Call SambaNova API
            response = self.sambanova_client.chat.completions.create(
                model='Meta-Llama-3.1-8B-Instruct',
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                top_p=0.1
            )

            # Extract response content
            response_text = response.choices[0].message.content.strip()

            # Attempt to parse JSON
            try:
                # Remove any code block markers or extra text
                json_match = re.search(r'```json\n(.*?)```', response_text, re.DOTALL)
                if json_match:
                    response_text = json_match.group(1)

                # Parse the JSON
                extracted_data = json.loads(response_text)

                return extracted_data
            except json.JSONDecodeError:
                print("Failed to parse JSON. Raw response:")
                print(response_text)
                return None

        except Exception as e:
            print(f"Error in extraction: {e}")
            return None

    def process_client_description(self, input_filename='description.txt'):
        """
        Process the client description file and extract structured information
        """
        try:
            # Construct full input file path
            input_file_path = os.path.join(self.default_input_path, input_filename)

            # Read the file
            with open(input_file_path, 'r', encoding='utf-8') as file:
                client_description = file.read()

            # Extract structured information
            extracted_info = self.extract_client_info(client_description)

            if extracted_info:
                # Construct output file path
                output_filename = 'description.txt.json'
                output_file_path = os.path.join(self.default_output_path, output_filename)

                # Write extracted information to JSON file
                with open(output_file_path, 'w', encoding='utf-8') as outfile:
                    json.dump(extracted_info, outfile, indent=2)

                print(f"Client information saved to {output_file_path}")
                return extracted_info

            return None

        except Exception as e:
            print(f"Error processing client description: {e}")
            return None


def main():
    # Determine project root
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Create extractor
    extractor = ClientInfoExtractor(project_root)

    # Process the client description file
    result = extractor.process_client_description()

    # Print extracted information
    if result:
        print("\nExtracted Client Information:")
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()