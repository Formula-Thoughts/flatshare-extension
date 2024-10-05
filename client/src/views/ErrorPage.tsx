import { Button, Logo, Text, TextTypes } from "flatini-fe-library";
import React from "react";
import styled from "styled-components";

const Wrapper = styled.div`
  position: fixed;
  height: 100%;
  width: 100%;
  overflow: scroll;
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */

  &::-webkit-scrollbar {
    display: none;
  }
`;

const Content = styled.div`
  padding: 1rem;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  background: #171113;
  gap: 1.5rem;
  text-align: center;
`;

const Issue = styled.div`
  padding: 0.8rem;
  line-height: 1.5rem;
  background-color: #4b4b4b;
  border-radius: 0.5rem;
  font-family: "Courier New", Courier, monospace;
`;

type Props = {
  data: string | boolean;
};

const ErrorPage = (props: Props) => {
  return (
    <Wrapper>
      <Content>
        <Logo style={{ width: "10rem" }} />
        <Text type={TextTypes.title}>Oh no! There is a problem.</Text>{" "}
        <Text type={TextTypes.small}>
          Try reloading the extension, signing out and signing back in or
          reinstall the extension.
        </Text>
        <Issue>
          {typeof props.data === "string" ? props.data : "Unknown Error"}
        </Issue>
        <Button
          onClick={() => window.location.reload()}
          label="Reload Flatini"
        />
      </Content>
    </Wrapper>
  );
};

export default ErrorPage;
