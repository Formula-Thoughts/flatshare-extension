import { SetStateAction, useState } from "react";
import { Link } from "react-router-dom";
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

  // Handle programmatic navigation when user clicks
  // Create a new group button
  const navigate = useNavigate();
  const createNewGroup = () => navigate("/CreateGroup");

  // Handle exiting group id input field state
  const [inputValue, setInputValue] = useState("");

  // Handle enter key press in exiting group id input. If enter
  // key is pressed, call the function passed as second argument
  const handleEnterKeyPress = (e: { key: string }, f: () => void) => {
    if (e.key === "Enter") {
      f();
    }
  };

  // Only allow digits in the exiting group id input
  const allowDigitsOnly = (e: { target: { value: string } }) => {
    const numericValue = e.target.value.replace(/[^0-9]/g, "");
    setInputValue(numericValue);
  };

  const joinExistingGroup = () => {
    console.log("joinExistingGroup");
  };

  return (
    <Wrapper style={{ top: 30 }}>
      <Block
        style={{
          maxHeight: 30,
          backgroundColor: "#322848",
          display: "flex",
          justifyContent: "flex-start",
          flexDirection: "row",
        }}
      >
        <Link
          style={{ marginLeft: 10, color: "#ccc", textDecoration: "none" }}
          to="Flats"
        >
          My flat links
        </Link>
      </Block>
      <Block>
        <p>
          Create a group with your flatmates and start sharing links to find
          your next flat.
        </p>
        <Button onClick={createNewGroup}>Create a new group</Button>
      </Block>
      <Block $bgColor="#322848">
        <p>Join an existing group one of your flatmates has already created</p>
        <Input
          type="text"
          $topMargin="10px"
          placeholder="Enter the group ID"
          value={inputValue}
          onChange={allowDigitsOnly}
          onKeyDown={(event) => handleEnterKeyPress(event, joinExistingGroup)}
        />
        <Button $disabled={inputValue === ""} onClick={joinExistingGroup}>
          Join existing group
        </Button>
      </Block>
    </Wrapper>
  );
};
