import { Amplify } from "aws-amplify";

import "@aws-amplify/ui-react/styles.css";
import {
  AuthUser,
  getCurrentUser,
  signInWithRedirect,
  signOut,
} from "aws-amplify/auth";
import { Hub } from "aws-amplify/utils";
import { useEffect, useState } from "react";

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
          domain: "flatini.auth.eu-west-2.amazoncognito.com/",
        },
      },
      userPoolId: "eu-west-2_U2HUbgIZK",
      userPoolClientId: "95rl77bq6dosrgerjfkgm12f5",
    },
  },
});

const SocialLogin = () => {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [error, setError] = useState<unknown>(null);
  const [customState, setCustomState] = useState<string | null>(null);

  useEffect(() => {
    const unsubscribe = Hub.listen("auth", ({ payload }) => {
      switch (payload.event) {
        case "signInWithRedirect":
          getUser();
          break;
        case "signInWithRedirect_failure":
          setError("An error has occurred during the OAuth flow.");
          break;
        case "customOAuthState":
          setCustomState(payload.data); // this is the customState provided on signInWithRedirect function
          break;
      }
    });

    getUser();

    return unsubscribe;
  }, []);

  const getUser = async (): Promise<void> => {
    try {
      const currentUser = await getCurrentUser();
      setUser(currentUser);
    } catch (error) {
      console.error(error);
      console.log("Not signed in");
    }
  };
  console.error("error", { error });
  return (
    <div style={{ display: "flex", flexDirection: "column" }}>
      <button
        onClick={() =>
          signInWithRedirect({
            customState:
              "some state that was past during sign in, eg redirect url",
          })
        }
      >
        Open Hosted UI
      </button>
      <button
        onClick={() =>
          signInWithRedirect({
            provider: "Google",
          })
        }
      >
        Open Google
      </button>
      {user && <button onClick={() => signOut()}>Sign Out</button>}
      <div>Authenticated User: {user ? user.username : "anonymous"}</div>
      <div>Custom State: {customState}</div>
    </div>
  );
};

export default function App() {
  return <SocialLogin />;
}
