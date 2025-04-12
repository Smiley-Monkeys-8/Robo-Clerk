import Logo from "../../assets/JB-logo.svg";

export const Header = () => {
  return (
    <header className="bg-blue-zodiac text-white py-4 px-5 border-b border-white">
      <img src={Logo} alt="Julius Baer Logo" />{" "}
    </header>
  );
};
export default Header;
