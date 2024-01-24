// This file is part of cedge-library

import "styled-components";

declare module "styled-components" {
  export interface DefaultTheme {
    colors: {
      primary: string;
      secondary: string;
      background: string;
      text: string;
    };
    fonts: {
      family: {
        primary: string;
      };
      types: {
        small: {
          lineHeight: string;
          fontWeight: string;
          size: string;
        };
        paragraph: {
          lineHeight: string;
          fontWeight: string;
          size: string;
        };
        title: {
          lineHeight: string;
          fontWeight: string;
          size: string;
        };
      };
    };
  }
}
