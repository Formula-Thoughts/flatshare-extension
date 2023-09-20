import { useEffect, useState } from "react";
import { stockData } from "./stock";
import styled from "styled-components";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowUpRightFromSquare } from "@fortawesome/free-solid-svg-icons";
import { faHouseChimney } from "@fortawesome/free-solid-svg-icons";
import FlatImage, { FlatImageProps } from "./FlatImage";

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

export const Flats = () => {
  const [items, setItems] = useState<any[]>([]);
  const apiUrl = "Some aws endpoint"; // Replace with your API endpoint

  useEffect(() => {
    // Fetch data from the API
    fetch(apiUrl)
      .then((response) => response.json())
      .then((data) => setItems(data))
      .catch((error) => {
        console.error("Error fetching data:", error);
        setItems(stockData); // TODO: remove this line when API Completed
      });
  }, []);
  return (
    <div>
      <div style={{ padding: 10 }}>List of flats</div>
      <div className="App">
        {items.map((item) => {
          return (
            <FlatCard
              key={item.id}
              onClick={() => {
                chrome.tabs.create({ url: item.name });
              }}
            >
              <FlatCardHeader>
                <FontAwesomeIcon icon={faHouseChimney} />
                <FontAwesomeIcon
                  icon={faArrowUpRightFromSquare}
                  onClick={() => {
                    chrome.tabs.create({ url: item.name });
                  }}
                />
              </FlatCardHeader>
              <FlatCardBody>
                <FlatName>{stripIdFromUrl(item.name)}</FlatName>
                <FlatImage item={item as FlatImageProps} />
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
