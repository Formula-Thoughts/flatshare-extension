import { signInWithRedirect, signOut } from "@aws-amplify/auth";
import { Link } from "react-router-dom";
import styled, { useTheme } from "styled-components";
import promoImg from "../promo.png";
import promo2Img from "../promo-2.png";

import redFlagUp from "../red-flag-up.png";
import houseRight from "../house-right.png";

import supportedSites from "../supported-sites.png";

import xavierImg from "../images-people/1675698725213.jpg";
import aidanImg from "../images-people/1709241356504.jpg";
import domImg from "../images-people/1725373221246.jpg";
import {
  Logo,
  Text,
  device,
  TextTypes,
  Button,
  Image,
} from "flatini-fe-library";

const Wrapper = styled.div`
  flex-direction: column;
  gap: 4rem;
  margin: auto;

  @media ${device.tablet} {
    .branding-image {
      opacity: 0.1;
    }
  }

  @media ${device.tablet} {
    .text {
      line-height: 2rem;
    }
  }
`;

const NavBar = styled.div`
  display: flex;
  background-color: #1d1d1d;
  padding: 0 2rem;
  padding-top: 1rem;
`;

const Hero = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background-color: #1d1d1d;
  text-align: center;
  gap: 2rem;

  .hero-wrapper {
    @media ${device.tablet} {
      padding: 0 !important;
      padding-bottom: 2rem !important;
    }
  }
`;

const Block = styled.div`
  display: flex;
  align-items: center;
  gap: 2rem;

  @media ${device.tablet} {
    flex-direction: column;

    .how-does-it-work {
      padding: 0.5rem !important;
    }
    margin-bottom: 2rem;
  }
`;

const ContentLayout = styled.div`
  margin: 2rem;
`;

const People = styled.div`
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 3rem;
  background: #1d1d1d;
  padding: 4rem;

  @media ${device.tablet} {
    display: block;
    padding: 0;

    img {
      width: 100%;
    }
  }
`;

const Person = styled.div`
  @media ${device.tablet} {
    display: inline-block;
    margin: 1rem;
  }

  span {
    display: block;
    margin: 0.5rem 0;
  }

  h1 {
    max-width: 30px;
  }
`;

const Homepage = (props: any) => {
  const theme = useTheme();
  var isChrome = !!window.chrome;

  return (
    <Wrapper>
      <NavBar>
        <div style={{ flex: 1 }}>
          <Logo style={{ width: "10rem" }} />
        </div>

        {isChrome ? (
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
                <div style={{ display: "flex", gap: "1rem" }}>
                  <Button
                    id="openFlatiniSidebar"
                    label={"Open Flatini"}
                    style={{
                      cursor: "pointer",
                      background: theme.colors.primary,
                      color: "black",
                    }}
                  />
                  <Button
                    style={{ cursor: "pointer" }}
                    label="Sign out"
                    onClick={() => signOut()}
                  />
                </div>
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
                    id="openFlatiniSidebar"
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
        ) : (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              padding: "1rem",
              borderRadius: "0.5rem",
              background: "grey",
            }}
          >
            Flatini is only available in Chrome
          </div>
        )}
      </NavBar>
      <Hero>
        <ContentLayout>
          <div
            className="hero-wrapper"
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "2rem",
              padding: "6rem 1rem",
              maxWidth: "1000px",
              margin: "auto",
            }}
          >
            <Text
              type={TextTypes.paragraph}
              style={{ fontSize: "1.5rem", opacity: 0.5 }}
            >
              Looking to rent in London? Flatini is made for you.
            </Text>
            <div style={{ position: "relative" }}>
              <Image
                src={houseRight}
                className="branding-image"
                style={{
                  width: "5rem",
                  position: "absolute",
                  top: "-7rem",
                  left: "4rem",
                }}
                alt={"brand visual"}
              />
              <Text type={TextTypes.title} style={{ lineHeight: "2.5rem" }}>
                Manage lists of properties with your friends from any of the big
                real estate portals & see red flags left by users like you.
              </Text>

              <Image
                src={redFlagUp}
                className="branding-image"
                style={{
                  width: "5rem",
                  position: "absolute",
                  left: "5rem",
                  bottom: "-7rem",
                }}
                alt={"brand visual"}
              />
            </div>
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
          </div>
        </ContentLayout>
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
              Download the chrome extension and use right away.
            </Text>
            <Text type={TextTypes.title}>
              Manage properties you want to view easily.
            </Text>
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
                When looking for a property to rent with your friends, you deal
                with hundreds of different links from different providers.
              </Text>
            </li>
            <li>
              <Text type={TextTypes.paragraph}>
                You and your friends can manage them all through Flatini. No
                more WhatsApp lists.
              </Text>
            </li>
          </ol>
        </div>
      </Block>
      <Block>
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
              Download the chrome extension and use right away.
            </Text>
            <Text type={TextTypes.title}>
              Don’t waste time. Know what you’re going to view.
            </Text>
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
                We know the pain of going to a viewing that was too good to be
                true.
              </Text>
            </li>
            <li>
              <Text type={TextTypes.paragraph}>
                Read reviews (red flags) from other users before attending the
                viewing to make sure the place is what you’re looking for.
              </Text>
            </li>
          </ol>
        </div>
        <div style={{ background: "#353432", flex: 1, padding: "2rem" }}>
          <Image
            src={promo2Img}
            style={{ width: "100%" }}
            alt={"Promo image"}
          />
        </div>
      </Block>
      <Block
        style={{
          flex: 1,
          padding: "2rem",
          display: "flex",
          flexDirection: "row",
          gap: "1rem",
        }}
      >
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
      <ContentLayout>
        <Text style={{ marginBottom: "1rem" }} type={TextTypes.title}>
          Behind Flatini
        </Text>
        <div>
          <People>
            <Person>
              <Image
                src={aidanImg}
                style={{ width: "10rem" }}
                alt={"Promo image"}
              />
              <Text
                style={{ color: theme.colors.primary }}
                type={TextTypes.small}
              >
                Back-End & Devops
              </Text>
              <Text type={TextTypes.title}>Aidan Gannon</Text>
            </Person>
            <Person>
              <Image
                src={xavierImg}
                style={{ width: "10rem" }}
                alt={"Promo image"}
              />
              <Text
                style={{ color: theme.colors.primary }}
                type={TextTypes.small}
              >
                Front-End & Product
              </Text>
              <Text type={TextTypes.title}>Xavier Mod</Text>
            </Person>
            <Person>
              <Image
                src={domImg}
                style={{ width: "10rem" }}
                alt={"Promo image"}
              />
              <Text
                style={{ color: theme.colors.primary }}
                type={TextTypes.small}
              >
                Business & Operations
              </Text>
              <Text type={TextTypes.title}>Dominic Farr</Text>
            </Person>
          </People>
        </div>
      </ContentLayout>
    </Wrapper>
  );
};

export default Homepage;
