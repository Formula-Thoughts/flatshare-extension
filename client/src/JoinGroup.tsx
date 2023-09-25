import React, { useState } from "react";
import { SelectGroupProps } from "./SelectGroup";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import { useFlats } from "./context/FlatsContext";

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

const Text = styled.p`
  font-size: 14px;
  text-align: left;
`;

const ErrorContainer = styled.div<{ $show: boolean }>`
  height: 20px;
  background-color: ${(props) => (props.$show ? "#322848" : "transparent")};
`;

export const JoinGroup = (props: SelectGroupProps) => {
  const { setGroupCode, setFlats } = useFlats();
  const navigate = useNavigate();
  const [showError, setShowError] = useState(false);
  const [joinBtnOn, setJoinBtnOn] = useState(false);
  const { Block, Button } = props;
  const [inputValue, setInputValue] = useState("");

  const changeValue = (e: { target: { value: string } }) => {
    setInputValue(e.target.value.toUpperCase());
    setShowError(false);
    setJoinBtnOn(e.target.value.length === 8);
  };
  const handleEnterKeyPress = (e: React.KeyboardEvent, f: () => void) => {
    if (e.key === "Enter" && joinBtnOn) {
      f();
    }
  };
  const joinExistingGroup = () => {
    const url =
      "https://gbjrcfuc7b.execute-api.eu-west-2.amazonaws.com/groups/" +
      inputValue;

    fetch(url, {
      method: "Get",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (!response.ok) {
          console.log(`Network response was not ok:`, response);
          setShowError(true);
          return;
        }
        return response.json();
      })
      .then((data) => {
        if (data) {
          console.log("Calling GET groups", data);
          setGroupCode(data.code);
          setFlats(data.flats);
          navigate("/Flats");
        }
      })
      .catch((error) => {
        console.error("There was a problem with the fetch operation:", error);
      });
  };
  return (
    <Block $bgColor="#322848">
      <p>Join an existing group one of your flatmates has already created</p>
      <Input
        type="text"
        $topMargin="10px"
        placeholder="Enter the group code"
        value={inputValue}
        onChange={changeValue}
        onKeyDown={(event) => handleEnterKeyPress(event, joinExistingGroup)}
        maxLength={8}
      />

      <Button $disabled={!joinBtnOn} onClick={() => joinExistingGroup()}>
        Join existing group
      </Button>
      <ErrorContainer $show={showError}>
        {showError && <Text>Error: Group code not found</Text>}
      </ErrorContainer>
    </Block>
  );
};
