import React, { useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCopy } from "@fortawesome/free-solid-svg-icons";
import styled from "styled-components";
import ColorfulString from "./ColorfulString"; // Import your ColorfulString component
import { useFlats } from "./context/FlatsContext";
import { getGroupCode } from "./utils/storage";

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
  const [groupCode, setGroupCode] = useState<string>("");
  const handleCopy = (flat: string) => {
    navigator.clipboard.writeText(flat);
  };

  useEffect(() => {
    const fetchGroupCode = async () => {
      const code = await getGroupCode();
      setGroupCode(code || "");
    };
    fetchGroupCode();
  }, [getGroupCode]);

  return (
    <Container>
      <Row>
        <ColorfulString text={groupCode} />
        <FontAwesomeIcon
          icon={faCopy}
          onClick={() => handleCopy(groupCode)}
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
