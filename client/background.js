console.log("background.js");
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("message", message);
  chrome.storage.local.get({ items: [] }, (result) => {
    const { items } = result;

    // Add the new data to the list of items
    items.push(message);

    // Save the updated list back to storage
    chrome.storage.local
      .set({ items })
      .then(() => {
        console.log("Data saved");
      })
      .catch((error) => {
        console.log("saving data into storage. error: ", error);
      });
  });
});
