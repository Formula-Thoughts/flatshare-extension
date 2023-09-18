import { useState } from "react";
import styled from "styled-components";
import Button from "./Button";

const Wrapper = styled.div`
  position: fixed;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 50px 20px;
`;

const Hashtag = styled.span`
  font-size: 11px;
  color: white;
`;

const CopyCodeWrapper = styled.div`
  flex: 8;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
`;

const GroupCode = styled.span`
  font-size: 45px;
  color: white;
`;

const LinkCopiedText = styled.div`
  background-color: #4b2798;
  color: white;
  padding: 10px 30px;
  border-radius: 5px;
  font-size: 20px;
`;

const CreateGroup = () => {
  const [id, setId] = useState(generateRandomId());
  const [copiedToClipboard, setCopiedToClipboard] = useState(false);

  function generateRandomId(): string {
    let randomId = "";
    for (let i = 0; i < 12; i++) {
      randomId += Math.floor(Math.random() * 10).toString();
    }
    return randomId;
  }

  return (
    <Wrapper>
      <p style={{ flex: 1 }}>
        You are creating a new group. Share this code with your flatmates so
        they can join the group.
      </p>

      <CopyCodeWrapper>
        <div>
          <Hashtag>#</Hashtag>
          <GroupCode className="secondary">{id}</GroupCode>
        </div>
        {copiedToClipboard ? (
          <LinkCopiedText style={{ margin: "20px 0" }}>
            <span className="secondary">Code copied to clipboard!</span>
          </LinkCopiedText>
        ) : null}
        <Button
          onClick={() => setCopiedToClipboard(true)}
          style={{ padding: 15, marginTop: 10 }}
        >
          {!copiedToClipboard ? (
            <img
              style={{ width: 30 }}
              src="https://cdns.iconmonstr.com/wp-content/releases/preview/7.8.0/240/iconmonstr-cut-lined.png"
            />
          ) : (
            <img
              style={{ width: 30 }}
              src="https://cdns.iconmonstr.com/wp-content/releases/preview/2012/240/iconmonstr-check-mark-4.png"
            />
          )}
        </Button>
      </CopyCodeWrapper>
      <div style={{ flex: 1 }}>
        <Button>Create new group</Button>
      </div>
    </Wrapper>
  );
};

export default CreateGroup;
