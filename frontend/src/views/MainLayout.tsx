import React from "react";
import styled from "styled-components";

const Wrapper = styled.div`
  position: fixed;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
`;

const MainLayout = (props: { children: React.ReactNode }) => {
  return <Wrapper>{props.children}</Wrapper>;
};

export default MainLayout;
