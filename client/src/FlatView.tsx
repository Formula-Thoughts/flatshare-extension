import React from "react";
import styled from "styled-components";
import Button from "./Button";
import { useFlats } from "./context/FlatsContext";

const Wrapper = styled.div`
  position: fixed;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 50px 20px;
`;

const FlatView = () => {
  const { flats } = useFlats();

  return (
    <Wrapper>
      <p>flats {JSON.stringify(flats)}</p>
      <p>The flat you are viewing has not been added to the list yet.</p>
      <Button onClick={() => {}} style={{ padding: 15, marginTop: 20 }}>
        Add to the list
      </Button>
    </Wrapper>
  );
};

export default FlatView;
