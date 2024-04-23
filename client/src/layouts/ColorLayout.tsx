import React, { PropsWithChildren } from "react";
import styled from "styled-components";

const Wrapper = styled.div`
  position: fixed;
  height: 100%;
  width: 100%;
  overflow: scroll;
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
  background-color: #af496e !important;

  &::-webkit-scrollbar {
    display: none;
  }
`;

const Content = styled.div`
  padding: 1rem;
  height: 100%;
`;

type Props = {
  children: React.ReactNode;
};

const ColorLayout = (props: Props) => {
  return (
    <Wrapper>
      <Content>{props.children}</Content>
    </Wrapper>
  );
};

export default ColorLayout;
