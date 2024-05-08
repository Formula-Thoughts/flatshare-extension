import React from "react";
import styled from "styled-components";

export enum TextTypes {
  paragraph = "paragraph",
  title = "title",
  small = "small",
}

const Small = styled.span`
  font-size: ${(props) => props.theme.fonts.types.small.size};
  font-weight: ${(props) => props.theme.fonts.types.small.fontWeight};
  line-height: ${(props) => props.theme.fonts.types.small.lineHeight};
`;

const Paragraph = styled.p`
  font-size: ${(props) => props.theme.fonts.types.paragraph.size};
  font-weight: ${(props) => props.theme.fonts.types.paragraph.fontWeight};
  line-height: ${(props) => props.theme.fonts.types.paragraph.lineHeight};
`;

const Title = styled.h1`
  font-size: ${(props) => props.theme.fonts.types.title.size};
  font-weight: ${(props) => props.theme.fonts.types.title.fontWeight};
  line-height: ${(props) => props.theme.fonts.types.title.lineHeight};
`;

type Props = {
  type: TextTypes;
  children: React.ReactNode;
  style?: React.CSSProperties;
  id?: string;
  className?: string;
};

const Text = (props: Props) => {
  return (
    <>
      {props.type === TextTypes.small && (
        <Small id={props.id} className={props.className} style={props.style}>
          {props.children}
        </Small>
      )}
      {props.type === TextTypes.paragraph && (
        <Paragraph
          id={props.id}
          className={props.className}
          style={props.style}
        >
          {props.children}
        </Paragraph>
      )}
      {props.type === TextTypes.title && (
        <Title id={props.id} className={props.className} style={props.style}>
          {props.children}
        </Title>
      )}
    </>
  );
};

export default Text;
