import { Route, Routes, useNavigate } from "react-router-dom";
import FlatView from "./FlatView";
import { Flats } from "./Flats";
import Logo from "./assets/flatini-logo.png";
import FlatsContext, { useFlats } from "./context/AppProvider";
import { useEffect, useState } from "react";
import Landing from "./views/Landing";
import Settings from "./views/Settings";
import Invitations from "./views/Invitations";
import Auth from "./views/Auth";

function App() {
  // const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();
  const state = useFlats();
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
    } else if (url?.includes("https://localhost:3000/")) {
      authenticate();
    } else {
      navigate("/");
    }
  };

  const authenticate = () => {
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
      async function getAuthenticationDetails() {
        const authDetails = await chrome.scripting.executeScript({
          target: { tabId: tabs[0].id as number },
          func: () => {
            return JSON.stringify(localStorage);
          },
        });
        console.log("test", JSON.parse((authDetails as any)[0].result));

        console.log("tye", typeof (authDetails as any)[0].result);

        if ((authDetails as any)[0].result !== "{}") {
          console.log("tye val", (authDetails as any)[0].result);

          localStorage.setItem(
            "flatini-auth",
            JSON.stringify((authDetails as any)[0].result)
          );
        } else {
          localStorage.removeItem("flatini-auth");
        }
      }
      getAuthenticationDetails();
    });
  };

  const getAuthDetailsFromExtensionStorage = () =>
    localStorage.getItem("flatini-auth") || null;

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

  if (!getAuthDetailsFromExtensionStorage()) {
    return (
      <Routes>
        <Route path="/" element={<Auth />} />
      </Routes>
    );
  }

  return (
    <>
      <p>authDetails {JSON.stringify(getAuthDetailsFromExtensionStorage())}</p>
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
