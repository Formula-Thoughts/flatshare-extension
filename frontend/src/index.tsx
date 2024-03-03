import { Authenticator } from "@aws-amplify/ui-react";
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";
import reportWebVitals from "./reportWebVitals";
import { Amplify } from "aws-amplify";

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
            "https://localhost:3000/",
            "https://flatini.formulathoughts.com",
          ],
          responseType: "code",
          domain: "flatini.auth.eu-west-2.amazoncognito.com/",
        },
      },
      userPoolId: "eu-west-2_U2HUbgIZK",
      userPoolClientId: "95rl77bq6dosrgerjfkgm12f5",
    },
  },
});

root.render(
  <React.StrictMode>
    <Authenticator.Provider>
      <App />
    </Authenticator.Provider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
