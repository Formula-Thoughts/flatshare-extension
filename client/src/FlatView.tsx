import { useEffect, useState } from "react";
import styled from "styled-components";
import Button from "./Button";
import SaveDataButton from "./SaveDataButton";
import { Flat, useFlats } from "./context/FlatsContext";
import { _addFlat, _deleteFlat } from "./utils/resources";
import { getGroupCode } from "./utils/storage";

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
  const { flats, setFlats, removeFlat } = useFlats();
  const [isFlatDuplicated, setIsFlatDuplicated] = useState(false);

  const checkFlatIsDuplicated = () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs.length > 0) {
        const activeTab = tabs[0];
        if (flats.find((flat: Flat) => flat.url === activeTab.url)) {
          return setIsFlatDuplicated(true);
        }
        return setIsFlatDuplicated(false);
      }
    });
  };

  const addFlat = async (title: string, url: string, price: string) => {
    const newFlat: Flat = {
      id: (flats.length + 1).toString(),
      title: title,
      url: url,
      price: price,
    };
    await _addFlat((await getGroupCode()) as string, url, price, title);
    setFlats([...flats, newFlat]);
    setIsFlatDuplicated(true);
  };

  const removeFlatFromList = () => {
    chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
      if (tabs.length > 0) {
        const activeTab = tabs[0];
        await _deleteFlat(
          (await getGroupCode()) as string,
          flats.find((flat: Flat) => flat.url === activeTab.url)?.id as string
        );
        removeFlat(activeTab.url as string);
        setIsFlatDuplicated(false);
      }
    });
  };

  useEffect(() => {
    checkFlatIsDuplicated();
  }, []);

  if (isFlatDuplicated) {
    return (
      <Wrapper style={{ backgroundColor: "#322848" }}>
        <p>The flat you’re viewing has already been added to the list</p>
        <div
          style={{ marginTop: 30, display: "flex", flexDirection: "column" }}
        >
          <Button onClick={removeFlatFromList} style={{ padding: 15 }}>
            Remove
          </Button>
        </div>
      </Wrapper>
    );
  } else {
    return (
      <Wrapper>
        <p>The flat you are viewing has not been added to the list yet.</p>
        <div style={{ marginTop: 30 }}>
          <SaveDataButton onClickAction={addFlat} />
        </div>
      </Wrapper>
    );
  }
};

export default FlatView;
