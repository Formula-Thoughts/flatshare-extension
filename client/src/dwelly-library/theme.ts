import { DefaultTheme } from "styled-components";

const theme: DefaultTheme = {
  colors: {
    primary: "#EEBA00",
    secondary: "#AF496E",
    background: "#0B0708",
    text: "#ffffff",
  },
  fonts: {
    family: {
      primary: "Gabarito, sans-serif",
    },
    types: {
      small: {
        lineHeight: "1.6rem",
        fontWeight: "normal",
        size: "0.8rem",
      },
      paragraph: {
        lineHeight: "1.6rem",
        fontWeight: "normal",
        size: "1.3rem",
      },
      title: {
        lineHeight: "1.6rem",
        fontWeight: "bold",
        size: "1.7rem",
      },
    },
  },
};

export default theme;
