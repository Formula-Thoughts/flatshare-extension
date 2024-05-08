import React from "react";
import styled from "styled-components";
import Header from "../components/Header";

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
  background: #171113;
`;

type Props = {
  children: React.ReactNode;
};

const MainLayout = (props: Props) => {
  return (
    <Wrapper>
      <Header />
      <Content>{props.children}</Content>
    </Wrapper>
  );
};

export default MainLayout;
