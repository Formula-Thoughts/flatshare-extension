import axios, { AxiosResponse } from "axios";
import { useState } from "react";
import styled, { useTheme } from "styled-components";
import Text, { TextTypes } from "../flatini-library/components/Text";
import InputText from "../flatini-library/components/InputText";
import Button from "../flatini-library/components/Button";

const Wrapper = styled.div`
  position: fixed;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
`;

const Content = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const Invite = (props: any) => {
  const theme = useTheme();
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
    <Wrapper>
      <Content>
        <Text type={TextTypes.title}>Join a group</Text>
        <Text type={TextTypes.paragraph}>
          Enter the group code that has been shared with you.
        </Text>
        <InputText
          name="code"
          placeholder="Enter a code..."
          onChange={(value: any) => setCode(value)}
          defaultValue={props.code || ""}
        />
        <div>
          <Button
            style={{ cursor: "pointer" }}
            onClick={async () => await joinGroupFromInvite()}
            label="Click here to join a group"
          />
        </div>
        {userAlreadyInGroupError ? (
          <Text
            style={{ color: theme.colors.primary }}
            type={TextTypes.paragraph}
          >
            <p>Sorry, this user is already in this group.</p>
          </Text>
        ) : null}
        {userHasJoinedGroup ? (
          <Text
            style={{ color: theme.colors.primary }}
            type={TextTypes.paragraph}
          >
            You've joined the group. Open or reload your Flatini extension.
          </Text>
        ) : null}
      </Content>
    </Wrapper>
  );
};

export default Invite;
