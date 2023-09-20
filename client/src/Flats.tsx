import { useEffect, useState } from "react";
import { stockData } from "./stock";
import styled from "styled-components";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowUpRightFromSquare } from "@fortawesome/free-solid-svg-icons";

const FlatCard = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 10px;
  margin: 10px;
  width: 300px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: left;
  background-color: #2a4d1a;
`;

const FlatName = styled.div`
  font-weight: bold;
  font-size: 18px;
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
      <div style={{ padding: 10 }}>List of flats </div>
      <div className="App">
        <ul>
          {items.map((item) => (
            <FlatCard key={item.id}>
              <li key={item.id}>
                <FlatName>{item.name}</FlatName>
              </li>
              <FontAwesomeIcon icon={faArrowUpRightFromSquare} />
            </FlatCard>
          ))}
        </ul>
      </div>
    </div>
  );
};
