import { Amplify } from "aws-amplify";

export const isLocalhost = Boolean(
  window.location.hostname === "localhost" ||
    // [::1] is the IPv6 localhost address.
    window.location.hostname === "[::1]" ||
    // 127.0.0.1/8 is considered localhost for IPv4.
    window.location.hostname.match(
      /^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/
    )
);

function configureRedirects(awsExports: any) {
  // Assuming you have two redirect URIs, and the first is for hosted and second is for localhost
  const [localRedirectSignIn, productionRedirectSignIn] =
    awsExports.oauth.redirectSignIn.split(",");

  const [localRedirectSignOut, productionRedirectSignOut] =
    awsExports.oauth.redirectSignOut.split(",");

  const updatedAwsConfig = {
    ...awsExports,
    oauth: {
      ...awsExports.oauth,
      redirectSignIn: isLocalhost
        ? localRedirectSignIn
        : productionRedirectSignIn,
      redirectSignOut: isLocalhost
        ? localRedirectSignOut
        : productionRedirectSignOut,
    },
  };
  return updatedAwsConfig;
}

const aws = {
  region: "eu-west-2",
  userPoolId: "eu-west-2_U2HUbgIZK",
  userPoolWebClientId: "95rl77bq6dosrgerjfkgm12f5",
  mandatorySignIn: true,
  oauth: {
    domain: "flatini.auth.eu-west-2.amazoncognito.com/",
    scope: ["email", "openid", "profile"],
    redirectSignIn: "https://localhost:3000",
    redirectSignOut: "https://localhost:3000",
    responseType: "code",
  },
};

export const config = configureRedirects(aws);

Amplify.configure({
  Auth: config,
});
