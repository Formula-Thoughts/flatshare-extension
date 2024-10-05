import React from "react";
import styled, { useTheme } from "styled-components";
import { useProvider } from "../context/AppProvider";
import { Button, Logo, Text, TextTypes } from "flatini-fe-library";
import { useNavigate } from "react-router-dom";

const Wrapper = styled.div`
  position: fixed;
  height: 100%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  gap: 1rem;
`;

const Content = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const CreateGroup = () => {
  const theme = useTheme();
  const { createGroup } = useProvider();
  const navigate = useNavigate();

  return (
    <Wrapper>
      <Content>
        <Logo style={{ width: "13rem" }} />
        <Text type={TextTypes.title}>
          Create a group or join an existing one.
        </Text>
        <Text type={TextTypes.paragraph}>
          Create a group with your flatmates and start sharing links to find
          your next flat.
        </Text>
        <Text style={{ color: theme.colors.primary }} type={TextTypes.small}>
          How to join an existing group?
        </Text>
        <Text type={TextTypes.paragraph}>
          Ask the group leader to invite you and you will be able to join from
          here.
        </Text>
        <div
          style={{
            width: "100%",
            display: "flex",
            flexDirection: "column",
            gap: "0.5rem",
          }}
        >
          <Button
            style={{ width: "100%" }}
            onClick={createGroup}
            label="Create group"
          />
          <Button
            style={{ width: "100%", background: "transparent", color: "white" }}
            onClick={() => navigate("/JoinGroup")}
            label="Join existing group"
          />
        </div>
      </Content>
    </Wrapper>
  );
};

export default CreateGroup;
