import Logo from "./assets/flatini-logo.png";
import "./App.css";
import { Routes, Route, useNavigate } from "react-router-dom";
import { Landing } from "./Landing";
import CreateGroup from "./CreateGroup";
import { Flats } from "./Flats";

function App() {
  const navigate = useNavigate();
  function gotoLanding(): void {
    navigate("/");
  }

  return (
    <>
      <header style={{ cursor: "pointer" }} onClick={gotoLanding}>
        <img style={{ width: 110 }} src={Logo} />
      </header>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/Flats" element={<Flats />} />
        <Route path="/CreateGroup" element={<CreateGroup />} />
      </Routes>
    </>
  );
}

export default App;
