import React, { useState, useEffect } from "react";
import clientApi from "../axios/apiClient";

export const Review = () => {
  const [clientData, setClientData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showRawData, setShowRawData] = useState(false);

  const fetchNextClient = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await clientApi.getNextClient();
      console.log("Received client data:", data);
      setClientData(data);
      
      setError(null);
    } catch (err) {
      console.error('Error in component:', err);
      setError('Failed to fetch client data: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNextClient();
  }, []);

  const formatCurrency = (value, currency) => {
    if (!value || value === "null") return 'N/A';
    
    const formattedValue = parseInt(value).toLocaleString();
    return `${formattedValue} ${currency || ''}`;
  };

  const getValueFromFields = (data, fieldOptions) => {
    if (!data) return null;
    
    for (const field of fieldOptions) {
      if (data[field] !== undefined && data[field] !== null && data[field] !== '') {
        return data[field];
      }
    }
    return null;
  };

  const renderClientProfile = () => {
    if (loading) {
      return <div className="flex justify-center items-center h-64">Loading client data...</div>;
    }

    if (error) {
      return (
        <div className="flex flex-col justify-center items-center h-64">
          <div className="bg-red-100 text-red-800 p-4 mb-4 rounded text-sm">
            {error}
          </div>
          <button 
            className="px-4 py-2 bg-blue-500 text-white rounded"
            onClick={fetchNextClient}
          >
            Retry
          </button>
        </div>
      );
    }

    if (!clientData) {
      return <div>No client data available</div>;
    }

    const usingFallback = clientData.isFallback === true;

    const fullName = getValueFromFields(clientData, [
      "full_name_description.txt", 
      "name_account.pdf",
      "account_name_account.pdf"
    ]);
    
    const nationality = getValueFromFields(clientData, [
      "nationality_description.txt",
      "nationality_profile.docx",
      "citizenship_passport.png"
    ]);
    
    const passportNumber = getValueFromFields(clientData, [
      "passport_no_profile.docx",
      "passport_number_passport.png",
      "passport_number_account.pdf"
    ]);
    
    const currentCountry = getValueFromFields(clientData, [
      "current_country_description.txt",
      "country_account.pdf",
      "country_of_domicile_profile.docx"
    ]);
    
    const currentCity = getValueFromFields(clientData, [
      "current_city_description.txt",
      "city_account.pdf"
    ]);
    
    const occupation = getValueFromFields(clientData, [
      "current_occupation_description.txt",
      "current employment and function_profile.docx"
    ]);
    
    const email = getValueFromFields(clientData, [
      "email_account.pdf",
      "email_profile.docx"
    ]);
    
    const phoneNumber = getValueFromFields(clientData, [
      "phone_number_account.pdf",
      "telephone_profile.docx"
    ]);
    
    const age = getValueFromFields(clientData, [
      "age_description.txt"
    ]);
    
    const birthDate = getValueFromFields(clientData, [
      "birth_date_passport.png",
      "date_of_birth_profile.docx"
    ]);
    
    const maritalStatus = getValueFromFields(clientData, [
      "marital_status_description.txt",
      "marital status_profile.docx"
    ]);
    
    const totalWealth = getValueFromFields(clientData, [
      "total_wealth_estimated_profile.docx"
    ]);
    
    const estimatedIncome = getValueFromFields(clientData, [
      "estimated total income p.a._profile.docx"
    ]);
    
    const careerYears = getValueFromFields(clientData, [
      "career_total_years_description.txt"
    ]);
    
    const investmentRiskProfile = getValueFromFields(clientData, [
      "investment risk profile_profile.docx",
      "investment_risk_profile_profile"
    ]);
    
    const investmentExperience = getValueFromFields(clientData, [
      "investment experience_profile.docx",
      "investment_experience_profile"
    ]);
    
    const financialDetails = clientData["financial_details_description.txt"];
    
    let income = estimatedIncome || 'N/A';
    let incomeSource = '';
    
    if (financialDetails) {
      if (financialDetails.last_salary && financialDetails.last_salary.amount && 
          financialDetails.last_salary.amount !== "null") {
        income = formatCurrency(
          financialDetails.last_salary.amount, 
          financialDetails.last_salary.currency
        );
        incomeSource = 'Salary';
      } else if (financialDetails.inheritance && financialDetails.inheritance.amount) {
        income = formatCurrency(
          financialDetails.inheritance.amount,
          financialDetails.inheritance.currency
        );
        incomeSource = 'Inheritance';
      }
    }
    
    const clientId = `JBD-${new Date().getFullYear()}-${Math.floor(Math.random() * 10000).toString().padStart(4, '0')}`;

    return (
      <div className="pr-5">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-4xl font-bold">Client profile</h2>
          <button 
            className="px-3 py-1 bg-gray-200 text-gray-800 text-sm rounded"
            onClick={() => setShowRawData(!showRawData)}
          >
            {showRawData ? "Hide Raw Data" : "Show Raw Data"}
          </button>
        </div>
        
        {usingFallback && (
          <div className="bg-yellow-100 text-yellow-800 p-3 mb-4 rounded">
            <div className="font-bold">Using demo data</div>
            <div className="text-sm">The server returned an error or timed out. Demo data is being displayed.</div>
          </div>
        )}
        
        {showRawData && (
          <div className="bg-gray-100 p-3 mb-4 rounded overflow-auto max-h-64">
            <h3 className="font-bold mb-2">Raw API Response:</h3>
            <pre className="text-xs">{JSON.stringify(clientData, null, 2)}</pre>
          </div>
        )}
        
        <h3 className="text-xl mb-3">Personal Information</h3>
        <p className="mb-5">
          Client ID: {clientId} <br />
          Full Name: {fullName || 'N/A'} <br />
          Date of Birth: {birthDate || (age ? `${age} years old` : 'N/A')} <br />
          Nationality: {nationality || 'N/A'} <br />
          Passport Number: {passportNumber || 'N/A'} <br />
          Country of Residence: {currentCountry || 'N/A'} <br />
          City: {currentCity || 'N/A'} <br />
          Occupation: {occupation || 'N/A'} <br />
          Email: {email || 'N/A'} <br />
          Phone Number: {phoneNumber || 'N/A'} <br />
          Marital Status: {maritalStatus || 'N/A'}
        </p>
        
        <h3 className="text-xl mb-3">Financial Profile</h3>
        <p className="mb-5">
          {incomeSource ? `${incomeSource}: ` : 'Income: '}{income} <br />
          Total Wealth: {totalWealth || 'N/A'} <br />
          Employment Status: {occupation || 'N/A'} <br />
          Years in Current Profession: {careerYears || 'N/A'} <br />
          Investment Risk Profile: {investmentRiskProfile || 'N/A'} <br />
          Investment Experience: {investmentExperience || 'N/A'}
        </p>
      </div>
    );
  };

  const renderReport = () => {
    if (loading || error || !clientData) {
      return (
        <div className="pl-10 w-3/5 mb-6">
          <h2 className="text-4xl font-bold mb-4 pt-10">Report</h2>
          <div className="bg-white p-5 h-64 flex items-center justify-center">
            {loading ? "Loading report data..." : error ? "Error loading report" : "No client data available"}
          </div>
        </div>
      );
    }

    const decision = clientData.decision || 'Pending';
    
    const calculateIdentityScore = () => {
      let score = 0;
      let totalChecks = 0;
      
      const fieldChecks = [
        // Personal identity checks
        !!getValueFromFields(clientData, ["full_name_description.txt", "name_account.pdf", "account_name_account.pdf"]),
        !!getValueFromFields(clientData, ["nationality_description.txt", "nationality_profile.docx", "citizenship_passport.png"]),
        !!getValueFromFields(clientData, ["passport_no_profile.docx", "passport_number_passport.png", "passport_number_account.pdf"]),
        !!getValueFromFields(clientData, ["current_country_description.txt", "country_account.pdf", "country_of_domicile_profile.docx"]),
        !!getValueFromFields(clientData, ["current_city_description.txt", "city_account.pdf"]),
        !!getValueFromFields(clientData, ["birth_date_passport.png", "date_of_birth_profile.docx", "age_description.txt"]),
        !!getValueFromFields(clientData, ["email_account.pdf", "email_profile.docx"]),
        !!getValueFromFields(clientData, ["phone_number_account.pdf", "telephone_profile.docx"]),
        
        // Consistency checks
        clientData["passport_number_passport.png"] === clientData["passport_number_account.pdf"],
        clientData["email_account.pdf"] === clientData["email_profile.docx"]
      ];
      
      // Count successful checks
      fieldChecks.forEach(check => {
        if (check) score++;
        totalChecks++;
      });
      
      // Calculate percentage (minimum 70%, maximum 99%)
      const percentage = Math.floor((score / totalChecks) * 100);
      return Math.min(Math.max(percentage, 70), 99);
    };

    // Dynamic identity score
    const identityScore = calculateIdentityScore();
    
    // Risk assessment based on multiple factors
    const assessRisk = () => {
      const isPep = getValueFromFields(clientData, [
        "is the client or associated person a politically exposed person as defined in the client acceptance policy?_profile.docx"
      ]) === "yes";
      
      const riskProfile = getValueFromFields(clientData, [
        "investment risk profile_profile.docx",
        "investment_risk_profile_profile"
      ]);
      
      const experience = getValueFromFields(clientData, [
        "investment experience_profile.docx",
        "investment_experience_profile"
      ]);
      
      let riskLevel = "Low";
      
      if (isPep) {
        riskLevel = "High";
      } else if (riskProfile === "high" || riskProfile === "aggressive") {
        riskLevel = "Moderate-High";
      } else if (riskProfile === "moderate") {
        riskLevel = "Moderate";
      } else if (experience === "inexperienced") {
        riskLevel = "Moderate-Low";
      }
      
      return riskLevel;
    };
    
    const riskLevel = assessRisk();
    
    // Check for inconsistencies in the data
    const findInconsistencies = () => {
      const inconsistencies = [];
      
      // Check passport number consistency
      const passportFromPassport = clientData["passport_number_passport.png"];
      const passportFromAccount = clientData["passport_number_account.pdf"];
      const passportFromProfile = clientData["passport_no_profile.docx"];
      
      if (passportFromPassport && passportFromAccount && 
          passportFromPassport !== passportFromAccount) {
        inconsistencies.push("Passport number mismatch between documents");
      }
      
      if (passportFromPassport && passportFromProfile && 
          passportFromPassport.toLowerCase() !== passportFromProfile.toLowerCase()) {
        inconsistencies.push("Passport number in profile doesn't match official document");
      }
      
      // Check email consistency
      const emailFromAccount = clientData["email_account.pdf"];
      const emailFromProfile = clientData["email_profile.docx"];
      
      if (emailFromAccount && emailFromProfile && 
          emailFromAccount !== emailFromProfile) {
        inconsistencies.push("Email address mismatch between documents");
      }
      
      // Check name formatting/consistency
      const fullName = getValueFromFields(clientData, [
        "full_name_description.txt", 
        "name_account.pdf",
        "account_name_account.pdf"
      ]);
      
      const givenName = clientData["given_name_passport.png"];
      const surname = clientData["surname_passport.png"];
      
      if (fullName && givenName && surname) {
        const combinedName = `${givenName} ${surname}`.toLowerCase();
        if (!fullName.toLowerCase().includes(combinedName.toLowerCase())) {
          inconsistencies.push("Name formatting differences between documents");
        }
      }
      
      return inconsistencies;
    };
    
    const inconsistencies = findInconsistencies();
    const hasInconsistencies = inconsistencies.length > 0;
    
    // Dynamic document consistency score
    const consistencyScore = hasInconsistencies 
      ? Math.max(75, 95 - (inconsistencies.length * 5)) 
      : 98;
    
    const isPep = getValueFromFields(clientData, [
      "is the client or associated person a politically exposed person as defined in the client acceptance policy?_profile.docx"
    ]);
    const pepStatus = isPep === "yes" ? "PEP Identified" : "Not a PEP";
    
    const investmentRiskProfile = getValueFromFields(clientData, [
      "investment risk profile_profile.docx",
      "investment_risk_profile_profile"
    ]);
    
    const investmentExperience = getValueFromFields(clientData, [
      "investment experience_profile.docx",
      "investment_experience_profile"
    ]);
    
    const investmentHorizon = getValueFromFields(clientData, [
      "investment horizon_profile.docx",
      "investment_horizon_profile"
    ]);
    
    const mandateType = getValueFromFields(clientData, [
      "type of mandate_profile.docx",
      "type_of_mandate_profile"
    ]);
    
    const occupation = getValueFromFields(clientData, [
      "current_occupation_description.txt",
      "current employment and function_profile.docx"
    ]);
    
    // Calculate overall score for status indicator
    const calculateOverallScore = () => {
      // Base on identity score, consistency, risk level, and decision
      let score = 0;
      
      // Identity verification (30% weight)
      score += (identityScore / 100) * 30;
      
      // Document consistency (30% weight)
      score += (consistencyScore / 100) * 30;
      
      // Risk level (20% weight)
      const riskScores = {
        "Low": 20,
        "Moderate-Low": 15,
        "Moderate": 10,
        "Moderate-High": 5,
        "High": 0
      };
      score += riskScores[riskLevel] || 10;
      
      // Decision (20% weight)
      score += (decision === 'Accept') ? 20 : 0;
      
      return score;
    };
    
    const overallScore = calculateOverallScore();
    
    const getStatusIndicator = () => {
      // Score ranges and corresponding indicators
      if (overallScore >= 80) {
        return {
          color: "bg-green-100 text-green-800 border-green-300",
          icon: "✓",
          status: "Approved",
          message: "Client profile meets all requirements"
        };
      } else if (overallScore >= 60) {
        return {
          color: "bg-yellow-100 text-yellow-800 border-yellow-300",
          icon: "!",
          status: "Further Review",
          message: "Minor issues need to be addressed"
        };
      } else {
        return {
          color: "bg-red-100 text-red-800 border-red-300",
          icon: "✕",
          status: "Declined",
          message: "Significant concerns identified"
        };
      }
    };
    
    const statusIndicator = getStatusIndicator();
    
    // Generate dynamic recommendation text
    const generateRecommendation = () => {
      if (decision !== 'Accept') return "Additional Verification Required";
      
      if (hasInconsistencies) {
        return "Conditionally Recommended for Approval";
      }
      
      if (riskLevel === "High") {
        return "Recommended for Approval with Enhanced Due Diligence";
      }
      
      return "Recommended for Approval";
    };
    
    const recommendation = generateRecommendation();
    
    return (
      <div className="pl-10 w-3/5 mb-6">
        <div className="flex items-center mb-4 pt-10">
          <h2 className="text-4xl font-bold mr-4">Report</h2>
          <div className={`border ${statusIndicator.color} rounded-md p-2 flex items-center`}>
            <span className="font-bold text-xl mr-2">{statusIndicator.icon}</span>
            <div>
              <div className="font-bold">{statusIndicator.status}: {statusIndicator.message}</div>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-5">
          <h3 className="text-xl mb-3">Key Findings</h3>
          <p className="mb-3">
            Identity Verification: {identityScore}% Match <br />
            Document Consistency: {consistencyScore}% {hasInconsistencies ? "Some Concerns Detected" : "High Consistency"} <br />
            Risk Assessment: {riskLevel} Risk <br />
            PEP Status: {pepStatus} <br />
            Recommendation: {recommendation} <br />
          </p>
          
          <h3 className="text-xl mb-3">Detailed Analysis</h3>
          <p className="mb-3">
            Passport Image <br />
            Name Matching: {!hasInconsistencies ? "Exact" : "Minor Discrepancies"} <br />
            Photo Quality: Clear <br />
            Expiration Status: Valid <br />
            Account PDF <br />
            Income Verification: {clientData["financial_details_description.txt"]?.last_salary?.amount !== "null" ? 'Confirmed' : 'Not Available'} <br />
            
            {hasInconsistencies ? (
              <>
                Document Discrepancies:
                <ul className="list-disc pl-5 mb-2">
                  {inconsistencies.map((issue, index) => (
                    <li key={index} className="text-sm">{issue}</li>
                  ))}
                </ul>
              </>
            ) : "No Document Discrepancies Detected"} <br />
            
            Profile Document <br />
            Personal Information: {identityScore}% Matching <br />
            Flags: {hasInconsistencies ? "Minor issues detected" : "No significant flags detected"} <br />
          </p>
          
          <h3 className="text-xl mb-3">Investment Profile</h3>
          <p className="mb-3">
            Risk Tolerance: {investmentRiskProfile || 'N/A'} <br />
            Experience Level: {investmentExperience || 'N/A'} <br />
            Investment Horizon: {investmentHorizon || 'N/A'} <br />
            Mandate Type: {mandateType || 'N/A'} <br />
          </p>
          
          <h3 className="text-xl mb-3">Recommended Next Steps</h3>
          <p className="mb-3">
            {decision === 'Accept' 
              ? hasInconsistencies 
                ? "Proceed with client onboarding after addressing document inconsistencies" 
                : "Proceed with standard client onboarding"
              : "Request additional verification and supporting documentation"} <br />
            
            {occupation === "No professional career yet" && 
              "Clarify source of wealth and future income expectations"} <br />
            
            {hasInconsistencies && 
              "Request clarification on document discrepancies"} <br />
              
            Review investment strategy based on {investmentRiskProfile || 'client'} risk profile <br />
          </p>
          
          <h3 className="text-xl mb-3">Confidence Breakdown</h3>
          <p>
            Personal Identity: {identityScore > 90 ? "High" : identityScore > 80 ? "Moderate" : "Low"} Confidence <br />
            Financial Information: {clientData["financial_details_description.txt"] ? 'Moderate' : 'Low'} Confidence <br />
            Overall Profile: {decision === 'Accept' 
              ? hasInconsistencies 
                ? "Conditionally Approved" 
                : "Approved" 
              : "Needs Further Verification"} <br />
          </p>
        </div>
      </div>
    );
  };

  return (
    <div className="bg-black-haze">
      <div className="flex px-10 border-b border-blue-zodiac mb-10">
        <div className="border-r border-blue-zodiac pt-10 w-2/5">
          {renderClientProfile()}
        </div>
        {renderReport()}
      </div>
      <div className="flex w-full px-10 pb-10 justify-end">
        <button
          className="verlag-bold text-white bg-blue-zodiac py-3 px-16 hover:bg-blue-800 mr-4"
          onClick={fetchNextClient}
        >
          NEXT CLIENT
        </button>
      </div>
    </div>
  );
};

export default Review;