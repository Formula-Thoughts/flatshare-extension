import React, { useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCopy } from "@fortawesome/free-solid-svg-icons";
import styled from "styled-components";
import ColorfulString from "./ColorfulString"; // Import your ColorfulString component

// Styled-components for the components
const Container = styled.div`
  display: flex;
  flex-direction: column; /* Stack elements vertically */
  margin: 10px;
`;

const Row = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const Text = styled.p`
  font-size: 14px;
  text-align: left;
`;

interface MyComponentProps {}

const GroupCodeShare: React.FC<MyComponentProps> = () => {
  const [group, setGroup] = useState(undefined);

  const handleCopy = (flat: string) => {
    navigator.clipboard.writeText(flat);
  };

  useEffect(() => {
    chrome.storage.local.get("groupSelected", function (result) {
      if (chrome.runtime.lastError) {
        console.error(chrome.runtime.lastError);
      } else {
        let key = result.groupSelected === "own" ? "group" : "groupOther";
        chrome.storage.local.get(key, function (result) {
          if (chrome.runtime.lastError) {
            console.error(chrome.runtime.lastError);
          } else {
            console.log(`${key}`, result);
            setGroup(result[key]);
          }
        });
      }
    });
  }, []);

  return (
    <Container>
      <Row>
        <ColorfulString text={group} />
        <FontAwesomeIcon
          icon={faCopy}
          onClick={() => group && handleCopy(group)}
          style={{ cursor: "pointer", marginLeft: "10px", fontSize: "24px" }}
        />
      </Row>
      <Text>
        This is your group code. Share it with others to make them part of the
        group.
      </Text>
    </Container>
  );
};

export default GroupCodeShare;
