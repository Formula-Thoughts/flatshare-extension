import React from "react";
import Logo from "../dwelly-library/components/Logo";
import styled from "styled-components";
import Text, { TextTypes } from "../dwelly-library/components/Text";
import { useNavigate } from "react-router";

const Wrapper = styled.div`
  padding: 1rem;
`;

const NavBar = styled.div`
  display: flex;
  gap: 2rem;
`;

const Header = () => {
  const navigate = useNavigate();
  return (
    <Wrapper>
      <Logo style={{ width: "8rem" }} />
      <NavBar>
        <div onClick={() => navigate("/")}>
          <Text type={TextTypes.paragraph}>Flats</Text>
        </div>
        <div onClick={() => navigate("/Settings")}>
          <Text type={TextTypes.paragraph}>Settings</Text>
        </div>
        <div onClick={() => navigate("/Invitations")}>
          <Text type={TextTypes.paragraph}>Invitations</Text>
        </div>
      </NavBar>
    </Wrapper>
  );
};

export default Header;
