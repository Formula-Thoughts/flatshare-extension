import React, { useState } from "react";
import { SelectGroupProps } from "./SelectGroup";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";

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

export const JoinGroup = (props: SelectGroupProps) => {
  const navigate = useNavigate();

  const { Block, Button } = props;
  const [inputValue, setInputValue] = useState("");
  const changeValue = (e: { target: { value: string } }) => {
    setInputValue(e.target.value.toUpperCase());
  };
  const handleEnterKeyPress = (
    e: React.KeyboardEvent,
    f: (e: React.KeyboardEvent) => void
  ) => {
    if (e.key === "Enter") {
      f(e);
    }
  };
  const joinExistingGroup = (event: any) => {
    chrome.storage.local.set({ groupSelected: "other" }, function () {
      if (chrome.runtime.lastError) {
        console.error(chrome.runtime.lastError);
      } else {
        chrome.storage.local.set({ groupOther: inputValue }, function () {
          if (chrome.runtime.lastError) {
            console.error(chrome.runtime.lastError);
          } else {
            navigate("/Flats");
          }
        });
      }
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
        onKeyDown={(event) =>
          handleEnterKeyPress(event, (event) => joinExistingGroup)
        }
        maxLength={8}
      />

      <Button onClick={(event: any) => joinExistingGroup(event)}>
        Join existing group
      </Button>
    </Block>
  );
};
