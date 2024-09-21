import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import ColorLayout from "./layouts/ColorLayout";
import Text, { TextTypes } from "./flatini-library/components/Text";
import styled from "styled-components";
import Button from "./flatini-library/components/Button";
import { useProvider } from "./context/AppProvider";
import { FaArrowLeft, FaPlus } from "react-icons/fa";
import TimeAgo from "javascript-time-ago";
import ReactTimeAgo from "react-time-ago";
import { _voteRedFlag } from "./utils/resources";
import MainLayout from "./layouts/MainLayout";

type Data = {
  flatUrl: string;
  flatName: string;
  redFlags: RedFlagType[];
};

type RedFlagType = {
  id: string;
  body: string;
  propertyUrl: string;
  votes: number;
  votedByMe: boolean;
  date: Date;
};

const Header = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  width: 100%;
`;

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const Footer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: right;
`;

const HelpfulButton = styled.div`
  background: white;
  padding: 0.3rem;
  color: black;
  border-radius: 1rem;

  &.user-has-voted {
    background: transparent;
    color: white;
  }
`;

const RedFlags = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { activeFlatData } = useProvider();

  const [redFlags] = useState<RedFlagType[]>(activeFlatData.redFlags);

  console.log("check red flags", redFlags);

  return (
    <ColorLayout>
      <div
        style={{
          height: "100%",
          display: "flex",
          alignItems: "start",
          justifyContent: "start",
          flexDirection: "column",
          gap: "2rem",
        }}
      >
        <Header>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              gap: "1rem",
              width: "100%",
            }}
          >
            <Button onClick={() => navigate("/FlatView")}>
              <FaArrowLeft />
            </Button>
            <Text type={TextTypes.paragraph}>
              🚩{redFlags.length} red flag(s)
            </Text>
            <div>
              <Button
                style={{ background: "rgb(209 124 154)", color: "white" }}
                onClick={() => navigate("/AddRedFlag")}
              >
                <FaPlus />
              </Button>
            </div>
          </div>
        </Header>
        <div
          style={{
            display: "flex",
            gap: "3rem",
            flexDirection: "column",
            width: "100%",
          }}
        >
          {redFlags.map((redFlag) => {
            return <RedFlag {...redFlag} />;
          })}
        </div>
      </div>
    </ColorLayout>
  );
};

const RedFlag = (props: RedFlagType) => {
  // const timeAgo = new TimeAgo("en-US");
  const { userAuthToken } = useProvider();

  return (
    <Wrapper>
      <Text type={TextTypes.small}>{props.body}</Text>
      <Footer>
        <div>
          <HelpfulButton
            onClick={async () =>
              await _voteRedFlag(
                userAuthToken,
                props.id,
                props.propertyUrl,
                props.votedByMe
              )
            }
            className={`${props.votedByMe ? "user-has-voted" : null}`}
          >
            <Text type={TextTypes.small} style={{ fontWeight: "bold" }}>
              Helpful
            </Text>
          </HelpfulButton>
        </div>
        <div style={{ flex: 1, opacity: 0.7 }}>
          <Text type={TextTypes.small}>{props.votes} users agree</Text>
        </div>
        <div style={{ flex: 1, opacity: 0.7 }}>
          <ReactTimeAgo date={props.date} locale="en" />
        </div>
      </Footer>
    </Wrapper>
  );
};

export default RedFlags;
