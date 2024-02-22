import React, { useContext, useEffect, useState } from "react";
import logo from "./logo.svg";
import "./App.css";
import { Auth } from "aws-amplify";
import { CognitoHostedUIIdentityProvider } from "@aws-amplify/auth";
import { useNavigate, useSearchParams } from "react-router-dom";

function App() {
  const [isAuthenticated, setAuthenticated] = useState(false);
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  const signIn = async () => {
    Auth.federatedSignIn({
      provider: CognitoHostedUIIdentityProvider.Google,
    });
  };

  useEffect(() => {
    const getToken = async () => {
      try {
        const res = await Auth.currentSession();
        let accessToken = res.getAccessToken();
        let jwt = accessToken.getJwtToken();
        //You can print them to see the full objects
        // console.log(`myAccessToken: ${JSON.stringify(accessToken)}`);
        // console.log(`myJwt: ${jwt}`);

        // navigate(`/?token=${jwt}`);
        setSearchParams({ flatiniToken: jwt });
        console.log("setting params");
        setAuthenticated(true);
      } catch (err) {
        console.log(err);
        if (searchParams.has("flatiniToken")) {
          searchParams.delete("flatiniToken");
          setSearchParams(searchParams);
        }
      }
    };

    getToken();
  }, [searchParams, setSearchParams]);

  return (
    <div className="App">
      <p>is auth {JSON.stringify(isAuthenticated)}</p>
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <button onClick={signIn}>Sign In</button>
        <button onClick={() => Auth.signOut()}>Sign Out</button>
      </header>
    </div>
  );
}

export default App;
