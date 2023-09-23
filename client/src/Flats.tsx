import styled from "styled-components";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowUpRightFromSquare } from "@fortawesome/free-solid-svg-icons";
import { faHouseChimney } from "@fortawesome/free-solid-svg-icons";
import { useFlats } from "./context/FlatsContext";

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
  const { flats } = useFlats();

  // useEffect(() => {
  //   // Listen for messages from the background script
  //   chrome.runtime.onMessage.addListener((message) => {
  //     if (message.action === "updatePopup") {
  //       // Trigger a re-render by updating the state
  //       setItems((items) => [...items, message.message]);
  //     }
  //   });
  // }, []);

  return (
    <div>
      <div style={{ padding: 10 }}>List of flats</div>
      <p>{JSON.stringify(flats)}</p>
      <div className="App">
        {flats.length === 0 && <div>No flats found</div>}
        {flats.map((item) => {
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
