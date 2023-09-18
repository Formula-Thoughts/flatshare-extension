import React from "react";
import Logo from "./assets/flatini-logo.png";
import "./App.css";
import { Routes, Route } from "react-router-dom";
import { Landing } from "./Landing";
import styled from "styled-components";
import CreateGroup from "./CreateGroup";

const Header = styled.div``;

function App() {
  return (
    <>
      <Header>
        <img style={{ width: 110 }} src={Logo} />
      </Header>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/CreateGroup" element={<CreateGroup />} />
      </Routes>
    </>
  );
}

export default App;
