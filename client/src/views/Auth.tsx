import React from "react";
import { flatiniAuthWebsite } from "../utils/constants";
import styled, { useTheme } from "styled-components";
import Button from "../flatini-library/components/Button";
import Text, { TextTypes } from "../flatini-library/components/Text";
import MainLayout from "../layouts/MainLayout";
import Logo from "../flatini-library/components/Logo";

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
          <a href={flatiniAuthWebsite} target="_blank">
            <Button
              style={{ maxWidth: "100%" }}
              onClick={async () => {}}
              label="Enter flatini"
            />
          </a>
        </div>
      </Content>
    </Wrapper>
  );
};

export default Auth;
