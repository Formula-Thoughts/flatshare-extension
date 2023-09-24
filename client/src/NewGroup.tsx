import React from "react";
import { useNavigate } from "react-router-dom";
import { SelectGroupProps } from "./SelectGroup";

export const NewGroup = (props: SelectGroupProps) => {
  const { Block, Button } = props;
  const navigate = useNavigate();

  const createNewGroup = () => {
    chrome.storage.local.set({ groupSelected: "own" }, function () {
      if (chrome.runtime.lastError) {
        console.error(chrome.runtime.lastError);
      } else {
        navigate("/Flats");
      }
    });
  };

  return (
    <Block>
      <p>
        Create a group with your flatmates and start sharing links to find your
        next flat.
      </p>
      <Button onClick={createNewGroup}>Create a new group</Button>
    </Block>
  );
};
