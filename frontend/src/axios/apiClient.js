// apiClient.js - With enhanced error handling and fallback
import axios from 'axios';

// Create a custom axios instance with shorter timeout
const api = axios.create({
  baseURL: '/api',
  timeout: 5000, // Shorter timeout to avoid long waits
  headers: {
    'Content-Type': 'application/json'
  }
});

// Sample fallback data for when server is unavailable
const FALLBACK_DATA = {
  "account_name_account.pdf": "Benjamin Paul Wagner",
  "account_holder_name_account.pdf": "Benjamin Paul",
  "account_holder_surname_account.pdf": "Wagner",
  "passport_number_account.pdf": "ZR9108088",
  "chf_account.pdf": "/Off",
  "eur_account.pdf": "/Yes",
  "usd_account.pdf": "/Off",
  "other_ccy_account.pdf": "",
  "building_number_account.pdf": "17",
  "postal_code_account.pdf": "0884",
  "city_account.pdf": "Bregenz",
  "country_account.pdf": "Austria",
  "name_account.pdf": "Benjamin Paul Wagner",
  "phone_number_account.pdf": "+43 683 900 6028",
  "email_account.pdf": "benjamin.wagner@gmail.com",
  "street_name_account.pdf": "Liechtensteinstraße",
  "signature_image_found_account.pdf": true,
  "country_passport.png": "OSTERREICH / Republic of Austria",
  "surname_passport.png": "WAGNER",
  "given_name_passport.png": "BENJAMIN PAUL",
  "birth_date_passport.png": "11-Jun-1986",
  "citizenship_passport.png": "Austrian'OSTERREICH",
  "sex_passport.png": "",
  "issue_date_passport.png": "27-Feb-2022",
  "expiry_date_passport.png": "26-Feb-2032",
  "passport_number_passport.png": "7RG108088",
  "last_name_profile.docx": "wagner",
  "first_name_profile.docx": "benjamin",
  "middle_name_profile.docx": "paul",
  "address_profile.docx": "liechtensteinstra e 17, 0884 bregenz",
  "country_of_domicile_profile.docx": "austria ",
  "date_of_birth_profile.docx": "1986-06-11",
  "nationality_profile.docx": "austrian ",
  "passport_no_profile.docx": "zr9108088",
  "id_type_profile.docx": "passport ",
  "id_issue_date_profile.docx": "2022-02-27",
  "id_expiry_date_profile.docx": "2032-02-26",
  "telephone_profile.docx": "e-mail",
  "gender_profile.docx": "male",
  "is the client or associated person a politically exposed person as defined in the client acceptance policy?_profile.docx": "no",
  "marital status_profile.docx": "divorced",
  "current employment and function_profile.docx": "employee",
  "total wealth estimated_profile.docx": "eur 1.5m-5m",
  "estimated assets_profile.docx": [
    "real estate",
    "business"
  ],
  "estimated total income p.a._profile.docx": "< eur 250,000",
  "commercial account_profile.docx": "no",
  "investment risk profile_profile.docx": "moderate",
  "type of mandate_profile.docx": "advisory",
  "investment experience_profile.docx": "expert",
  "investment horizon_profile.docx": "long-term",
  "email_profile.docx": "benjamin.wagner@gmail.com",
  "decision": "Accept",
  "isFallback": true
};

// Second fallback client
const FALLBACK_DATA_2 = {
  "full_name_description.txt": "Ophélie Hortense Dubois",
  "first_name_description.txt": "Ophélie",
  "surname_description.txt": "Dubois",
  "age_description.txt": "39",
  "nationality_description.txt": "French",
  "country_of_origin_description.txt": "France",
  "current_city_description.txt": "Caen",
  "current_country_description.txt": "France",
  "marital_status_description.txt": "Married",
  "spouse_name_description.txt": "Renault",
  "children_names_description.txt": ["Léa"],
  "children_count_description.txt": 1,
  "current_occupation_description.txt": "Regional Vice President",
  "career_total_years_description.txt": "15 years",
  "passport_no_profile.docx": "1G4078236",
  "email_profile.docx": "ophelie.dubois@live.fr",
  "telephone_profile.docx": "03 30 32 04 67",
  "investment_risk_profile_profile": "considerable",
  "type_of_mandate_profile": "advisory",
  "total_wealth_estimated_profile.docx": "EUR 5m-10m",
  "financial_details_description.txt": {
    "last_salary": {
      "amount": "112000",
      "currency": "EUR"
    },
    "savings": {
      "amount": "160000",
      "currency": "EUR"
    },
    "real_estate": [
      {
        "location": "Caen",
        "value": "1970000",
        "currency": "EUR",
        "type": "Townhouse"
      },
      {
        "location": "Strasbourg",
        "value": "1200000",
        "currency": "EUR",
        "type": "Condo"
      }
    ]
  },
  "decision": "Accept",
  "isFallback": true
};

// Keep track of which fallback data to use
let useSecondFallback = false;

/**
 * Client API methods
 */
const clientApi = {
  /**
   * Get the next random client
   * @returns {Promise<Object>} Client data
   */
  getNextClient: async () => {
    try {
      // Try to get data from the server first
      console.log('Attempting to fetch client data from server...');
      const response = await api.get('/next-client');
      console.log('Successfully fetched client data from server');
      return response.data;
    } catch (error) {
      // Log the error details for debugging
      console.error('Error fetching client data:', error);
      
      // Handle different error types
      let errorMessage = 'An unknown error occurred';
      
      if (error.code === 'ECONNABORTED') {
        errorMessage = 'Server request timed out. Using fallback data.';
      } else if (error.response) {
        // The server responded with a status code outside the 2xx range
        errorMessage = `Server error: ${error.response.status}. Using fallback data.`;
      } else if (error.request) {
        // The request was made but no response was received
        errorMessage = 'No response from server. Using fallback data.';
      }
      
      console.warn(errorMessage);
      
      // Return fallback data, alternating between samples
      useSecondFallback = !useSecondFallback;
      return useSecondFallback ? FALLBACK_DATA_2 : FALLBACK_DATA;
    }
  }
};

export default clientApi;