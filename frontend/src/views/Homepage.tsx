import {
  AuthUser,
  getCurrentUser,
  signInWithRedirect,
  signOut,
} from "@aws-amplify/auth";
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const Homepage = (props: any) => {
  return (
    <div>
      <h2>Home Page</h2>
      {props.user && (
        <>
          <p>Hello {props.user?.username}!</p>
          <div>
            Join a group: <Link to="/invite">join group</Link>
          </div>
          <button onClick={() => signOut()}>Sign Out</button>
        </>
      )}
      {!props.user && (
        <button
          style={{ width: 200 }}
          onClick={() =>
            signInWithRedirect({
              provider: "Google",
              customState:
                "some state that was past during sign in, eg redirect url",
            })
          }
        >
          Sign In with Google
        </button>
      )}
    </div>
  );
};

export default Homepage;
