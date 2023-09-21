// content.js
console.log("DOMContentLoaded - content.js");
createFlatiniButton();
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.command === "SCRAPE") {
    try {
      sendResponse({ price: getAllTextEndingWithPCM(document.body) });
    } catch (error) {
      console.log("error: ", error);
      sendResponse({ data: " ERROR " });
    }
  }
});

// Inject Flatini button into page
function createFlatiniButton() {
  const element = document.querySelector('[data-test="seeMapScroll"]');
  if (element) {
    const newButton = document.createElement("button");
    newButton.textContent = "Add to Flatini";
    newButton.style.borderRadius = "10px"; // Round border
    newButton.style.border = "2px solid green"; // 1px solid green border
    newButton.style.marginLeft = "10px"; // Margin-left of 10px
    newButton.style.fontWeight = "bold";
    newButton.style.padding = "5px";
    newButton.style.marginTop = "-5px";
    newButton.style.cursor = "pointer";
    newButton.style.backgroundColor = "#2a4d1a";
    newButton.style.color = "white";
    element.parentNode.insertBefore(newButton, element.nextSibling);

    // Add a click event listener to the new button (optional)
    newButton.addEventListener("click", function () {
      console.log("Button clicked!");
      const pageTitle = document.title;
      const pageURL = window.location.href;
      const price = getAllTextEndingWithPCM(document.body);
      console.log("data", { pageTitle, pageURL, price });
      // Send the data to the background script
      chrome.runtime
        .sendMessage({
          title: pageTitle,
          url: pageURL,
          price,
        })
        .then(() => {
          console.log("Message sent!", {
            title: pageTitle,
            url: pageURL,
            price,
          });
        })
        .catch((error) => {
          console.log("!!!error: ", error);
        });
    });
  }
}

// Find the element with price and returns it
function getAllTextEndingWithPCM(element) {
  let textContent = "";

  // Helper function to recursively traverse and collect text
  function traverse(node) {
    // Exclude script and style tags
    if (node.nodeName === "SCRIPT" || node.nodeName === "STYLE") {
      return;
    }
    // If the node is a text node and it ends with "pcm", add its content to the textContent
    if (
      node.nodeType === Node.TEXT_NODE &&
      /pcm$/i.test(node.textContent?.trim())
    ) {
      textContent += node.textContent?.trim() + " ";
    }

    // Recursively traverse child nodes
    for (const childNode of node.childNodes) {
      traverse(childNode);
    }
  }
  traverse(element || document.body);

  return textContent.trim();
}
