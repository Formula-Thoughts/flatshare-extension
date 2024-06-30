import React from "react";
import styled from "styled-components";

const Wrapper = styled.div``;

const MainLayout = (props: { children: React.ReactNode }) => {
  return <Wrapper>{props.children}</Wrapper>;
};

export default MainLayout;
