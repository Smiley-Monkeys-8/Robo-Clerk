import Logo from "../../assets/JB-logo.svg";
import { Link } from "react-router-dom";

export const Header = () => {
  return (
    <header className="bg-blue-zodiac text-white py-4 px-5 border-b border-white flex justify-between items-center">
      <Link to="/">
        <img src={Logo} alt="Julius Baer Logo" />{" "}
      </Link>
      <ul className="flex gap-10">
        <Link
          to="/"
          className="text-xl hover:underline-offset-4 hover:underline"
        >
          Home
        </Link>
        <Link
          to="how-it-works"
          className="text-xl hover:underline-offset-4 hover:underline"
        >
          How it works
        </Link>
        <Link
          to="/review"
          className="text-xl hover:underline-offset-4 hover:underline"
        >
          Review
        </Link>
      </ul>
    </header>
  );
};
export default Header;
