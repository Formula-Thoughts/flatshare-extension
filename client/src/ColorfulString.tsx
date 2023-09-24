import React from "react";

interface ColorfulStringProps {
  text: string;
}

const ColorfulString: React.FC<ColorfulStringProps> = ({ text }) => {
  // Function to determine whether a character is a letter
  const isLetter = (char: string) => /^[a-zA-Z]$/.test(char);

  // Function to determine whether a character is a digit
  const isDigit = (char: string) => /^[0-9]$/.test(char);

  // Function to render each character with the appropriate color
  const renderColoredCharacter = (char: string, index: number) => {
    if (isLetter(char)) {
      return (
        <span key={index} style={{ color: "black" }}>
          {char}
        </span>
      );
    } else if (isDigit(char)) {
      return (
        <span key={index} style={{ color: "blue" }}>
          {char}
        </span>
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
