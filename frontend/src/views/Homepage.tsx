import { signInWithRedirect, signOut } from "@aws-amplify/auth";
import { Link } from "react-router-dom";
import Logo from "../flatini-library/components/Logo";
import Text, { TextTypes } from "../flatini-library/components/Text";
import styled, { useTheme } from "styled-components";
import Button from "../flatini-library/components/Button";
import Image from "../flatini-library/components/Image";
import promoImg from "../promo.png";
import supportedSites from "../supported-sites.png";
import { device } from "../flatini-library/util/mediaQueries";

const Wrapper = styled.div`
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 4rem;
  max-width: 1200px;
  margin: auto;
`;

const NavBar = styled.div`
  display: flex;
`;

const Hero = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const Block = styled.div`
  display: flex;
  align-items: center;

  @media ${device.tablet} {
    flex-direction: column;

    .how-does-it-work {
      padding: 0.5rem !important;
    }
  }
`;

const Homepage = (props: any) => {
  const theme = useTheme();

  return (
    <Wrapper>
      <NavBar>
        <div style={{ flex: 1 }}>
          <Logo style={{ width: "10rem" }} />
        </div>

        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "1rem",
          }}
        >
          {props.user ? (
            <Text type={TextTypes.paragraph}>
              <Link to="/invite">join a group</Link>
            </Text>
          ) : null}
          <div
            style={{
              flex: 1,
              textAlign: "right",
            }}
          >
            {props.user ? (
              <Button
                style={{ cursor: "pointer" }}
                label="Sign out"
                onClick={() => signOut()}
              />
            ) : (
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  textAlign: "center",
                  maxWidth: "15rem",
                  gap: "0.5rem",
                }}
              >
                <Button
                  label="Enter Flatini"
                  style={{ cursor: "pointer" }}
                  onClick={() =>
                    signInWithRedirect({
                      provider: "Google",
                      customState: props.code,
                    })
                  }
                />
              </div>
            )}
          </div>
        </div>
      </NavBar>
      <Hero>
        <Text type={TextTypes.title}>
          Find your next flat to rent in London easier and faster with Flatini.
        </Text>
        <Text type={TextTypes.paragraph}>
          Looking for a flat is excruciatingly draining. We’re here to help you
          find your next flat.
        </Text>
        <a
          href="https://chromewebstore.google.com/detail/flatini/ndikjhgaonkjjgpjcnkdpddpjdkgpepo?hl=en&authuser=1&pli=1"
          target="_blank"
          rel="noreferrer"
        >
          <Button
            label="Add to chrome ⎯⎯ it's free"
            style={{ cursor: "pointer" }}
          />
        </a>
      </Hero>
      <Block>
        <div style={{ background: "#943759", flex: 1, padding: "2rem" }}>
          <Image src={promoImg} style={{ width: "100%" }} alt={"Promo image"} />
        </div>
        <div
          className="how-does-it-work"
          style={{
            flex: 1,
            padding: "2rem",
            display: "flex",
            flexDirection: "column",
            gap: "1rem",
          }}
        >
          <div>
            <Text
              style={{ color: theme.colors.primary }}
              type={TextTypes.small}
            >
              Download the extension and use.
            </Text>
            <Text type={TextTypes.title}> How does it work?</Text>
          </div>
          <ol
            style={{
              display: "flex",
              alignItems: "flex-start",
              flexDirection: "column",
              gap: "1.3rem",
            }}
          >
            <li>
              <Text type={TextTypes.paragraph}>
                Add Flatini’s chrome extension to your browser in 2 seconds, for
                free.
              </Text>
            </li>
            <li>
              <Text type={TextTypes.paragraph}>
                Create shared lists of flats as you browse through your
                favourites.
              </Text>
            </li>
            <li>
              <Text type={TextTypes.paragraph}>
                Access flat reviews from other users.Access flat reviews from
                other users.
              </Text>
            </li>
          </ol>
        </div>
      </Block>
      <Block>
        <div style={{ flex: 1 }}>
          <Text style={{ color: theme.colors.primary }} type={TextTypes.small}>
            Sites you can use Flatini in
          </Text>
          <Text type={TextTypes.title}>Supported portals</Text>
          <Text style={{ marginTop: "1rem" }} type={TextTypes.paragraph}>
            You can save flats from any of the biggest real estate sites in
            London
          </Text>
        </div>
        <div style={{ flex: 1, padding: "2rem" }}>
          <Image
            src={supportedSites}
            style={{ width: "100%" }}
            alt={"Promo image"}
          />
        </div>
      </Block>
    </Wrapper>
  );
};

export default Homepage;
