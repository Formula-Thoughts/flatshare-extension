import { Route, Routes, useNavigate } from "react-router-dom";
import FlatView from "./FlatView";
import { Flats } from "./Flats";
import Logo from "./assets/flatini-logo.png";
import FlatsContext, { useFlats } from "./context/AppProvider";
import { useEffect, useState } from "react";
import Landing from "./views/Landing";
import Settings from "./views/Settings";
import Invitations from "./views/Invitations";

function App() {
  // const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();
  const state = useFlats();
  const [token, setToken] = useState("");
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
    } else if (url?.includes("flatiniToken")) {
      setToken(url?.split("flatiniToken=")[1]);
    } else {
      navigate("/");
    }
  };

  // // Listens to changes on tabs
  // chrome.tabs.onUpdated.addListener(async (tabId, info, tab) => {
  //   console.log("updating tab2", tab);
  //   defaultNavigation(tab.url);
  // });

  // // Reads changes when active tab changes
  // chrome.tabs.onActivated.addListener(function (activeInfo) {
  //   // Gets the URL of the active tab
  //   chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
  //     let url = tabs[0].url;
  //     defaultNavigation(url);
  //   });
  // });

  useEffect(() => {
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
  }, []);

  return (
    <>
      <p>token{token}</p>
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
