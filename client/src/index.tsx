import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./sidepanel";
import { MemoryRouter } from "react-router-dom";
import AppProvider from "./context/AppProvider";
import { ThemeProvider } from "styled-components";

import TimeAgo from "javascript-time-ago";

import en from "javascript-time-ago/locale/en";
import GlobalStyle from "./utils/globalStyle";
import { FlatiniProvider, theme } from "flatini-fe-library";

TimeAgo.addDefaultLocale(en);

const root = document.createElement("div");
root.className = "container";
document.body.appendChild(root);
const rootDiv = ReactDOM.createRoot(root);
rootDiv.render(
  <MemoryRouter>
    <AppProvider>
      <FlatiniProvider theme={theme}>
        <ThemeProvider theme={theme as any}>
          <GlobalStyle />
          <App />
        </ThemeProvider>
      </FlatiniProvider>
    </AppProvider>
  </MemoryRouter>
);
