import React from "react";
import Logo from "../flatini-library/components/Logo";
import styled from "styled-components";
import Text, { TextTypes } from "../flatini-library/components/Text";
import { useNavigate } from "react-router";
import { Link } from "react-router-dom";
import { flatiniAuthWebsite } from "../utils/constants";

const Wrapper = styled.div`
  padding: 1rem;
`;

const NavBar = styled.div`
  display: flex;
  gap: 2rem;

  div {
    cursor: pointer;
  }
`;

const Header = () => {
  const navigate = useNavigate();
  return (
    <Wrapper>
      <a href={flatiniAuthWebsite} target="_blank">
        <Logo style={{ width: "8rem" }} />
      </a>
      <NavBar>
        <div onClick={() => navigate("/")}>
          <Text type={TextTypes.paragraph}>Flats</Text>
        </div>
        <div onClick={() => navigate("/Settings")}>
          <Text type={TextTypes.paragraph}>Settings</Text>
        </div>
        <div onClick={() => navigate("/Participants")}>
          <Text type={TextTypes.paragraph}>Participants</Text>
        </div>
      </NavBar>
    </Wrapper>
  );
};

export default Header;
