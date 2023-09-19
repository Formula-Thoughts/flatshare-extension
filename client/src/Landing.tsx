import React, { useState } from "react";
import styled from "styled-components";
import Button from "./Button";
import { Link } from "react-router-dom";

const Wrapper = styled.div`
  position: fixed;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
`;

const Block = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  text-align: center;
  p {
    max-width: 245px;
  }
`;

enum ScreenTypes {
  landing = "landing",
  enterCode = "enterCode",
  flatList = "flatList",
  flatView = "flatView",
}

export const Landing = () => {
  const [state, setState] = useState({
    activeView: ScreenTypes.landing,
  });
  return (
    <Wrapper style={{ top: 30 }}>
      <Block
        style={{
          maxHeight: 30,
          backgroundColor: "#322848",
          display: "flex",
          justifyContent: "flex-start",
          flexDirection: "row",
        }}
      >
        <Link
          style={{ marginLeft: 10, color: "#ccc", textDecoration: "none" }}
          to="Flats"
        >
          My flat links
        </Link>
      </Block>
      <Block>
        <p>
          Create a group with your flatmates and start sharing links to find
          your next flat.
        </p>
        <Link to="CreateGroup">
          <Button style={{ marginTop: 30 }}>Create a new group</Button>
        </Link>
      </Block>
      <Block style={{ backgroundColor: "#322848" }}>
        <p>Join an existing group one of your flatmates has already created</p>
      </Block>
    </Wrapper>
  );
};
