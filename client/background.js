console.log("background.js");
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  chrome.runtime.sendMessage({ action: "updatePopup", message });
});
