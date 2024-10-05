import { Button, InputText, Text, TextTypes } from "flatini-fe-library";
import React, { useState } from "react";
import styled from "styled-components";
import { _joinExistingGroup } from "../utils/resources";
import { useProvider } from "../context/AppProvider";
import { AxiosError } from "axios";
import { FaArrowLeft } from "react-icons/fa";
import { useNavigate } from "react-router-dom";

const Wrapper = styled.div`
  position: fixed;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  text-align: left;
  padding: 50px 20px;
  gap: 2rem;
  background: #0b0708;
  color: white;
`;

const ErrorWrapper = styled.div`
  background: #e47020;
  padding: 1rem;
  border-radius: 0.5rem;
`;

const JoinGroup = () => {
  const [code, setCode] = useState<string | null>(null);
  const [error, setError] = useState<string | boolean>(false);
  const { userAuthToken } = useProvider();
  const navigate = useNavigate();

  return (
    <Wrapper>
      <div
        onClick={() => navigate("/")}
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: "0.5rem",
          cursor: "pointer",
          opacity: 0.7,
        }}
      >
        <FaArrowLeft />
        <Text type={TextTypes.paragraph}>Back</Text>
      </div>
      <Text type={TextTypes.title}>Join existing group</Text>
      <Text type={TextTypes.paragraph}>
        Enter the code’s group to join it. Ask a member of the group to send you
        an invite code.
      </Text>
      <InputText
        name="text"
        placeholder="Enter the group code..."
        style={{ width: "100%" }}
        onChange={(value) => {
          setCode(value);
        }}
      />
      <Button
        style={{ width: "100%" }}
        onClick={async () => {
          try {
            await _joinExistingGroup(userAuthToken, code as string);
            window.location.reload();
          } catch (err) {
            if ((err as AxiosError)?.response?.status === 404) {
              setError(
                "That group doesn't exist. Please try again with a valid code."
              );
            }

            if ((err as AxiosError)?.response?.status === 500) {
              setError(
                "There's been a server error. Please make sure you're entering a valid group code."
              );
            }

            if ((err as any)?.response?.status === 400) {
              setError(
                "You are already in that group! Reload the extension and try again."
              );
            }
          }
        }}
        label="Join group"
      />
      {error ? (
        <ErrorWrapper>
          <Text type={TextTypes.paragraph}>{error}</Text>
        </ErrorWrapper>
      ) : null}
    </Wrapper>
  );
};

export default JoinGroup;
