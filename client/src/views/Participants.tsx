import React, { useEffect, useState } from "react";
import styled from "styled-components";
import MainLayout from "../layouts/MainLayout";
import Button from "../flatini-library/components/Button";
import { useProvider } from "../context/AppProvider";
import { FaCheck } from "react-icons/fa";
import Text, { TextTypes } from "../flatini-library/components/Text";
import { flatiniAuthWebsite } from "../utils/constants";
import UserCircle from "../flatini-library/components/UserCircle";

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

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
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [shareCode]);

  return (
    <MainLayout>
      <Wrapper>
        <div
          style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}
        >
          <Text type={TextTypes.title}>Participants</Text>
          <Text type={TextTypes.small}>Add people to your group</Text>
        </div>
        <ul>
          {participants?.map((participant: string) => {
            return (
              <li
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "flex-start",
                  gap: "1rem",
                }}
              >
                <UserCircle>{Array.from(participant)[0]}</UserCircle>
                <Text type={TextTypes.title}>{participant}</Text>
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
              <div
                style={{
                  marginTop: "1rem",
                  display: "flex",
                  gap: "1rem",
                }}
              >
                <FaCheck size={20} />
                <div>
                  <Text
                    type={TextTypes.paragraph}
                    style={{ fontWeight: "bold", marginBottom: "0.5rem" }}
                  >
                    Link copied to clipboard!
                  </Text>
                  <Text type={TextTypes.small}>
                    Share this link with someone so they can login to Flatini
                    and join your group
                  </Text>
                </div>
              </div>
            ) : null}
          </div>
        </AddMembers>
      </Wrapper>
    </MainLayout>
  );
};

export default Participants;
