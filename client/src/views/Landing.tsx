import React from "react";
import Text, { TextTypes } from "../dwelly-library/components/Text";
import MainLayout from "../layouts/MainLayout";
import { styled, useTheme } from "styled-components";

const Wrapper = styled.div`
  border: 1px solid red;
  height: 100%;
  display: flex;
  flex-direction: column;
`;

const Block = styled.div`
  flex: 1;
  border: 1px solid green;
`;

const Landing = () => {
  const theme = useTheme();

  return (
    <MainLayout>
      <Wrapper>
        <Block>
          <Text type={TextTypes.title}>
            Create a group or join an existing one.
          </Text>
          <Text type={TextTypes.paragraph}>
            Create a group with your flatmates and start sharing links to find
            your next flat.
          </Text>
        </Block>
        <Block>
          <Text type={TextTypes.small} style={{ color: theme.colors.primary }}>
            How do I join an existing group?
          </Text>
          <Text type={TextTypes.paragraph}>
            Ask the group leader to invite you and you will be able to join from
            here.
          </Text>
        </Block>
      </Wrapper>
    </MainLayout>
  );
};

export default Landing;
