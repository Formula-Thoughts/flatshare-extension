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
import Image from "./flatini-library/components/Image";
import NoFlatsFoundImage from "./assets/no-flats-found.png";
import UserCircle from "./flatini-library/components/UserCircle";

const FlatList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
`;

const FlatCard = styled.div`
  position: relative;
`;

const FlatCardBody = styled.div`
  cursor: pointer;

  &:hover {
    .title {
      text-decoration: underline;
    }
  }
`;

const NoFlatsFound = styled.div`
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  flex-direction: column;
`;

export const Flats = () => {
  const { flats } = useProvider();

  return (
    <MainLayout>
      <div className="App">
        {flats?.length === 0 && (
          <NoFlatsFound>
            {
              <Image
                style={{ width: "100%" }}
                alt="No flats found image"
                src={NoFlatsFoundImage}
              />
            }
            <Text type={TextTypes.title}>No flats added yet.</Text>
            <Text type={TextTypes.paragraph}>
              With the extension open, visit a flat for rent in{" "}
              <a
                href="https://www.rightmove.co.uk/property-to-rent.html"
                target="_blank"
              >
                Rightmove
              </a>
              ,{" "}
              <a
                href="https://www.zoopla.co.uk/to-rent/property/london/"
                target="_blank"
              >
                Zoopla
              </a>
              ,{" "}
              <a href="https://www.openrent.co.uk/" target="_blank">
                OpenRent
              </a>{" "}
              or{" "}
              <a href="https://www.spareroom.co.uk/" target="_blank">
                SpareRoom
              </a>{" "}
              and add it to your list.
            </Text>
          </NoFlatsFound>
        )}
        <FlatList>
          {flats?.map((item) => {
            return (
              <FlatCard
                key={item.id}
                onClick={() => {
                  chrome.tabs.create({ url: item.url });
                }}
              >
                <div
                  style={{
                    display: "flex",
                    gap: "1rem",
                    alignItems: "flex-start",
                    justifyContent: "center",
                  }}
                >
                  <FontAwesomeIcon
                    style={{ fontSize: "1.4rem", opacity: 0.5 }}
                    icon={faHouseChimney}
                  />
                  <FlatCardBody style={{ marginBottom: "1rem" }}>
                    <Text className="title" type={TextTypes.title}>
                      {item.title}
                    </Text>
                    <div style={{ marginTop: "0.5rem" }}>
                      <Text type={TextTypes.small}>
                        <span style={{ opacity: 0.7 }}>Added by</span>{" "}
                        <UserCircle>
                          {Array.from(item.addedBy as string)[0]}
                        </UserCircle>{" "}
                      </Text>
                      <Text type={TextTypes.small}>£ {item.price}</Text>
                    </div>
                  </FlatCardBody>
                </div>
              </FlatCard>
            );
          })}
        </FlatList>
      </div>
    </MainLayout>
  );
};
