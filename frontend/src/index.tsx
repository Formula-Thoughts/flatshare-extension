import { Authenticator } from "@aws-amplify/ui-react";
import { Amplify } from "aws-amplify";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { ThemeProvider } from "styled-components";
import App from "./App";
import "./index.css";
import { FlatiniProvider, theme } from "flatini-fe-library";

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
  <Authenticator.Provider>
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        <FlatiniProvider theme={theme}>
          <App />
        </FlatiniProvider>
      </ThemeProvider>
    </BrowserRouter>
  </Authenticator.Provider>
);
