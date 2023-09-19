import { SetStateAction, useState } from "react";
import styled from "styled-components";
import Button from "./Button";
import { useNavigate } from "react-router-dom";

const Wrapper = styled.div`
  position: fixed;
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const Block = styled.div<{ $bgColor?: string; $gap?: string }>`
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  text-align: center;
  p {
    max-width: 245px;
  }
  background-color: ${(props) => props.$bgColor || "transparent"};
  gap: ${(props) => props.$gap || "10px"};
`;

const Input = styled.input<{ $topMargin?: string }>`
  background-color: transparent;
  border: 2px solid #ccc;
  padding: 20px;
  width: 200px;
  border-radius: 10px;
  margin-top: ${(props) => props.$topMargin || "0"};
  &::placeholder {
    text-align: center;
  }
  color: #ccc;
`;

enum ScreenTypes {
  landing = "landing",
  enterCode = "enterCode",
  flatList = "flatList",
  flatView = "flatView",
}

export const Landing = () => {
  const [state, setState] = useState({
    activeView: ScreenTypes.landing,
  });
  const navigate = useNavigate();
  const handleOnClick = () => navigate("/CreateGroup");

  const [inputValue, setInputValue] = useState("");

  const handleInputChange = (e: {
    target: { value: SetStateAction<string> };
  }) => {
    setInputValue(e.target.value);
  };

  return (
    <Wrapper>
      <Block $gap="20px">
        <p>
          Create a group with your flatmates and start sharing links to find
          your next flat.
        </p>
        <Button onClick={handleOnClick}>Create a new group</Button>
      </Block>
      <Block $bgColor="#322848">
        <p>Join an existing group one of your flatmates has already created</p>
        <Input
          $topMargin="10px"
          type="text"
          placeholder="Enter the group ID"
          value={inputValue}
          onChange={handleInputChange}
        />
        <Button $disabled={inputValue === ""}>Join existing group</Button>
      </Block>
    </Wrapper>
  );
};
