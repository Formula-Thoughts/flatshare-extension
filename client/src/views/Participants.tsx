import React, { useEffect, useState } from "react";
import styled from "styled-components";
import MainLayout from "../layouts/MainLayout";
import Button from "../flatini-library/components/Button";
import { useProvider } from "../context/AppProvider";
import { FaClipboard } from "react-icons/fa";
import Text, { TextTypes } from "../flatini-library/components/Text";
import { flatiniAuthWebsite } from "../utils/constants";

const Wrapper = styled.div``;

const AddMembers = styled.div``;

const Participants = () => {
  const [shareCode, setShareCode] = useState(null);
  const { getGroupShareCode, participants } = useProvider();

  const copyToClipboard = async () => {
    if (shareCode) {
      if ("clipboard" in navigator) {
        await navigator.clipboard.writeText(
          `${flatiniAuthWebsite}invite?groupCode=${shareCode}`
        );
      } else {
        document.execCommand(
          "copy",
          true,
          `${flatiniAuthWebsite}invite?groupCode=${shareCode}`
        );
      }
    }
  };

  useEffect(() => {
    copyToClipboard();
  }, [shareCode]);

  return (
    <MainLayout>
      <Wrapper>
        <Text type={TextTypes.small}>Participants</Text>
        <ul style={{ marginBottom: "1rem" }}>
          {participants?.map((participant: string) => {
            return (
              <li>
                <Text type={TextTypes.paragraph}>{participant}</Text>
              </li>
            );
          })}
        </ul>
        <AddMembers>
          <div>
            <Button
              onClick={async () => {
                setShareCode(await getGroupShareCode());
              }}
              label="Share code to invite"
            />
            {shareCode ? (
              <div style={{ marginTop: "1rem" }}>
                <FaClipboard />
                Code copied to clipboard!
              </div>
            ) : null}
          </div>
        </AddMembers>
      </Wrapper>
    </MainLayout>
  );
};

export default Participants;
