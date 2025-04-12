import { BrowserRouter } from "react-router-dom";
import BaseLayout from "../layouts/BaseLayout";
import { Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import HowItWorks from "../pages/HowItWorks";

const PageRoutes = () => {
  return (
    <BrowserRouter>
    <BaseLayout>
      <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/how-it-works" element={<HowItWorks />} />
          {/* <Route path="/contact" element={<Contact />} />
          <Route path="*" element={<NotFound />} /> */}
      </Routes>
      </BaseLayout>

    </BrowserRouter>
  );
};
export default PageRoutes;
