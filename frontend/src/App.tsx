import { Button, View, useAuthenticator } from "@aws-amplify/ui-react";
import "@aws-amplify/ui-react/styles.css";
import { Amplify } from "aws-amplify";

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

export default function App() {
  // const components = {
  //   SignIn: {
  //     Footer() {
  //       const { toForgotPassword } = useAuthenticator();
  //       return (
  //         <View textAlign="center">
  //           <Button fontWeight="normal" onClick={toForgotPassword} size="small">
  //             Forgot Password???
  //           </Button>
  //         </View>
  //       );
  //     },
  //   },
  // };
  const { user, toSignIn } = useAuthenticator((context) => [context.user]);
  console.log(`user ${user}\ntoSignIn ${toSignIn}`);
  return (
    <div>
      Here{user?.username}
      <button onClick={toSignIn}>Sign In</button>
    </div>
  );
}
