import { useEffect, useState } from "react";
import styled from "styled-components";
import Button from "./Button";
import { useNavigate } from "react-router-dom";
import { NewGroup } from "./NewGroup";
import { JoinGroup } from "./JoinGroup";

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

export interface SelectGroupProps {
  Block: React.ComponentType<any>;
  Button: React.ComponentType<any>;
}

export const SelectGroup = () => {
  const navigate = useNavigate();

  const [whichGroup, setWhichGroup] = useState(undefined);

  useEffect(() => {
    chrome.storage.local.get("groupSelected", (result) => {
      if (chrome.runtime.lastError) {
        console.error(chrome.runtime.lastError);
      } else {
        if (result?.groupSelected) {
          setWhichGroup(result.groupSelected);
        }
      }
    });
  }, []);

  if (whichGroup) {
    navigate("/Flats");
  }

  return (
    <Wrapper style={{ top: 30 }}>
      <NewGroup Block={Block} Button={Button} />
      <JoinGroup Block={Block} Button={Button} />
    </Wrapper>
  );
};
