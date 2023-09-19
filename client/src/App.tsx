import Logo from "./assets/flatini-logo.png";
import "./App.css";
import { Routes, Route } from "react-router-dom";
import { Landing } from "./Landing";
import CreateGroup from "./CreateGroup";

function App() {
  return (
    <>
      <header>
        <img style={{ width: 110 }} src={Logo} alt="DOM WAS HERE" />
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/CreateGroup" element={<CreateGroup />} />
        </Routes>
      </main>
    </>
  );
}

export default App;
