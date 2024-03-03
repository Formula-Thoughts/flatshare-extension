import React, { useEffect, useState } from "react";
import styled from "styled-components";
import MainLayout from "../layouts/MainLayout";
import Button from "../flatini-library/components/Button";
import { useProvider } from "../context/AppProvider";
import { FaClipboard } from "react-icons/fa";

const Wrapper = styled.div``;

const AddMembers = styled.div``;

const Participants = () => {
  const [shareCode, setShareCode] = useState(null);
  const { getGroupShareCode, participants } = useProvider();

  const copyToClipboard = async () => {
    if (shareCode) {
      if ("clipboard" in navigator) {
        await navigator.clipboard.writeText(shareCode);
      } else {
        document.execCommand("copy", true, shareCode);
      }
    }
  };

  useEffect(() => {
    copyToClipboard();
  }, [shareCode]);

  return (
    <MainLayout>
      <Wrapper>
        <ul>
          {participants?.map((participant: string) => {
            return <li>{participant}</li>;
          })}
        </ul>
        <AddMembers>
          <div>
            <Button
              onClick={async () => {
                setShareCode(await getGroupShareCode());
              }}
              label="Generate share link"
            />
            {shareCode ? (
              <div>
                <FaClipboard />
                Your code has been copied to clipboard: {shareCode}
              </div>
            ) : null}
          </div>
        </AddMembers>
      </Wrapper>
    </MainLayout>
  );
};

export default Participants;
