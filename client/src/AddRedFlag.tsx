import { useLocation, useNavigate } from "react-router-dom";
import Text, { TextTypes } from "./flatini-library/components/Text";
import ColorLayout from "./layouts/ColorLayout";
import styled from "styled-components";
import InputText from "./flatini-library/components/InputText";
import { useState } from "react";
import Button from "./flatini-library/components/Button";
import { _addRedFlag } from "./utils/resources";
import { useProvider } from "./context/AppProvider";

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
      <Button onClick={() => navigate("/RedFlags")} label="Back to flags" />
      <Wrapper>
        <Text type={TextTypes.title}>Add a red flag</Text>
        <Text type={TextTypes.paragraph}>
          Tell us about the problems you've seen in {activeFlatData.flatName}
        </Text>
        <Text type={TextTypes.paragraph}>
          Don't worry, it's 100% anonymous.
        </Text>
        <InputText
          type="text"
          name="new-red-flag"
          placeholder="Type here..."
          value={newRedFlag as string}
          defaultValue={""}
          style={{ color: "white" }}
          onChange={(value) => setNewRedFlag(value)}
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
