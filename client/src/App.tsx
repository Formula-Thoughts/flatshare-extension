import { Route, Routes, useNavigate } from "react-router-dom";
import FlatView from "./FlatView";
import { Flats } from "./Flats";
import Logo from "./assets/flatini-logo.png";
import FlatsContext from "./context/AppProvider";
import { useEffect, useState } from "react";
import Landing from "./views/Landing";

function App() {
  // const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  const defaultNavigation = (url: string | undefined) => {
    if (url?.includes("https://www.rightmove.co.uk/properties/")) {
      navigate("/FlatView");
    } else {
      navigate("/");
    }
  };

  // Listens to changes on tabs
  chrome.tabs.onUpdated.addListener(async (tabId, info, tab) => {
    console.log("updating tab2", tab);
    defaultNavigation(tab.url);
  });

  // Reads changes when active tab changes
  chrome.tabs.onActivated.addListener(function (activeInfo) {
    // Gets the URL of the active tab
    chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
      let url = tabs[0].url;
      defaultNavigation(url);
    });
  });

  return (
    <FlatsContext>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/Flats" element={<Flats />} />
        <Route path="/FlatView" element={<FlatView />} />
      </Routes>
    </FlatsContext>
  );
}

export default App;
