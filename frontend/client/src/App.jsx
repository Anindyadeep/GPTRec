import Home from "./pages/home/Home";
import Auth from "./pages/auth/Auth";
import MovieDesc from "./pages/movieDesc/MovieDesc";
import Error from "./pages/error/Error";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Auth />} />
        <Route path="/home" element={<Home />} />
        <Route path="/movie/:id" element={<MovieDesc />} />
        <Route path="*" element={<Error />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;