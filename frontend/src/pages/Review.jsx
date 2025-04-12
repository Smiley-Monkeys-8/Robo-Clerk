import { Link } from "react-router-dom";

export const Review = () => {
  return (
    <div className="bg-black-haze">
      <div className="flex px-10 border-b border-blue-zodiac mb-10">
        <div className="border-r border-blue-zodiac pt-10 w-2/5">
          <div className="pr-5">
            <h2 className="text-4xl font-bold mb-5">Client profile</h2>
            <h3 className="text-xl mb-3">Personal Information</h3>
            <p className="mb-5">
              Client ID: JBM-2024-0563 <br />
              Full Name: Elena Rodriguez <br />
              Date of Birth: March 15, 1989 <br />
              Nationality: Spanish <br />
              Passport Number: P8976543
              <br />
              Country of Residence: United Kingdom <br />
              Occupation: Digital Marketing Consultant Contact <br />
              Email: elena.rodriguez@email.com <br />
              Phone Number: +44 7911 123456
            </p>

            <h3 className="text-xl mb-3">Financial Profile</h3>

            <p className="mb-5">
              Annual Income: £65,000 <br />
              Employment Status: Self-Employed
              <br />
              Primary Bank: Barclays Bank <br />
              Years in Current Profession: 7 <br />
            </p>
          </div>
        </div>
        <div className="pl-10 w-3/5 mb-6">
          <h2 className="text-4xl font-bold mb-4 pt-10">Report</h2>
          <div className="bg-white p-5">
            <h3 className="text-xl mb-3"> Key Findings</h3>

            <p className="mb-3">
              Identity Verification: 95% Match
              <br />
              Document Consistency: Moderate Concerns Detected
              <br />
              Recommendation: Additional Verification Required
              <br />
            </p>
            <h3 className="text-xl mb-3"> Detailed Analysis</h3>

            <p className="mb-3">
              Passport Image
              <br />
              Name Matching: Exact
              <br />
              Photo Quality: Clear
              <br />
              Expiration Status: Valid
              <br />
              Account PDF
              <br />
              Income Verification: Partially Confirmed
              <br />
              Bank Statement Discrepancy: Minor inconsistency in address format
              <br />
              Text Description
              <br />
              Professional Details: Mostly Aligned
              <br />
              Potential Clarification Needed: Exact nature of self-employment
              <br />
              Profile Document
              <br />
              Personal Information: 90% Matching
              <br />
              Flags: Slight variation in middle name spelling
              <br />
            </p>

            <h3 className="text-xl mb-3"> Recommended Next Steps</h3>

            <p className="mb-3">
              Request clarification on self-employment details
              <br />
              Obtain additional proof of current address
              <br />
              Verify income documentation with supplementary evidence
              <br />
            </p>
            <h3 className="text-xl mb-3"> Confidence Breakdown</h3>

            <p>
              Confidence Breakdown
              <br />
              Personal Identity: High Confidence
              <br />
              Financial Information: Moderate Confidence
              <br />
              Overall Profile: Needs Further Verification
              <br />
            </p>
          </div>
        </div>
      </div>
      <div className="flex w-full px-10 pb-10 justify-end">
        <Link
          className="verlag-bold text-white bg-blue-zodiac py-3 px-16 hover:bg-blue-800"
          to="/review"
        >
          NEXT
        </Link>
      </div>
    </div>
  );
};
export default Review;
