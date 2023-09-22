import { useEffect, useState } from "react";
import styled from "styled-components";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowUpRightFromSquare } from "@fortawesome/free-solid-svg-icons";
import { faHouseChimney } from "@fortawesome/free-solid-svg-icons";
import SaveDataButton from "./SaveDataButton";

const FlatCard = styled.div`
  display: flex;
  justify-content: space-between;
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 10px;
  margin: 10px;
  width: 300px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: left;
  background-color: #2a4d1a;
  flex-direction: column;
  gap: 10px;
  cursor: pointer;
`;

const FlatCardHeader = styled.div`
  display: flex;
  justify-content: space-between;
`;

const FlatCardBody = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const FlatName = styled.div`
  font-size: 18px;
  background-color: #2a4d1a;
`;

type Flat = {
  id: string;
  title: string;
  url: string;
  price: string;
};

export const Flats = () => {
  const [items, setItems] = useState<Flat[]>([]);
  const apiUrl = "Some aws endpoint"; // Replace with your API endpoint
  const addFlat = (title: string, url: string, price: string) => {
    const newFlat: Flat = {
      id: (items.length + 1).toString(),
      title: title,
      url: url,
      price: price,
    };
    setItems([...items, newFlat]);
  };
  // useEffect(() => {
  //   // Fetch data from the API
  //   fetch(apiUrl)
  //     .then((response) => response.json())
  //     .then((data) => setItems(data))
  //     .catch((error) => {
  //       // console.log("Error fetching data:", error);
  //       // setItems(stockData); // TODO: remove this line when API Completed
  //     });
  // }, []);

  useEffect(() => {
    // Retrieve the data from storage when the popup opens
    chrome.storage.local.get({ items: [] }, (result) => {
      const { items } = result;
      setItems(items);
    });
  }, []);

  useEffect(() => {
    // Listen for messages from the background script
    chrome.runtime.onMessage.addListener((message) => {
      if (message.action === "updatePopup") {
        // Trigger a re-render by updating the state
        setItems((items) => [...items, message.message]);
      }
    });
  }, []);

  return (
    <div>
      <div style={{ padding: 10 }}>List of flats</div>
      <div style={{ padding: 10 }}>
        <SaveDataButton onClickAction={addFlat} />
      </div>
      <div className="App">
        {items.length === 0 && <div>No flats found</div>}
        {items.map((item) => {
          return (
            <FlatCard
              key={item.id}
              onClick={() => {
                chrome.tabs.create({ url: item.url });
              }}
            >
              <FlatCardHeader>
                <FontAwesomeIcon icon={faHouseChimney} />
                <FlatName>{item.price}</FlatName>
                <FontAwesomeIcon
                  icon={faArrowUpRightFromSquare}
                  onClick={() => {
                    chrome.tabs.create({ url: item.url });
                  }}
                />
              </FlatCardHeader>
              <FlatCardBody>
                <FlatName>{item.title}</FlatName>
              </FlatCardBody>
            </FlatCard>
          );
        })}
      </div>
    </div>
  );
};

// this only works for the rightmove urls
// eg. https://www.rightmove.co.uk/properties/140079353#/?channel=RES_LET
const stripIdFromUrl = (url: string) => {
  const urlParts = url.split("/");
  return urlParts[urlParts.length - 2];
};
