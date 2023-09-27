import React from "react";
import Logo from "./assets/flatini-logo.png";
import styled from "styled-components";

const Wrapper = styled.header`
  display: flex;
`;

const SignOutWrapper = styled.div`
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  text-align: right;
`;

const Header = (props: { showSignout: boolean }) => {
  const signOut = () => {
    chrome.storage.local.clear(function () {
      var error = chrome.runtime.lastError;
      if (error) {
        console.error(error);
      }
    });
    chrome.storage.sync.clear();
    window.location.reload();
  };

  return (
    <Wrapper style={{ cursor: "pointer", padding: 10 }}>
      <img style={{ width: 110 }} src={Logo} />
      {props.showSignout ? (
        <SignOutWrapper>
          <svg
            onClick={signOut}
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="white"
          >
            <path d="M16 10v-5l8 7-8 7v-5h-8v-4h8zm-16-8v20h14v-2h-12v-16h12v-2h-14z" />
          </svg>
        </SignOutWrapper>
      ) : null}
    </Wrapper>
  );
};

export default Header;
