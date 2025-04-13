import { Link } from "react-router-dom";
import ImgHome from "../assets/images/img-home.jpg";

const Home = () => {
  return (
    <div className=" bg-blue-zodiac min-h-screen flex justify-evenly items-center pb-7">
      <div>
        <h1 className="text-4xl mb-9 text-white">
          Making Decisions, Simplified
        </h1>
        <p className="text-xl mb-6 text-white">Drowning in paperwork?</p>
        <p className="text-xl mb-6 text-white">
          Every document tells a story.{" "}
        </p>
        <p className="text-xl mb-6 text-white">We help you see clearly.</p>
        <p className="text-xl mb-16 text-white">
          Faster. Smarter. More Accurate.
        </p>
        <Link className="verlag-bold bg-black-haze py-4 px-8 hover:bg-white" to="/how-it-works">
        GET STARTED
        </Link>
      </div>
      <div>
        <img src={ImgHome} alt="Illustration of a tired woman with paperwork" />
      </div>
    </div>
  );
};
export default Home;
