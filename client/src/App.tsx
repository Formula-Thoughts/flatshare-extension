import { Route, Routes, useNavigate } from "react-router-dom";
import "./App.css";
import FlatView from "./FlatView";
import { Flats } from "./Flats";
import Logo from "./assets/flatini-logo.png";
import FlatsContext from "./context/FlatsContext";
import { useEffect, useState } from "react";
import { SelectGroup } from "./SelectGroup";
import { getGroupCode } from "./utils/storage";

function App() {
  const [groupCode, setGroupCode] = useState<string>("");
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  const defaultNavigation = (url: string | undefined) => {
    if (url?.includes("https://www.rightmove.co.uk/properties/")) {
      navigate("/FlatView");
    } else {
      navigate("/");
    }
  };

  useEffect(() => {
    const fetchGroupCode = async () => {
      const code = await getGroupCode();
      setGroupCode(code || "");
    };
    fetchGroupCode();
    setIsLoading(false);
  }, [getGroupCode]);

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

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (groupCode) {
    return (
      <FlatsContext>
        <header style={{ cursor: "pointer", padding: 10 }}>
          <img style={{ width: 110 }} src={Logo} />
        </header>
        <Routes>
          <Route path="/" element={<Flats />} />
          <Route path="/FlatView" element={<FlatView />} />
        </Routes>
      </FlatsContext>
    );
  }

  return (
    <FlatsContext>
      <header style={{ cursor: "pointer", padding: 10 }}>
        <img style={{ width: 110 }} src={Logo} />
      </header>
      <Routes>
        <Route path="/" element={<SelectGroup />} />
        <Route path="/Flats" element={<Flats />} />
        <Route path="/FlatView" element={<FlatView />} />
      </Routes>
    </FlatsContext>
  );
}

export default App;
