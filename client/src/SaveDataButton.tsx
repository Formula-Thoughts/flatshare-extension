import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

// Declare a type for the tab object
type TabInfo = {
  url?: string;
  title?: string;
};

interface SaveDataButtonProps {
  onClickAction: (name: string, url: string, price: string) => void;
}

// collect title, url, and price to send to the server

function SaveDataButton({ onClickAction }: SaveDataButtonProps) {
  const saveData = () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs.length > 0) {
        const tab: TabInfo = tabs[0];
        const url = tab?.url || "";
        const title = tab?.title || "";

        console.log("Data saved:", { url, title });

        const activeTab = tabs[0];
        console.log(activeTab);
        // Send a message to the content script of the active tab
        chrome.tabs.sendMessage(
          activeTab.id || 0,
          { command: "SCRAPE" },
          (response) => {
            console.log("Response from content script:", response);
            onClickAction(title, url, response?.price || "");
          }
        );
      }
    });
  };
  return (
    <React.Fragment>
      <button onClick={saveData}>
        <FontAwesomeIcon icon={faPlus} />
      </button>
    </React.Fragment>
  );
}

export default SaveDataButton;
