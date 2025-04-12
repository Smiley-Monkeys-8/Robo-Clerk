import ImgHowItWorks from "../assets/images/img-how-it-works.jpg";
import Tick from "../assets/icons/tick.svg";
import { Link } from "react-router-dom";

export const HowItWorks = () => {
  return (
    <div className="flex bg-black-haze  pt-10 justify-evenly items-center pb-7">
      <div>
        <img
          src={ImgHowItWorks}
          alt="Illustration of a man and a woman with paperwork"
        />
      </div>
      <div>
        <h2 className="text-4xl mb-9 ">How It Works</h2>
        <p className="text-xl mb-6 ">
          Your documents & Our smart review process{" "}
        </p>
        <h2 className="text-4xl mb-9 ">What we look for?</h2>

        <div className="flex items-center gap-3 mb-6">
          <img src={Tick} alt="Tick icon" />
          <p className="text-xl ">Name matches </p>
        </div>

        <div className="flex items-center gap-3 mb-6">
          <img src={Tick} alt="Tick icon" />
          <p className="text-xl ">Personal information consistency</p>
        </div>

        <div className="flex items-center gap-3 mb-6">
          <img src={Tick} alt="Tick icon" />
          <p className="text-xl ">Potential discrepancies</p>
        </div>

        <div className="flex items-center gap-3 mb-16">
          <img src={Tick} alt="Tick icon" />
          <p className="text-xl ">Hidden red flags </p>
        </div>

        <Link
          className="verlag-bold text-white bg-blue-zodiac py-4 px-8 hover:bg-blue-800"
          to="/review"
        >
          BEGIN REVIEW
        </Link>
      </div>
    </div>
  );
};

export default HowItWorks;
