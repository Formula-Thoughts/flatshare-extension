import { Route, Routes, useNavigate } from "react-router-dom";
import FlatView from "./FlatView";
import { Flats } from "./Flats";
import { useProvider } from "./context/AppProvider";
import { useEffect } from "react";
import Settings from "./views/Settings";
import Participants from "./views/Participants";
import Auth from "./views/Auth";
import CreateGroup from "./views/CreateGroup";
import { flatiniAuthWebsite } from "./utils/constants";
import Loading from "./views/Loading";
import ErrorPage from "./views/ErrorPage";
import Explore from "./views/Explore";

function App() {
  const navigate = useNavigate();
  const state = useProvider();
  let url;
  const setActiveUrl = () => {
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
      url = tabs[0].url;

      if (url) {
        const getPropertyProvider = (url: string) => {
          if (url?.includes("https://www.rightmove.co.uk/properties/")) {
            return "rightmove";
          }

          if (url?.includes("https://www.zoopla.co.uk/to-rent/details/")) {
            return "zoopla";
          }

          if (
            url?.includes(
              "https://www.spareroom.co.uk/flatshare/flatshare_detail.pl?flatshare_id="
            )
          ) {
            return "spareroom";
          }

          if (url?.includes("https://www.openrent.co.uk/property-to-rent/")) {
            return "openrent";
          }

          return null;
        };

        state.setActiveUrl({
          tabId: tabs[0].id,
          contents: url,
          propertyProvider: getPropertyProvider(url),
        });

        defaultNavigation(url);
      }
    });
  };

  const defaultNavigation = (url: string | undefined) => {
    if (
      url?.includes("https://www.rightmove.co.uk/properties/") ||
      url?.includes("https://www.zoopla.co.uk/to-rent/details/") ||
      url?.includes(
        "https://www.spareroom.co.uk/flatshare/flatshare_detail.pl?flatshare_id="
      ) ||
      url?.includes("https://www.openrent.co.uk/property-to-rent/")
    ) {
      navigate("/FlatView");
    } else if (url?.includes(flatiniAuthWebsite)) {
      state.authenticateUser();
      navigate("/");
    } else {
      navigate("/");
    }
  };

  const addChromeEvents = () => {
    chrome.tabs.onCreated.addListener(function () {
      // Code to run on extension installation or update
      setActiveUrl();
    });
    // Reads changes when active tab changes
    chrome.tabs.onUpdated.addListener(async () => {
      console.log("[Performance] onUpdated");
      setActiveUrl();
    });
    chrome.tabs.onActivated.addListener(function () {
      setActiveUrl();
      console.log("[Performance] onActivated");
    });
  };

  useEffect(() => {
    addChromeEvents();

    if (state.userAuthToken) {
      console.log(
        "state user token yes",
        state.userAuthToken,
        typeof state.userAuthToken
      );
      state.getGroup();
      setActiveUrl();
    } else {
      const existingLocalStorage = localStorage.getItem("flatini-auth");

      if (existingLocalStorage && existingLocalStorage !== "null") {
        state.setUserAuthToken(existingLocalStorage);
      } else {
        state.authenticateUser();
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [state.userAuthToken]);

  if (state.appHasError || (state.appHasError as string).length > 0) {
    return <ErrorPage data={state.appHasError} />;
  }

  if (!state.userAuthToken) {
    return (
      <Routes>
        <Route path="/" element={<Auth />} />
      </Routes>
    );
  }

  if (state.isGroupLoading) {
    return <Loading />;
  }

  if (!state.userHasGroup) {
    return (
      <>
        <Routes>
          <Route path="/" element={<CreateGroup />} />
        </Routes>
      </>
    );
  }

  return (
    <>
      {state.activeUrl ? (
        <Routes>
          <Route path="/" element={<Flats />} />
          <Route path="/Settings" element={<Settings />} />
          <Route path="/Explore" element={<Explore />} />
          <Route path="/FlatView" element={<FlatView />} />
          {/* <Route path="/Warnings" element={<Warnings />} /> */}
          <Route path="/Participants" element={<Participants />} />
        </Routes>
      ) : (
        <></>
      )}
    </>
  );
}

export default App;
