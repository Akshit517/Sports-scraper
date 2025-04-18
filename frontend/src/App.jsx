import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
// import About from "./pages/About";
import CommentaryPage from "./components/CommentaryPage";
export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
  <Route path="/commentary/:matchcode" element={<CommentaryPage />} />
        {/* <Route path="/about" element={<About />} /> */}
      </Routes>
    </Router>
  );
}
