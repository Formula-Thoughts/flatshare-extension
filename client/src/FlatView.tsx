import React, { useEffect, useState } from "react";
import styled from "styled-components";
import Button from "./Button";
import { Flat, useFlats } from "./context/FlatsContext";
import SaveDataButton from "./SaveDataButton";

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
  const { flats, setFlats } = useFlats();
  // TODO - this isn't working yet as window.location.href gets the extension's url, not browser.
  const checkForDuplication = () => {
    if (flats.find((flat: Flat) => flat.url === window.location.href)) {
      return true;
    }
    console.log(false);
    return false;
  };

  const [mode, setMode] = useState(
    checkForDuplication() ? "DuplicatedFlat" : "AvailableFlat"
  );

  const addFlat = (title: string, url: string, price: string) => {
    const newFlat: Flat = {
      id: (flats.length + 1).toString(),
      title: title,
      url: url,
      price: price,
    };
    setFlats([...flats, newFlat]);
    setMode("DuplicatedFlat");
  };

  if (mode === "DuplicatedFlat") {
    return (
      <Wrapper>
        <p>this flat is duplicated</p>
      </Wrapper>
    );
  } else {
    return (
      <Wrapper>
        <p>mode {mode}</p>
        <p>checkForDuplication {JSON.stringify(checkForDuplication())}</p>
        <p>flats {JSON.stringify(flats)}</p>
        <p>The flat you are viewing has not been added to the list yet.</p>
        {/* <Button onClick={() => {}} style={{ padding: 15, marginTop: 20 }}>
        Add to the list
      </Button> */}
        <SaveDataButton onClickAction={addFlat} />
      </Wrapper>
    );
  }
};

export default FlatView;
