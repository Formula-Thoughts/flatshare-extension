import React from "react";
import Logo from "./assets/flatini-logo.png";
import "./App.css";
import { Routes, Route, useNavigate } from "react-router-dom";
import { Landing } from "./Landing";
import styled from "styled-components";
import CreateGroup from "./CreateGroup";
import { Flats } from "./Flats";

const Header = styled.div``;

function App() {
  const navigate = useNavigate();
  function gotoLanding(): void {
    navigate("/");
  }

  return (
    <>
      <Header style={{ cursor: "pointer" }} onClick={gotoLanding}>
        <img style={{ width: 110 }} src={Logo} />
      </Header>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/Flats" element={<Flats />} />
        <Route path="/CreateGroup" element={<CreateGroup />} />
      </Routes>
    </>
  );
}

export default App;
