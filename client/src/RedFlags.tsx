import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import ColorLayout from "./layouts/ColorLayout";
import styled from "styled-components";
import { useProvider } from "./context/AppProvider";
import { FaArrowLeft, FaPlus } from "react-icons/fa";
import ReactTimeAgo from "react-time-ago";
import { _voteRedFlag } from "./utils/resources";
import { Button, Text, TextTypes } from "flatini-fe-library";

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
  background: transparent;
  padding: 0.3rem;
  color: white;
  border-radius: 1rem;
  border: 3px solid white;
  cursor: pointer;

  &.user-has-voted {
    background: white;
    span {
      color: black !important;
    }
  }
`;

const RedFlags = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { activeFlatData } = useProvider();

  const [redFlags] = useState<RedFlagType[]>(activeFlatData.redFlags);

  const sortByVotes = (data: any[], ascending: boolean = false) => {
    return data.sort((a, b) => {
      return ascending ? a.votes - b.votes : b.votes - a.votes;
    });
  };

  console.log("sortByVotes", sortByVotes(redFlags));

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
          {sortByVotes(redFlags).map((redFlag) => {
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
  const [votedByMe, setVotedByMe] = useState(props.votedByMe);
  const [votes, setVotes] = useState(props.votes);

  return (
    <Wrapper>
      <Text type={TextTypes.small}>{props.body}</Text>
      <Footer>
        <div>
          <HelpfulButton
            onClick={async () => {
              await _voteRedFlag(
                userAuthToken,
                props.id,
                props.propertyUrl,
                votedByMe
              );
              setVotedByMe(!votedByMe);

              if (votedByMe) {
                setVotes(votes - 1);
              } else {
                setVotes(votes + 1);
              }
            }}
            className={`${votedByMe ? "user-has-voted" : null}`}
          >
            <Text type={TextTypes.small} style={{ fontWeight: "bold" }}>
              Helpful
            </Text>
          </HelpfulButton>
        </div>
        <div style={{ flex: 1, opacity: 0.7 }}>
          <Text type={TextTypes.small}>{votes} users agree</Text>
        </div>
        <div style={{ flex: 1, opacity: 0.7 }}>
          <ReactTimeAgo date={props.date} locale="en" />
        </div>
      </Footer>
    </Wrapper>
  );
};

export default RedFlags;
