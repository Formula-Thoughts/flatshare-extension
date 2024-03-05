import {
  AuthUser,
  getCurrentUser,
  signInWithRedirect,
} from "@aws-amplify/auth";
import { Hub } from "aws-amplify/utils";
import axios, { AxiosResponse } from "axios";
import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const Invite = (props: any) => {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const codeFromParam = searchParams.get("code");

  const [code, setCode] = useState(codeFromParam || "");

  const joinGroupFromInvite = async () => {
    // Gets access token from storage - I don't like this but it's good for now
    const getAccessToken = (): string => {
      function getObjectByKeyPart(keyPart: string, obj: any): any {
        for (const [key, value] of Object.entries(obj)) {
          if (key.includes(keyPart)) {
            return value;
          }
        }

        return null;
      }

      return getObjectByKeyPart(
        "accessToken",
        JSON.parse(JSON.stringify(localStorage))
      );
    };

    // Adds token to call
    const config = {
      headers: {
        Authorization: `Bearer ${getAccessToken()}`,
      },
    };

    const res = (await axios.post(
      `/participants?code=${code}`,
      {},
      config
    )) as AxiosResponse;
    // return res.data;
    console.log("res", res);
  };

  return (
    <div>
      <p>{JSON.stringify(props.user)}</p>
      <p>{code}</p>
      <h2>Invite Page</h2>
      <input
        onChange={(e) => setCode(e.target.value)}
        defaultValue={codeFromParam || ""}
      />
      <button onClick={async () => await joinGroupFromInvite()}>
        Click here to join group
      </button>
    </div>
  );
};

export default Invite;
