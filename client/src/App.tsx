import { Route, Routes, useNavigate } from "react-router-dom";
import FlatView from "./FlatView";
import { Flats } from "./Flats";
import { useProvider } from "./context/AppProvider";
import { useEffect } from "react";
import Settings from "./views/Settings";
import Invitations from "./views/Invitations";
import Auth from "./views/Auth";
import CreateGroup from "./views/CreateGroup";
import { flatiniAuthWebsite } from "./utils/constants";

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
    state.getGroup();
  }, []);

  if (!state.getAuthenticatedUser()) {
    return (
      <Routes>
        <Route path="/" element={<Auth />} />
      </Routes>
    );
  }

  if (state.isGroupLoading) {
    return <p>loading...</p>;
  }

  if (!state.userHasGroup) {
    return (
      <Routes>
        <Route path="/" element={<CreateGroup />} />
      </Routes>
    );
  }

  return (
    <>
      {state.activeUrl ? (
        <Routes>
          {/* <Route path="/" element={<Landing />} /> */}
          <Route path="/" element={<Flats />} />
          <Route path="/Settings" element={<Settings />} />
          <Route path="/FlatView" element={<FlatView />} />
          <Route path="/Invitations" element={<Invitations />} />
        </Routes>
      ) : (
        <></>
      )}
    </>
  );
}

export default App;
