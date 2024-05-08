import Logo from "../flatini-library/components/Logo";
import styled from "styled-components";
import { Link, NavLink } from "react-router-dom";
import { flatiniAuthWebsite } from "../utils/constants";
import { FaEye, FaUser } from "react-icons/fa";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCog,
  faHouseChimney,
  faPeopleGroup,
} from "@fortawesome/free-solid-svg-icons";
import { useProvider } from "../context/AppProvider";

const Wrapper = styled.div`
  padding: 1rem;
  padding-bottom: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const NavBar = styled.div`
  display: flex;
  gap: 0.5rem;

  div {
    cursor: pointer;
  }
`;

const TopBar = styled.div`
  display: flex;
  align-items: center;
  justify-content: flex-start;
`;

const NavIcon = styled.div`
  width: 3rem;
  text-align: center;

  a {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    svg {
      opacity: 0.5;
    }
  }

  a.active {
    svg {
      opacity: 1;
    }
    .active-border {
      display: block;
    }
  }
`;

const NavIconActiveBorder = styled.div`
  display: none;
  width: 100%;
  height: 0.5rem;
  background: ${(props) => props.theme.colors.primary};
`;

const ViewingFlatBanner = styled.div`
  background-color: ${(props) => props.theme.colors.primary};
  color: black;
  text-align: center;
  padding: 0.8rem;
  display: flex;
  gap: 1rem;
  align-items: center;
  justify-content: center;

  a {
    color: black;
    font-weight: bold;
  }
`;

const Header = () => {
  const { activeUrl } = useProvider();
  return (
    <>
      {activeUrl?.propertyProvider !== null ? (
        <ViewingFlatBanner>
          <FaEye />
          <div>
            You are viewing <Link to="/FlatView">a flat</Link>
          </div>
        </ViewingFlatBanner>
      ) : null}
      <Wrapper>
        <TopBar>
          <Logo style={{ width: "8rem" }} />
          <div style={{ flex: 1, textAlign: "right" }}>
            <a href={flatiniAuthWebsite} target="_blank" rel="noreferrer">
              <FaUser size={20} />
            </a>
          </div>
        </TopBar>
        <NavBar>
          <NavIcon>
            <NavLink to="/">
              <FontAwesomeIcon
                style={{ fontSize: "1.4rem" }}
                icon={faHouseChimney}
              />
              <NavIconActiveBorder className="active-border" />
            </NavLink>
          </NavIcon>
          <NavIcon>
            <NavLink to="/Settings">
              <FontAwesomeIcon style={{ fontSize: "1.4rem" }} icon={faCog} />
              <NavIconActiveBorder className="active-border" />
            </NavLink>
          </NavIcon>
          <NavIcon>
            <NavLink to="/Participants">
              <FontAwesomeIcon
                style={{ fontSize: "1.4rem" }}
                icon={faPeopleGroup}
              />
              <NavIconActiveBorder className="active-border" />
            </NavLink>
          </NavIcon>
        </NavBar>
      </Wrapper>
    </>
  );
};

export default Header;
