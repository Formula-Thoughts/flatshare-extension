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
import RedFlags from "./RedFlags";
import AddRedFlag from "./AddRedFlag";

function App() {
  const navigate = useNavigate();
  const state = useProvider();
  let url;
  const setActiveUrl = () => {
    console.log(
      "3 [setActiveUrl - App.tsx] -> Sets active URL",
      state.isGroupLoading
    );

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
    } else if (url?.includes(flatiniAuthWebsite as string)) {
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
      setActiveUrl();
    });
    chrome.tabs.onActivated.addListener(function () {
      setActiveUrl();
    });
  };

  useEffect(() => {
    console.log(
      "1 [useEffect - App.tsx] -> First use effect, app loads",
      state.isGroupLoading
    );
    addChromeEvents();

    if (state.userAuthToken) {
      state.getGroup();
      setActiveUrl();
    } else {
      state.authenticateUser();
    }
  }, []);

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
          <Route path="/RedFlags" element={<RedFlags />} />
          <Route path="/AddRedFlag" element={<AddRedFlag />} />
          <Route path="/Participants" element={<Participants />} />
        </Routes>
      ) : (
        <></>
      )}
    </>
  );
}

export default App;
