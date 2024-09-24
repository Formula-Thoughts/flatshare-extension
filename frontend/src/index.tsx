import { Authenticator } from "@aws-amplify/ui-react";
import { Amplify } from "aws-amplify";
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { ThemeProvider } from "styled-components";
import App from "./App";
import theme from "./flatini-library/theme";
import "./index.css";
import reportWebVitals from "./reportWebVitals";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);

Amplify.configure({
  Auth: {
    Cognito: {
      loginWith: {
        oauth: {
          scopes: ["email", "openid", "profile"],
          redirectSignIn: [
            "https://localhost:3000",
            "https://flatini.formulathoughts.com",
          ],
          redirectSignOut: [
            "https://localhost:3000",
            "https://flatini.formulathoughts.com",
          ],
          responseType: "code",
          domain: (process.env.NODE_ENV === "production"
            ? process.env.REACT_APP_COGNITO_DOMAIN_PROD
            : process.env.REACT_APP_COGNITO_DOMAIN_STAGING) as string,
        },
      },
      userPoolId: (process.env.NODE_ENV === "production"
        ? process.env.REACT_APP_COGNITO_POOL_ID_PROD
        : process.env.REACT_APP_COGNITO_POOL_ID_STAGING) as string,
      userPoolClientId: (process.env.NODE_ENV === "production"
        ? process.env.REACT_APP_COGNITO_CLIENT_ID_PROD
        : process.env.REACT_APP_COGNITO_CLIENT_ID_STAGING) as string,
    },
  },
});

root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <Authenticator.Provider>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </Authenticator.Provider>
    </ThemeProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
