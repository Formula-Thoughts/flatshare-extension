import axios, { AxiosResponse } from "axios";
import { useState } from "react";

const Invite = (props: any) => {
  const [code, setCode] = useState(props.code || "");

  const [userAlreadyInGroupError, setUserAlreadyInGroupError] = useState(false);
  const [userHasJoinedGroup, setUserHasJoinedGroup] = useState(false);

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

    try {
      const res = (await axios.post(
        `https://pmer135n4j.execute-api.eu-west-2.amazonaws.com/participants?code=${code}`,
        {},
        config
      )) as AxiosResponse;

      if (res.status === 200) {
        setUserHasJoinedGroup(true);
      }
    } catch (err) {
      if ((err as any)?.response?.status === 400) {
        setUserAlreadyInGroupError(true);
      }
    }
  };

  return (
    <div>
      <p>{JSON.stringify(props.user)}</p>
      <p>{code}</p>
      <h2>Invite Page</h2>
      <div>
        <input
          onChange={(e) => setCode(e.target.value)}
          defaultValue={props.code || ""}
        />
        <button onClick={async () => await joinGroupFromInvite()}>
          Click here to join group
        </button>
      </div>
      {userAlreadyInGroupError ? (
        <p>sorry, the user is already in this group</p>
      ) : null}
      {userHasJoinedGroup ? (
        <p>You've joined the group. Open or reload your Flatini extension.</p>
      ) : null}
    </div>
  );
};

export default Invite;
