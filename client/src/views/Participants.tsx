import React, { useEffect, useState } from "react";
import styled from "styled-components";
import MainLayout from "../layouts/MainLayout";
import { useProvider } from "../context/AppProvider";
import { FaCheck } from "react-icons/fa";
import { flatiniAuthWebsite } from "../utils/constants";
import { Button, Text, TextTypes } from "flatini-fe-library";
import UserCircle from "../components/UserCircle";
import { useNavigate } from "react-router-dom";

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const AddMembers = styled.div``;

const Participants = () => {
  const [shareCode, setShareCode] = useState(null);
  const { getGroupShareCode, participants, leaveGroup } = useProvider();
  const navigate = useNavigate();

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
        <ul style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
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
          <div
            style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}
          >
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
            <div
              onClick={() => {
                leaveGroup();
                navigate("/");
              }}
            >
              <Text
                type={TextTypes.paragraph}
                style={{ textAlign: "center", cursor: "pointer" }}
              >
                Leave group
              </Text>
            </div>
          </div>
        </AddMembers>
      </Wrapper>
    </MainLayout>
  );
};

export default Participants;
