import MainLayout from "../layouts/MainLayout";
import styled from "styled-components";
import { useProvider } from "../context/AppProvider";
import { Button, Text, TextTypes } from "flatini-fe-library";

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const Link = styled.a`
  &:hover {
    button {
      border: 2px solid rgba(255, 255, 255, 1) !important;
    }
  }
`;

const Explore = () => {
  const { requirements } = useProvider();
  return (
    <MainLayout>
      <Wrapper>
        <div
          style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}
        >
          <Text type={TextTypes.title}>Explore</Text>
          <Text type={TextTypes.small}>
            Quickly access flats based on your requirements. We will only use
            your 1st desired location.
          </Text>
        </div>
        <Link
          href={`https://www.rightmove.co.uk/property-to-rent/search.html?searchLocation=${requirements?.locations?.[0]}&useLocationIdentifier=false&locationIdentifier=&rent=To+rent`}
          target="_blank"
          rel="noreferrer"
        >
          <Button
            style={{
              width: "100%",
              border: "2px solid rgba(255, 255, 255, 0.5)",
              background: "transparent",
              color: "white",
            }}
            label="Go to Rightmove"
          />
        </Link>
        <Link
          href={`https://www.zoopla.co.uk/to-rent/property/${requirements?.locations?.[0]}/?q=${requirements?.locations?.[0]}&price_frequency=per_month&price_max=${requirements?.price}`}
          target="_blank"
          rel="noreferrer"
        >
          <Button
            style={{
              width: "100%",
              border: "2px solid rgba(255, 255, 255, 0.5)",
              background: "transparent",
              color: "white",
            }}
            label="Go to Zoopla"
          />
        </Link>
        <Link
          href={`https://www.openrent.co.uk/properties-to-rent?term=${requirements?.locations?.[0]}&prices_max=${requirements?.price}`}
          target="_blank"
          rel="noreferrer"
        >
          <Button
            style={{
              width: "100%",
              border: "2px solid rgba(255, 255, 255, 0.5)",
              background: "transparent",
              color: "white",
            }}
            label="Go to OpenRent"
          />
        </Link>
        <Link
          href={`https://www.spareroom.co.uk/flatshare/${requirements?.locations?.[0]}/`}
          target="_blank"
          rel="noreferrer"
        >
          <Button
            style={{
              width: "100%",
              border: "2px solid rgba(255, 255, 255, 0.5)",
              background: "transparent",
              color: "white",
            }}
            label="Go to SpareRoom"
          />
        </Link>
        <Link
          href={`https://www.onthemarket.com/to-rent/`}
          target="_blank"
          rel="noreferrer"
        >
          <Button
            style={{
              width: "100%",
              border: "2px solid rgba(255, 255, 255, 0.5)",
              background: "transparent",
              color: "white",
            }}
            label="Go to OnTheMarket"
          />
        </Link>
      </Wrapper>
    </MainLayout>
  );
};

export default Explore;
