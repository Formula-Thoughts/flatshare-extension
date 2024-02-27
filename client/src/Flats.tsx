import styled from "styled-components";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowUpRightFromSquare } from "@fortawesome/free-solid-svg-icons";
import { faHouseChimney } from "@fortawesome/free-solid-svg-icons";
import { useProvider } from "./context/AppProvider";
import { useEffect } from "react";
import { _getGroupById } from "./utils/resources";
import MainLayout from "./layouts/MainLayout";
import Text, { TextTypes } from "./flatini-library/components/Text";
import { Authenticator } from "@aws-amplify/ui-react";

const FlatCard = styled.div`
  position: relative;
`;

const FlatCardBody = styled.div``;

export const Flats = () => {
  const { flats } = useProvider();

  return (
    <MainLayout>
      <div className="App">
        {flats?.length === 0 && <div>No flat2 found</div>}
        {flats?.map((item) => {
          return (
            <FlatCard
              key={item.id}
              onClick={() => {
                chrome.tabs.create({ url: item.url });
              }}
            >
              <div style={{ display: "flex", gap: "1rem" }}>
                <FontAwesomeIcon
                  style={{ fontSize: "1.4rem" }}
                  icon={faHouseChimney}
                />
                <FlatCardBody>
                  <Text type={TextTypes.title}>{item.title}</Text>
                  <div>
                    <Text type={TextTypes.small}>{item.price}</Text>
                    <Text type={TextTypes.small}>Added by</Text>
                  </div>
                </FlatCardBody>
              </div>
              <FontAwesomeIcon
                icon={faArrowUpRightFromSquare}
                style={{ position: "absolute", top: 0, right: 0 }}
                onClick={() => {
                  chrome.tabs.create({ url: item.url });
                }}
              />
            </FlatCard>
          );
        })}
      </div>
    </MainLayout>
  );
};
