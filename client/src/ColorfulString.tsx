import React from "react";
import styled from "styled-components";

interface ColorfulStringProps {
  text?: string;
}

const StyledSpan = styled.span<{ $color: string; $gap: boolean }>`
  color: ${(props) => props.$color};
  font-size: 34px;
  margin-right: ${(props) =>
    props.$gap
      ? "5px"
      : "0"}; // add a margin-right style for every 4th character
`;

const ColorfulString: React.FC<ColorfulStringProps> = ({ text = "" }) => {
  // Function to determine whether a character is a letter
  const isLetter = (char: string) => /^[a-zA-Z]$/.test(char);

  // Function to determine whether a character is a digit
  const isDigit = (char: string) => /^[0-9]$/.test(char);

  // Function to render each character with the appropriate color
  const renderColoredCharacter = (char: string, index: number) => {
    const gap = (index + 1) % 4 === 0 && index !== 0; // check if this is the 4th character in a group
    if (isLetter(char)) {
      return (
        <StyledSpan key={index} $color="white" $gap={gap}>
          {char}
        </StyledSpan>
      );
    } else if (isDigit(char)) {
      return (
        <StyledSpan key={index} $color="lightgrey" $gap={gap}>
          {char}
        </StyledSpan>
      );
    } else {
      return <span key={index}>{char}</span>;
    }
  };

  // Split the text into an array of characters and render them
  const characters = text.split("");
  const coloredText = characters.map((char, index) =>
    renderColoredCharacter(char, index)
  );

  return <div>{coloredText}</div>;
};

export default ColorfulString;
