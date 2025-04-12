import Header from "../components/Header/Header";

const BaseLayout = ({ children }) => {
  return (
    <div className="min-h-screen">
      <Header />
      <main>{children}</main>
    </div>
  );
};

export default BaseLayout;
