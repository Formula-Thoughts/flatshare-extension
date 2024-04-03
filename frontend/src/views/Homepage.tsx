import { signInWithRedirect, signOut } from "@aws-amplify/auth";
import { Link } from "react-router-dom";
import Logo from "../flatini-library/components/Logo";
import Text, { TextTypes } from "../flatini-library/components/Text";
import styled, { useTheme } from "styled-components";
import Button from "../flatini-library/components/Button";

const Wrapper = styled.div`
  max-width: 25rem;
`;

const Content = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const Homepage = (props: any) => {
  const theme = useTheme();
  return (
    <Wrapper>
      <Logo style={{ width: "15rem" }} />
      <Content>
        <Text style={{ color: theme.colors.primary }} type={TextTypes.small}>
          Find together the perfect place.
        </Text>

        {props.user ? (
          <>
            <Text type={TextTypes.paragraph}>
              Click here to <Link to="/invite">join a group</Link>
            </Text>
            <Button
              style={{ cursor: "pointer" }}
              label="Sign out"
              onClick={() => signOut()}
            />
          </>
        ) : (
          <>
            <Text type={TextTypes.paragraph}>
              Click on the following button to authenticate with Google and use
              Flatini.
            </Text>
            <Button
              label="Sign In with Google"
              style={{ cursor: "pointer" }}
              onClick={() =>
                signInWithRedirect({
                  provider: "Google",
                  customState: props.code,
                })
              }
            />
          </>
        )}
      </Content>
    </Wrapper>
  );
};

export default Homepage;
