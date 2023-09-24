console.log("background.js");
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  chrome.runtime.sendMessage({ action: "updatePopup", message });
});

chrome.runtime.onInstalled.addListener(function (details) {
  if (details.reason === "install") {
    // This code will run only on initial installation
    console.log("Extension installed for the first time.");

    // Set a flag to indicate that the installation script has been executed
    chrome.storage.local.set({ installed: true }, function () {
      if (chrome.runtime.lastError) {
        console.error(chrome.runtime.lastError);
      }
    });

    // Set a random group code
    chrome.storage.local.set({ group: generateRandomString(8) }, function () {
      if (chrome.runtime.lastError) {
        console.error(chrome.runtime.lastError);
      }
    });
  }
});

function generateRandomString(length) {
  const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  let randomString = "";

  for (let i = 0; i < length; i++) {
    const randomIndex = Math.floor(Math.random() * characters.length);
    randomString += characters.charAt(randomIndex);
  }

  return randomString;
}
