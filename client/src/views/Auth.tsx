import React from "react";
import { flatiniAuthWebsite } from "../utils/constants";
import styled, { useTheme } from "styled-components";
import { Button, Logo, Text, TextTypes } from "flatini-fe-library";

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

const Auth = () => {
  const theme = useTheme();
  return (
    <Wrapper>
      <Content>
        <Logo style={{ width: "13rem" }} />
        <Text style={{ color: theme.colors.primary }} type={TextTypes.small}>
          Find together the perfect place.
        </Text>
        <Text type={TextTypes.paragraph}>
          Flatini is an extension that allows you to save your favourite
          properties to a list, and invite your flatmates.
        </Text>
        <div>
          <a href={flatiniAuthWebsite} target="_blank" rel="noreferrer">
            <Button
              style={{ maxWidth: "100%" }}
              onClick={async () => {}}
              label="Go to Flatini's site"
            />
          </a>
          <div style={{ paddingTop: "1rem" }}>
            <Text style={{ opacity: 0.5 }} type={TextTypes.small}>
              Once you reach Flatini's site, click on "Enter Flatini" to log in
              and get you inside.
            </Text>
          </div>
        </div>
      </Content>
    </Wrapper>
  );
};

export default Auth;
