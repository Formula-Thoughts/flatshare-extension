import { useLocation, useNavigate } from "react-router-dom";
import ColorLayout from "./layouts/ColorLayout";
import styled from "styled-components";
import { useState } from "react";
import { _addRedFlag } from "./utils/resources";
import { useProvider } from "./context/AppProvider";
import { FaArrowLeft } from "react-icons/fa";
import { Button, InputText, Text, TextTypes } from "flatini-fe-library";

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 5rem;

  & ::placeholder {
    color: white !important;
    opacity: 0.5;
  }
`;

const EditableDiv = styled.div`
  color: white;
  font-size: 1.5rem;
  padding: 1rem 0;
  cursor: text;
  line-height: 2rem;

  /* Placeholder styling */
  &:empty:before {
    content: attr(data-placeholder);
    opacity: 0.5;
  }
`;

type Data = {
  flatName: string;
  flatUrl: string;
};

const AddRedFlags = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [newRedFlag, setNewRedFlag] = useState("");

  const { userAuthToken, setActiveFlatData, activeFlatData } = useProvider();

  const addRedFlag = async () => {
    const response = await _addRedFlag(
      userAuthToken,
      activeFlatData.url,
      newRedFlag
    );
    console.log("response", response);
    setActiveFlatData({
      ...activeFlatData,
      redFlags: [...activeFlatData.redFlags, { ...response.redFlag }],
    });
    navigate("/RedFlags");
  };

  return (
    <ColorLayout>
      <Button onClick={() => navigate("/RedFlags")}>
        <FaArrowLeft />
      </Button>
      <Wrapper>
        <Text type={TextTypes.title}>🚩 Add a red flag</Text>
        <Text type={TextTypes.small}>
          Tell us about the problems you've seen in{" "}
          <span style={{ fontWeight: "bold" }}>{activeFlatData?.title}</span>.
          Don't worry, it's 100% anonymous.
        </Text>
        <InputText
          name="text"
          placeholder="Enter your text here..."
          style={{ width: "100%", minHeight: "150px" }}
          onChange={(value) => {
            setNewRedFlag(value);
          }}
        />
        <Button
          style={{
            width: "100%",
          }}
          onClick={() => addRedFlag()}
          label="Add red flag"
        />
      </Wrapper>
    </ColorLayout>
  );
};

export default AddRedFlags;
