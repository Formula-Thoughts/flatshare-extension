import { Amplify } from "aws-amplify";

import { Authenticator } from "@aws-amplify/ui-react";
import "@aws-amplify/ui-react/styles.css";

Amplify.configure({
  Auth: {
    Cognito: {
      loginWith: {
        oauth: {
          scopes: ["email", "openid", "profile"],
          redirectSignIn: [
            "https://localhost:3000/",
            "https://www.example.com/",
          ],
          redirectSignOut: [
            "https://localhost:3000/",
            "https://www.example.com/",
          ],
          responseType: "code",
          domain: "flatini.auth.eu-west-2.amazoncognito.com/",
        },
      },
      userPoolId: "eu-west-2_U2HUbgIZK",
      userPoolClientId: "95rl77bq6dosrgerjfkgm12f5D",
    },
  },
});

export default function App() {
  return (
    <Authenticator socialProviders={["google"]}>
      {({ signOut, user }) => (
        <main>
          <h1>Hello {user?.username}</h1>
          <button onClick={signOut}>Sign out</button>
        </main>
      )}
    </Authenticator>
  );
}
